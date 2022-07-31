from geopy.geocoders import Nominatim

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux, Config
from megumin.utils.decorators import input_str

@megux.on_message(filters.command("gps", Config.TRIGGER))
async def gps_(c: megux, m: Message):
    target_msg = m.reply_to_message or m
    text = input_str(m)
    input_ = f"{text}"
    msg = await target_msg.reply("<i>Procurando...</i>")
    geolocator = Nominatim(user_agent=f"WhiterKangBOT {target_msg.from_user.id}")
    geoloc = geolocator.geocode(input_)
    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        await megux.send_location(m.chat.id, lat, lon)
        await msg.delete()
    else:
        await msg.edit("Localização não encontrada!")
