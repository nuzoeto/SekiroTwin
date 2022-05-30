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


async def _init():
    global LAST_USERS  # pylint: disable=global-statement
    lastdb = await REG.find_one({"_id": "LAST_USERS"})
    if lastdb:
        LAST_USERS = lastdb["last_data"]



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
    try:
        view_data = await get_response.json(link=API, params=params)
    except ValueError:
        return await message.reply("__Error. Make sure you entered the correct username__")
    if "error" in view_data:
        return await message.reply(view_data["error"])
    recent_song = view_data["recenttracks"]["track"]
    if len(recent_song) == 0:
        if query:
            return await message.reply(f"__{user_lastfm} don't scrobble any music__")
        else:
            return await message.reply("__You don't scrobble any music__")
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
    try:
        view_data_ = await get_response.json(link=API, params=params_)
        get_track = view_data_["track"]
        get_scrob = int(get_track["userplaycount"])
        if get_scrob == 0:
            scrob = get_scrob + 1
        else:
            scrob =  get_scrob            
        listening = f"is listening for {scrob}th time"
    except KeyError:
        listening = "está ouvindo"
    if image_:
        img_ = download(image_, Config.DOWN_PATH)
    else:
        img_ = download(
            "https://telegra.ph/file/328131bd27e0cb8969b31.png", Config.DOWN_PATH)
    loved = int(song_["loved"])

    # User Photo
    if user_.photo:
        photos = message.from_user.photo.big_file_id
        pfp = await megux.download_media(photos)
    else:
        pfp = 'megumin/plugins/misc/pic.jpg'

    # background object
    canvas = Image.new("RGB", (600, 250), (18, 18, 18))
    draw = ImageDraw.Draw(canvas)

    # album art
    try:
        art_ori = Image.open(img_).convert("RGB")
        art = Image.open(img_).convert("RGB")
        enhancer = ImageEnhance.Brightness(art)
        im_ = enhancer.enhance(0.7)
        blur = im_.filter(ImageFilter.GaussianBlur(20))
        blur_ = blur.resize((600, 600))
        canvas.paste(blur_, (0, -250))
        # original art
        art_ori = art_ori.resize((200, 200), Image.ANTIALIAS)
        canvas.paste(art_ori, (25, 25))
    except Exception as ex:
        print(ex)

    # profile pic
    o_pfp = Image.open(pfp).convert("RGB")
    o_pfp = o_pfp.resize((52, 52), Image.ANTIALIAS)
    canvas.paste(o_pfp, (523, 25))

    # set font sizes
    open_sans = ImageFont.truetype(Fonts.OPEN_SANS, 21)

    # open_bold = ImageFont.truetype(Fonts.OPEN_BOLD, 23)
    poppins = ImageFont.truetype(Fonts.POPPINS, 25)
    arial = ImageFont.truetype(Fonts.ARIAL, 25)
    arial23 = ImageFont.truetype(Fonts.ARIAL, 21)

    # assign fonts
    songfont = poppins if checkUnicode(song_name) else arial
    artistfont = open_sans if checkUnicode(artist_name) else arial23

    # draw text on canvas
    white = '#ffffff'
    draw.text((248, 18), truncate(user_lastfm, poppins, 250),
              fill=white, font=poppins)
    draw.text((248, 53), listening,
              fill=white, font=open_sans)
    draw.text((248, 115), truncate(song_name, songfont, 315),
              fill=white, font=songfont)
    draw.text((248, 150), truncate(artist_name, artistfont, 315),
              fill=white, font=artistfont)

    # draw heart
    if loved:
        lov_ = Image.open("megumin/plugins/misc/heart.png", 'r')
        leve = lov_.resize((25, 25), Image.ANTIALIAS)
        canvas.paste(leve, (248, 190), mask=leve)
        draw.text((278, 187), truncate("loved", artistfont, 315),
                  fill=white, font=artistfont)

    # return canvas
    image = BytesIO()
    canvas.save(image, format="webp")
    image.seek(0)
    artists = artist_name.replace(" ", "+")
    songs = song_name.replace(" ", "+")
    prof = f"https://www.last.fm/user/{user_lastfm}"
    link_ = f"https://www.youtube.com/results?search_query={songs}+{artists}"
    button_ = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔎 Youtube", url=link_
                ),
                InlineKeyboardButton(
                    "👤 Profile", url=prof
                ),
            ]
        ]
    )
    # send pic
    await message.reply_photo(image, reply_markup=button_)

    os.remove(img_)
    os.remove(pfp)

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
