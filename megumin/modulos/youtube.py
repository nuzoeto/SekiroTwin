import json
import os
import time

import requests
from pytube import YouTube
from youtubesearchpython import Search, SearchVideos

from pyrogram.types import Message
from pyrogram import filters
from megumin import megux


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


@megux.on_message(filters.command(["song", "music"]))
async def song(client: megux, message: Message):
    music = " ".join(message.text.split()[1:])
    if not music:
        return await message.reply("`Vou baixar o vento?!`")
    msg = await message.reply("`Processando...`")
    result = search_music(music)
    if result is None:
        return await msg.edit("`Não foi possível encontrar a música.`")
    link = get_link(result)
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


@megux.on_message(filters.command(["video"]))
async def video_(client: megux, message: Message):
    video = " ".join(message.text.split()[1:])
    if not video:
        return await message.reply("`Vou baixar o vento?!`")
    msg = await message.reply("`Processando...`")
    result = search_video(video)
    if result is None:
        return await message.edit("`Não foi possível encontrar o vídeo.`")
    link = get_link(result)
    m, filename = get_filename(result)
    try:
        down_video(link, filename)
    except Exception as e:
        await msg.edit("`Não foi possível baixar o video.`")
        time.sleep(2)
        await msg.delete()
        print(str(e))
    else:
        caption = f"**Título ➠** __[{result[0]['title']}]({link})__\n**Canal ➠** __{result[0]['channel']}__"
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
