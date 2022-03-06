import os
import yt_dlp
import shutil
import tempfile
import re
import io
import asyncio
import datetime 

from typing import Tuple, Callable
from functools import wraps, partial
from yt_dlp.utils import DownloadError
from pyrogram import filters
from pyrogram.errors import BadRequest, Forbidden, MessageTooLong
from pyrogram.types import CallbackQuery, Message

from megumin import megux

def aiowrap(func: Callable) -> Callable:
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run


@aiowrap
def extract_info(instance, url, download=True):
    return instance.extract_info(url, download)


def pretty_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


@megux.on_message(filters.command("ytdl", prefixes=["/","!"]))
async def ytdl_(c: megux, m: Message):
    args = " ".join(m.text.split()[1:])
    user = m.from_user.id

    if m.reply_to_message and m.reply_to_message.text:
        url = m.reply_to_message.text
    elif m.text and args:
        url = args
    else:
        await m.reply_text("Por favor, responda a um link do YouTube ou texto.")
        return

    ydl = yt_dlp.YoutubeDL(
        {
            "outtmpl": "dls/%(title)s-%(id)s.%(ext)s",
            "format": "mp4",
            "noplaylist": True,
        }
    )
    rege = re.match(
        r"http(?:s?):\/\/(?:www\.)?(?:music\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?",
        url,
        re.M,
    )

    temp = url.split("t=")[1].split("&")[0] if "t=" in url else "0"
    if not rege:
        yt = await extract_info(ydl, "ytsearch:" + url, download=False)
        yt = yt["entries"][0]
    else:
        try:
            yt = await extract_info(ydl, rege.group(), download=False)
        except DownloadError as e:
            await m.reply_text(f"<b>Error!</b>\n<code>{e}</code>")
            return

    if not temp.isnumeric():
        temp = "0"

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
                f"_aud.{yt['id']}|{afsize}|{vformat}|{temp}|{user}|{m.message_id}",
            ),
            (
                "🎬 Vídeo",
                f"_vid.{yt['id']}|{vfsize}|{vformat}|{temp}|{user}|{m.message_id}",
            ),
        ]
    ]

    if " - " in yt["title"]:
        performer, title = yt["title"].rsplit(" - ", 1)
    else:
        performer = yt.get("creator") or yt.get("uploader")
        title = yt["title"]

    text = f"🎧 <b>{performer}</b> - <i>{title}</i>\n"
    text += f"💾 <code>{pretty_size(afsize)}</code> (áudio) / <code>{pretty_size(int(vfsize))}</code> (vídeo)\n"
    text += f"⏳ <code>{datetime.timedelta(seconds=yt.get('duration'))}</code>"

    await m.reply_text(text, reply_markup=c.ikb(keyboard))


@megux.on_callback_query(filters.regex("^(_(vid|aud))"))
async def cli_ytdl(c, cq: CallbackQuery):
    data, fsize, vformat, temp, userid, mid = cq.data.split("|")
    if cq.from_user.id != int(userid):
        return await cq.answer("Este botão não é para você!", cache_time=60)
    if int(fsize) > 309715200:
        return await cq.answer(
            (
                "Desculpe! Não posso baixar esta mídia pois ela "
                "ultrapassa o meu limite de 300MB de download."
            ),
            show_alert=True,
            cache_time=60,
        )
    vid = re.sub(r"^\_(vid|aud)\.", "", data)
    url = "https://www.youtube.com/watch?v=" + vid
    await cq.message.edit("Baixando...")
    await cq.answer("Seu pedido é uma ordem... >-<", cache_time=0)
    with tempfile.TemporaryDirectory() as tempdir:
        path = os.path.join(tempdir, "ytdl")
    if "vid" in data:
        ydl = yt_dlp.YoutubeDL(
            {
                "outtmpl": f"{path}/%(title)s-%(id)s.%(ext)s",
                "format": f"{vformat}+140",
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
    except DownloadError as e:
        await cq.message.edit(f"<b>Error!</b>\n<code>{e}</code>")
        return
    await cq.message.edit("Enviando...")
    filename = ydl.prepare_filename(yt)
    ttemp = f"⏰ {datetime.timedelta(seconds=int(temp))} | " if int(temp) else ""
    thumb = io.BytesIO((await http.get(yt["thumbnail"])).content)
    thumb.name = "thumbnail.jpeg"
    caption = f"{ttemp} <a href='{yt['webpage_url']}'>{yt['title']}</a></b>"
    caption += "\n<b>Views:</b> <code>{:,}</code>".format(yt["view_count"])
    caption += "\n<b>Likes:</b> <code>{:,}</code>".format(yt["like_count"])
    if "vid" in data:
        try:
            await c.send_chat_action(cq.message.chat.id, "upload_video")
            await c.send_video(
                chat_id=cq.message.chat.id,
                video=filename,
                width=1920,
                height=1080,
                caption=caption,
                duration=yt["duration"],
                thumb=thumb,
                reply_to_message_id=int(mid),
            )
        except BadRequest as e:
            await c.send_message(
                chat_id=cq.message.chat.id,
                text=(
                    "Desculpe! Não consegui enviar o "
                    "vídeo por causa de um erro.\n"
                    f"<b>Erro:</b> <code>{e}</code>"
                ),
                reply_to_message_id=int(mid),
            )
    else:
        if " - " in yt["title"]:
            performer, title = yt["title"].rsplit(" - ", 1)
        else:
            performer = yt.get("creator") or yt.get("uploader")
            title = yt["title"]
        try:
            await c.send_chat_action(cq.message.chat.id, "upload_audio")
            await c.send_audio(
                chat_id=cq.message.chat.id,
                audio=filename,
                caption=caption,
                title=title,
                performer=performer,
                duration=yt["duration"],
                thumb=thumb,
                reply_to_message_id=int(mid),
            )
        except BadRequest as e:
            await c.send_message(
                chat_id=cq.message.chat.id,
                text=(
                    "Desculpe! Não consegui enviar o "
                    "vídeo por causa de um erro.\n"
                    f"<b>Erro:</b> <code>{e}</code>"
                ),
                reply_to_message_id=int(mid),
            )
    await cq.message.delete()
    shutil.rmtree(tempdir, ignore_errors=True)
