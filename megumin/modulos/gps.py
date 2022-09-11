from geopy.geocoders import Nominatim

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from megumin import megux, Config
from megumin.utils.decorators import input_str
from megumin.utils import is_disabled, disableable_dec

@megux.on_message(filters.command("gps", Config.TRIGGER))
@disableable_dec("gps")
async def gps_(c: megux, m: Message):
    if await is_disabled(m.chat.id, "gps"):
        return
    target_msg = m.reply_to_message or m
    text = input_str(m)
    input_ = f"{text}"
    msg = await target_msg.reply("<i>Procurando...</i>")
    geolocator = Nominatim(user_agent=f"WhiterKangBOT {target_msg.from_user.id}")
    geoloc = geolocator.geocode(input_)
    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        keyboard = [[InlineKeyboardButton(text="🌎 Abrir no Google Maps", url=f"https://www.google.com/maps/search/{lat},{lon}")]]
        await megux.send_location(m.chat.id, lat, lon, reply_markup=InlineKeyboardMarkup(keyboard))
        await msg.delete()
    else:
        await msg.edit("Localização não encontrada!")
