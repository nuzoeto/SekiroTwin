#Obrigado @fnixdev.
import json
import os
import time
import glob


from yt_dlp import YoutubeDL
from pathlib import Path
from youtubesearchpython import Search, SearchVideos
from wget import download
from re import compile as comp_regex  

from pyrogram.types import Message
from pyrogram import filters
from megumin import megux, Config


BASE_YT_URL = ("https://www.youtube.com/watch?v=")
YOUTUBE_REGEX = comp_regex(
    r"(?:youtube\.com|youtu\.be)/(?:[\w-]+\?v=|embed/|v/|shorts/)?([\w-]{11})"
)


def get_yt_video_id(url: str):
    # https://regex101.com/r/c06cbV/1
    match = YOUTUBE_REGEX.search(url)
    if match:
        return match.group(1)


@megux.on_message(filters.command(["song", "music"], Config.TRIGGER))
async def song_(c: megux, message: Message):
    query = " ".join(message.text.split()[1:])
    if not query:
        return await message.reply("`Vou baixar o vento?!`")
    msg = await message.reply("📦 <i>Baixando... </i>")
    link = await get_link(query)
    aud_opts = {
        "outtmpl": os.path.join(Config.DOWN_PATH, "%(title)s.%(ext)s"),
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        'format': 'bestaudio/best',
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
                {
                     'key': 'FFmpegExtractAudio',
                     'preferredcodec': "mp3",
                     'preferredquality': '320',
                 },
            {"key": "EmbedThumbnail"},
            {"key": "FFmpegMetadata"},
        ],
        "quiet": True,
    }
    filename_, capt_, duration_ = extract_inf(link, aud_opts)
    if int(duration_) > 3600:
        return await msg.edit("__Esse áudio é muito longo, a duração máxima é de 1 hora__")
    if filename_ == 0:
        _fpath = ''
        for _path in glob.glob(os.path.join(Config.DOWN_PATH, '*')):
            if not _path.lower().endswith((".jpg", ".png", ".webp")):
                _fpath = _path
        if not _fpath:
            await msg.edit("nothing found !")
            return
        await msg.edit("📦 <i>Enviando...</i>")
        await message.reply_audio(audio=Path(_fpath), caption=capt_, duration=duration_)
        await msg.delete()
        os.remove(Path(_fpath))
    else:
        await message.reply(str(filename_))


@megux.on_message(filters.command(["video", "vid"], Config.TRIGGER))
async def vid_(c: megux, message: Message):
    query = " ".join(message.text.split()[1:])
    if not query:
        return await message.reply("`Vou baixar o vento?!`")
    msg = await message.reply("📦 <i>Baixando...</i>")
    vid_opts = {
        "outtmpl": os.path.join(Config.DOWN_PATH, "%(title)s.%(ext)s"),
        'writethumbnail': False,
        'prefer_ffmpeg': True,
        'format': 'bestvideo+bestaudio/best',
        'postprocessors': [
                {
                    'key': 'FFmpegMetadata'
                }
            ],
        "quiet": True,
    }
    link = await get_link(query)
    filename_, capt_, duration_ = extract_inf(link, vid_opts)
    if int(duration_) > 3600:
        return await msg.edit("__Esse áudio é muito longo, a duração máxima é de 1 hora__")
    if filename_ == 0:
        _fpath = ''
        for _path in glob.glob(os.path.join(Config.DOWN_PATH, '*')):
            if not _path.lower().endswith((".jpg", ".png", ".webp")):
                _fpath = _path
        if not _fpath:
            return await msg.edit("nothing found !")
        await msg.edit("📦 <i>Enviando...</i>")
        await message.reply_video(video=Path(_fpath), caption=capt_, duration=duration_)
        await msg.delete()
        os.remove(Path(_fpath))
    else:
        await message.reply(str(filename_))


# retunr regex link or get link with query
async def get_link(query):
    vid_id = get_yt_video_id(query)
    link = f"{BASE_YT_URL}{vid_id}"
    if vid_id is None:
        try:
            res_ = SearchVideos(query, offset=1, mode="json", max_results=1)
            link = json.loads(res_.result())["search_result"][0]["link"]
            return link
        except Exception as e:
            LOGGER.exception(e)
            return e
    else:
        return link


def extract_inf(url, _opts):
    try:
        x = YoutubeDL(_opts)
        infoo = x.extract_info(url, False)
        x.process_info(infoo)
        duration_ = infoo["duration"]
        title_ = infoo["title"].replace("/", "_")
        channel_ = infoo["channel"]
        views_ = infoo["view_count"]
        capt_ = f"<a href={url}><b>{title_}</b></a>\n❯ Duração: {duration_}\n❯ Views: {views_}\n❯ Canal: {channel_}"
        dloader = x.download(url)
    except Exception as y_e:  # pylint: disable=broad-except
        LOGGER.exception(y_e)
        return y_e
    else:
        return dloader, capt_, duration_
