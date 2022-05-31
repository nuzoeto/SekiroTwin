# lastfm module by @fnix

import asyncio
import os

from telegraph import upload_file
from wget import download
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, InlineQuery, InlineQueryResultPhoto, InlineQueryResultArticle, InputTextMessageContent
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from io import BytesIO

from megumin import megux, Config
from megumin.utils.decorators import input_str
from .misc import *
from megumin.utils import get_collection, get_response

API = "http://ws.audioscrobbler.com/2.0"
LAST_KEY = Config.LASTFM_API_KEY
REG = get_collection("USERS")


@megux.on_message(filters.command(["lt", "lastfm"], prefixes=["/", "!"]))
async def last_(_, message: Message):
    query = input_str(message)
    user_ = message.from_user
    lastdb = await REG.find_one({"id_": user_.id})
    if not (lastdb or query):
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Create LastFM account", url="https://www.last.fm/join"
                    )
                ]
            ]
        )
        reg_ = "__Enter some username or use /set (username) to set yours. If you don't already have a LastFM account, click the button below to register.__"
        await message.reply(reg_, reply_markup=button)
        return
    if query:
        user_lastfm = query
    else:
        user_lastfm = lastdb["last_data"]
    
    # request on lastfm
    params = {
        "method": "user.getrecenttracks",
        "limit": 1,
        "extended": 1,
        "user": user_lastfm,
        "api_key": Config.LASTFM_API_KEY,
        "limit": 1,
        "format": "json",
    }
   view_data = await get_response.json(link=API, params=params)
   recent_song = view_data["recenttracks"]["track"]
   if len(recent_song) == 0:
       if query:
           return
      else:
           return
  song_ = recent_song[0]
  song_name = song_["name"]
  artist_name = song_["artist"]["name"]
  image_ = song_["image"][3].get("#text")
  params_ = {
      "method": "track.getInfo",
      "track": song_name,
      "artist": artist_name,
      "user": user_lastfm,
      "api_key": Config.LASTFM_API_KEY,
      "format": "json",
  }
  view_data_ = await get_response.json(link=API, params=params_)
  get_track = view_data_["track"]
  get_scrob = int(get_track["userplaycount"])
  await message.reply(f"{message.from_user.first_name} está ouvindo\n{artist_name} - {song_name}")

          

@megux.on_message(filters.command(["setuser", "reg"], prefixes=["/", "!"]))
async def last_save_user(_, message: Message):
    user_id = message.from_user.id
    fname = message.from_user.first_name
    uname = message.from_user.username
    text = input_str(message)
    if not text:
        await message.reply("__Bruh.. use /set username.__")
        return
    found = await REG.find_one({"id_": user_id})
    user_start = f"#USER_REGISTER #LOGS\n\n**User:** {fname}\n**ID:** {user_id} <a href='tg://user?id={user_id}'>**Link**</a>"
    if uname:
        user_start += f"\n**Username:** @{uname}"
    if found:
        await asyncio.gather(
                REG.update_one({"id_": user_id}, {
                                "$set": {"last_data": text}}, upsert=True),
                message.reply("__Your username has been successfully updated.__")
            )
    else:
        await asyncio.gather(
                REG.update_one({"id_": user_id}, {
                                "$set": {"last_data": text}}, upsert=True),
                c.send_log(
                    user_start,
                    disable_notification=False,
                    disable_web_page_preview=True,
                ),
                message.reply("__Your username has been successfully set.__")
            )


@megux.on_message(filters.command(["deluser", "duser"], prefixes=["/", "!"]))
async def last_save_user(_, message: Message):
    user_id = message.from_user.id
    found = await REG.find_one({"id_": user_id})
    if found:
        await asyncio.gather(
                REG.delete_one(found),
                message.reply("__Your username has been deleted.__")
            )
    else:
        return await message.reply("__You don't have a registered username__")
