#Obrigado @fnixdev.
import json
import os
import time


from yt_dlp import YoutubeDL
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


async def get_link(query):
    vid_id = get_yt_video_id(query)
    link = f"{BASE_YT_URL}{vid_id}"
    if vid_id is None:
        try:
            res_ = SearchVideos(query, offset=1, mode="json", max_results=1)
            link = json.loads(res_.result())["search_result"][0]["link"]
            id_ = link = json.loads(res_.result())["search_result"][0]["id"]
            return link, id_
        except Exception as e:
            return e
    else:
        return link, vid_id

# yt-dl args - extract video info
async def extract_inf(link, opts_):
    with YoutubeDL(opts_) as ydl:
        infoo = ydl.extract_info(link, False)
        ydl.process_info(infoo)
        duration_ = infoo["duration"]
        title_ = infoo["title"]
        channel_ = infoo["channel"]
        views_ = infoo["view_count"]
        capt_ = f"<a href={link}><b>{title_}</b></a>\n❯ Duração: {duration_}\n❯ Views: {views_}\n❯ Canal: {channel_}"
        return capt_, title_, duration_


@megux.on_message(filters.command(["video"], prefixes=["/", "!"]))
async def vid_(c: megux, message: Message):
    chat_id = message.chat.id 
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
    link, vid_id = await get_link(query)
    thumb_ = download(f"https://i.ytimg.com/vi/{vid_id}/maxresdefault.jpg", Config.DOWN_PATH)
    await msg.edit("📦 <i>Enviando...</i>")
    capt_, title_, duration_ = await extract_inf(link, vid_opts)
    await msg.delete()
    await c.send_video(chat_id, video=f"{Config.DOWN_PATH}{title_}.webm", caption=capt_, thumb=thumb_, duration=duration_)
    os.remove(f"{Config.DOWN_PATH}{title_}.webm")
    os.remove(f"{Config.DOWN_PATH}maxresdefault.jpg")


@megux.on_message(filters.command(["song", "music"], prefixes=["/", "!"]))
async def song_(c: megux, message: Message):
    chat_id = message.chat.id 
    query = " ".join(message.text.split()[1:])
    if not query:
        return await message.reply("`Vou baixar o vento?!`")
    msg = await message.reply("📦 <i>Baixando...</i>")
    if query.startswith("-f"):
        format_ = "flac/best"
        fid = "flac"
    else:
        format_ = "bestaudio/best"
        fid = "mp3"
    aud_opts = {
        "outtmpl": os.path.join(Config.DOWN_PATH, "%(title)s.%(ext)s"),
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        'format': format_,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
                {
                     'key': 'FFmpegExtractAudio',
                     'preferredcodec': fid,
                     'preferredquality': '320',
                 },
            {"key": "EmbedThumbnail"},
            {"key": "FFmpegMetadata"},
        ],
        "quiet": True,
    }
    query_ = query.strip("-f")
    link, vid_id = await get_link(query_)
    await msg.edit("📦 <i>Enviando...</i>")
    thumb_ = download(f"https://i.ytimg.com/vi/{vid_id}/maxresdefault.jpg", Config.DOWN_PATH)
    capt_, title_, duration_ = await extract_inf(link, aud_opts)
    capt_ += f"\n❯ Formato: {fid}"
    await msg.delete()
    await c.send_audio(chat_id, audio=f"{Config.DOWN_PATH}{title_}.{fid}", caption=capt_, thumb=thumb_, duration=duration_)
    os.remove(f"{Config.DOWN_PATH}{title_}.{fid}")
    os.remove(f"{Config.DOWN_PATH}maxresdefault.jpg")
