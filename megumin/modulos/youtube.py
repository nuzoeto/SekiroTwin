import json
import os
import time

import requests
from pytube import YouTube
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
async def vid_(message: Message):
    chat_id = message.chat.id
    query = " ".join(message.text.split()[1:])
    if not query:
        return await message.reply("`Vou baixar o vento?!`")
    msg = await message.reply("📦 <i>Baixando...</i>")
    link, vid_id = await get_link(query)
    thumb_ = download(f"https://i.ytimg.com/vi/{vid_id}/maxresdefault.jpg", Config.DOWN_PATH)
    await msg.edit("📦 <i>Enviando...</i>")
    capt_, title_, duration_ = await extract_inf(link)
    await msg.delete()
    await message.reply_video(video=f"{Config.DOWN_PATH}{title_}.webm", caption=capt_, thumb=thumb_, duration=duration_)
    os.remove(f"{Config.DOWN_PATH}{title_}.webm")
    os.remove(f"{Config.DOWN_PATH}maxresdefault.jpg")
