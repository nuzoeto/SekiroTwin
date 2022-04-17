import io
import ffmpeg
import os
import re
import html
import httpx
import shutil
import yt_dlp
import tempfile
import datetime
import rapidjson
import math
import asyncio 


from typing import Union, Tuple, Callable
from functools import wraps, partial

from yt_dlp.utils import DownloadError


def pretty_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def aiowrap(func: Callable) -> Callable:
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run


http = httpx.AsyncClient()


from pyrogram.types import Message, CallbackQuery
from pyrogram.errors import BadRequest
from pyrogram import filters
from pyrogram.helpers import ikb

from megumin import megux 


@aiowrap
def extract_info(instance, url, download=True):
    return instance.extract_info(url, download)


@megux.on_message(filters.command("ytdl", prefixes=["/", "!"]))
async def ytdlcmd(c: megux, m: Message):
    user = m.from_user.id

    if m.reply_to_message and m.reply_to_message.text:
        url = m.reply_to_message.text
    elif len(m.command) > 1:
        url = m.text.split(None, 1)[1]
    else:
        await m.reply_text("`Vou baixar o vento?!`")
        return

    ydl = yt_dlp.YoutubeDL(
        {"outtmpl": "dls/%(title)s-%(id)s.%(ext)s", "format": "mp4", "noplaylist": True}
    )
    rege = re.match(
        r"http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?",
        url,
        re.M,
    )

    if "t=" in url:
        temp = url.split("t=")[1].split("&")[0]
    else:
        temp = 0

    if not rege:
        yt = await extract_info(ydl, "ytsearch:" + url, download=False)
        yt = yt["entries"][0]
    else:
        yt = await extract_info(ydl, rege.group(), download=False)

    for f in yt["formats"]:
        if f["format_id"] == "140":
            afsize = f["filesize"] or 0
        if f["ext"] == "mp4" and f["filesize"] is not None:
            vfsize = f["filesize"] or 0
            vformat = f["format_id"]

    keyboard = [
        [
            (
                "💿 Áudio",
                f'_aud.{yt["id"]}|{afsize}|{temp}|{vformat}|{m.chat.id}|{user}|{m.message_id}',
            ),
            (
                "📽 Vídeo",
                f'_vid.{yt["id"]}|{vfsize}|{temp}|{vformat}|{m.chat.id}|{user}|{m.message_id}',
            ),
        ]
    ]

    if " - " in yt["title"]:
        performer, title = yt["title"].rsplit(" - ", 1)
    else:
        performer = yt.get("creator") or yt.get("uploader")
        title = yt["title"]

    text = f"🎧 <b>{performer}</b> - <i>{title}</i>\n"
    text += f"💾 <code>{pretty_size(afsize)}</code> (audio) / <code>{pretty_size(int(vfsize))}</code> (video)\n"
    text += f"⏳ <code>{datetime.timedelta(seconds=yt.get('duration'))}</code>"

    await m.reply_text(text, reply_markup=ikb(keyboard))


@megux.on_callback_query(filters.regex("^(_(vid|aud))"))
async def cli_ytdl(c: megux, cq: CallbackQuery):
    data, fsize, temp, vformat, cid, userid, mid = cq.data.split("|")
    if not cq.from_user.id == int(userid):
        return await cq.answer("Esse botão não é para você.", cache_time=60)
    if int(fsize) > 500000000:
        return await cq.answer(
            "O Vídeo ou Música qual você deseja baixar excede o meu tamanho de 500MB.\nNão foi possível baixar e enviar, desculpe.",
            show_alert=True,
            cache_time=60,
        )
    vid = re.sub(r"^\_(vid|aud)\.", "", data)
    url = "https://www.youtube.com/watch?v=" + vid
    await cq.message.edit("Baixando...")
    with tempfile.TemporaryDirectory() as tempdir:
        path = os.path.join(tempdir, "ytdl")

    ttemp = ""
    if int(temp):
        ttemp = f"⏰ {datetime.timedelta(seconds=int(temp))} | "

    if "vid" in data:
        ydl = yt_dlp.YoutubeDL(
            {
                "outtmpl": f"{path}/%(title)s-%(id)s.%(ext)s",
                "format": f"{vformat}+140",
                "extractaudio": True,
                "noplaylist": True,
            }
        )
    else:
        ydl = yt_dlp.YoutubeDL(
            {
                "outtmpl": f"{path}/%(title)s-%(id)s.%(ext)s",
                "format": "140",
                "extractaudio": True,
                "noplaylist": True,
            }
        )
    try:
        yt = await extract_info(ydl, url, download=True)
    except BaseException as e:
        await cq.message.edit(f"Desculpe! Não pude enviar o vídeo devido a um erro.\n<b>Erro:</b> <code>{e}</code>")
        return
    await cq.message.edit("Enviando...")
    filename = ydl.prepare_filename(yt)
    thumb = io.BytesIO((await http.get(yt["thumbnail"])).content)
    thumb.name = "thumbnail.png"
    if "vid" in data:
        try:
            await c.send_video(
                int(cid),
                filename,
                width=1920,
                height=1080,
                caption=ttemp + yt["title"],
                duration=yt["duration"],
                thumb=thumb,
                reply_to_message_id=int(mid),
            )
        except BadRequest as e:
            await c.send_message(
                chat_id=int(cid),
                text="Desculpe! Não pude enviar o vídeo devido a um erro.\n<b>Erro:</b> <code>{}</code>".format(errmsg=e),
                reply_to_message_id=int(mid),
            )
    else:
        if " - " in yt["title"]:
            performer, title = yt["title"].rsplit(" - ", 1)
        else:
            performer = yt.get("creator") or yt.get("uploader")
            title = yt["title"]
        try:
            await c.send_audio(
                int(cid),
                filename,
                title=title,
                performer=performer,
                caption=ttemp[:-2],
                duration=yt["duration"],
                thumb=thumb,
                reply_to_message_id=int(mid),
            )
        except BadRequest as e:
            await c.send_message(
                chat_id=int(cid),
                text="Desculpe! Não pude enviar a música devido a um erro.\n<b>Erro:</b> <code>{}</code>".format(errmsg=e),
                reply_to_message_id=int(mid),
            )
    await cq.message.delete()
