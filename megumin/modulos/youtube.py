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


def search_music(query):
    search = Search(query, limit=1)
    return search.result()["result"]


def search_video(query):
    search = SearchVideos(query, offset=1, mode="json", max_results=1)
    print(str(search.result()))
    return json.loads(search.result())["search_result"]


def get_link(result) -> str:
    return result[0]["link"]


def get_filename(result) -> str:
    title_ = str(result[0]["title"]).replace("/", "")
    title = title_.replace(" ", "_")
    return title + ".mp3", title + ".mp4"


def get_duration(result):
    duration = result[0]["duration"]
    secmul, dur, dur_arr = 1, 0, duration.split(":")
    for i in range(len(dur_arr) - 1, -1, -1):
        dur += int(dur_arr[i]) * secmul
        secmul *= 60
    return duration, dur


def durate(result):
    duraction = result[0]["duration"]


def get_thumb(result):
    thumbnail = result[0]["thumbnails"][0]["url"]
    title = str(result[0]["title"]).replace("/", "")
    thumb_name = f"{title}.jpg"
    thumb = requests.get(thumbnail, allow_redirects=True)
    open(os.path.join("./megumin/xcache/", thumb_name), "wb").write(thumb.content)
    return thumb_name


def down_song(link, filename):
    YouTube(link).streams.filter(only_audio=True)[0].download(
        "./megumin/xcache/", filename=filename
    )


def down_video(link, filename):
    YouTube(link).streams.get_highest_resolution().download(
        "./megumin/xcache/", filename=filename
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


@megux.on_message(filters.command(["ytsong", "ytmusic"], prefixes=["/", "!"]))
async def song(client: megux, message: Message):
    music = " ".join(message.text.split()[1:])
    user_id = message.from_user.id
    if not music:
        return await message.reply("`Vou baixar o vento?!`")
    if user_id in Config.BLACK_LIST:
        return await message.reply(f"Você não pode me usar devido ao seu id estar na blacklist.\n\n<b>Seu ID é</b>: {user_id}.")
    msg = await message.reply("📦 __Baixando...__")
    result = search_music(music)
    if result is None:
        return await msg.edit("`Não foi possível encontrar a música.`")
    link = get_link(result)
    duracion = durate(result) 
    duration, dur = get_duration(result)
    filename, m = get_filename(result)
    thumb = get_thumb(result)
    try:
        down_song(link, filename)
    except Exception as e:
        await msg.edit("`Não foi possível baixar a música.`")
        print(str(e))
        time.sleep(2)
        await msg.delete()
    else:
        await msg.edit("📦 __Enviando...__")
        await megux.send_chat_action(message.chat.id, "upload_audio")
        if os.path.exists(f"./megumin/xcache/{thumb}"):
            caption = f"""
**Título:** __[{result[0]['title']}]({link})__
**Duração:** __{duration}__
**Views:** __{result[0]['viewCount']["text"]}__
"""
            try:
                await msg.reply_audio(
                    audio=f"./megumin/xcache/{filename}",
                    caption=caption,
                    title=result[0]["title"],
                    thumb=f"./megumin/xcache/{thumb}",
                    duration=dur,
                )
            except Exception as e:
                await msg.edit("`Não foi possível enviar a música.`")
                print(str(e))
                time.sleep(2)
                await msg.delete()
            finally:
                await msg.delete()
                os.remove(f"./megumin/xcache/{filename}")
                os.remove(f"./megumin/xcache/{thumb}")


@megux.on_message(filters.command(["ytvideo"], prefixes=["/", "!"]))
async def video_(client: megux, message: Message):
    video = " ".join(message.text.split()[1:])
    user_id = message.from_user.id
    if not video:
        return await message.reply("`Vou baixar o vento?!`")
    if user_id in Config.BLACK_LIST:
        return await message.reply(f"Você não pode me usar devido ao seu id estar na blacklist.\n\n<b>Seu ID é</b>: {user_id}.")
    msg = await message.reply("📦 __Baixando...__")
    result = search_video(video)
    if result is None:
        return await message.edit("`Não foi possível encontrar o vídeo.`")
    link = get_link(result)
    duration, dur = get_duration(result)
    m, filename = get_filename(result)
    try:
        down_video(link, filename)
    except Exception as e:
        await msg.edit("`Não foi possível baixar o video.`")
        time.sleep(2)
        await msg.delete()
        print(str(e))
    else:
        await msg.edit("📦 __Enviando...__")
        await megux.send_chat_action(message.chat.id, "upload_video")
        caption = f"**Título ➠** __[{result[0]['title']}]({link})__\n**Duração ➠** __{duration}__\n**Canal ➠** __{result[0]['channel']}__"
        try:
            await msg.reply_video(
                video=f"./megumin/xcache/{filename}",
                caption=caption,
            )
        except Exception as e:
            await msg.edit("`Não foi possível enviar o vídeo.`")
            print(str(e))
            time.sleep(2)
            await msg.delete()
        finally:
            await msg.delete()
            os.remove(f"./megumin/xcache/{filename}")

@megux.on_message(filters.command(["video"], prefixes=["/", "!"]))
async def vid_(message: Message):
    chat_id = message.chat.id
    query = message.input_str
    if not query:
        return await message.edit("`Vou baixar o vento?!`", del_in=5)
    msg = await message.reply("📦 <i>Baixando...</i>")
    link, vid_id = await get_link(query)
    thumb_ = download(f"https://i.ytimg.com/vi/{vid_id}/maxresdefault.jpg", Config.DOWN_PATH)
    await msg.edit("📦 <i>Enviando...</i>")
    capt_, title_, duration_ = await extract_inf(link, vid_opts)
    await msg.delete()
    await message.reply_video(video=f"{Config.DOWN_PATH}{title_}.webm", caption=capt_, thumb=thumb_, duration=duration_)
    os.remove(f"{Config.DOWN_PATH}{title_}.webm")
    os.remove(f"{Config.DOWN_PATH}maxresdefault.jpg")
