import os
import yt_dlp
import shutil
import tempfile
import re
import io
import asyncio
import datetime
import math
import httpx 

from typing import Tuple, Callable
from functools import wraps, partial
from yt_dlp.utils import DownloadError
from pyrogram import filters
from pyrogram.errors import BadRequest, Forbidden, MessageTooLong
from pyrogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ForceReply


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


def ikb(rows = []):
    lines = []
    for row in rows:
        line = []
        for button in row:
            button = btn(*button) # InlineKeyboardButton
            line.append(button)
        lines.append(line)
    return InlineKeyboardMarkup(inline_keyboard=lines)
    #return {'inline_keyboard': lines}

def btn(text, value, type = 'callback_data'):
    return InlineKeyboardButton(text, **{type: value})
    #return {'text': text, type: value}


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


    if " - " in yt["title"]:
        performer, title = yt["title"].rsplit(" - ", 1)
    else:
        performer = yt.get("creator") or yt.get("uploader")
        title = yt["title"]

    data, fsize, vformat, temp, userid, mid = cq.data.split("|")
    if cq.from_user.id != int(userid):
        return await cq.answer("Este botão não é para você!", cache_time=60)
    if int(fsize) > 709715200:
        return await m.reply(
            (
                "Desculpe! Não posso baixar esta mídia pois ela "
                "ultrapassa o meu limite de 700MB de download."
            )
    url = "https://www.youtube.com/watch?v=" + vid
    msg = await m.reply("Baixando...")
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
        await msg.edit(f"<b>Error!</b>\n<code>{e}</code>")
        return
    await msg.edit("Enviando...")
    filename = ydl.prepare_filename(yt)
    ttemp = f"⏰ {datetime.timedelta(seconds=int(temp))} | " if int(temp) else ""
    thumb = io.BytesIO((await http.get(yt["thumbnail"])).content)
    thumb.name = "thumbnail.jpeg"
    caption = f"{ttemp} <a href='{yt['webpage_url']}'>{yt['title']}</a></b>"
    caption += "\n<b>Views:</b> <code>{:,}</code>".format(yt["view_count"])
    caption += "\n<b>Likes:</b> <code>{:,}</code>".format(yt["like_count"])
            await c.send_video(
                chat_id=m.chat.id,
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
                chat_id=m.chat.id,
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
        
    await msg.delete()
    shutil.rmtree(tempdir, ignore_errors=True)
