import os
import httpx
import rapidjson

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import BadRequest

from megumin import megux
from megumin.utils import get_collection, get_string, is_disabled, disableable_dec 

http = httpx.AsyncClient()



@megux.on_message(filters.command(["ddd"], prefixes=["/", "!"]))
@disableable_dec("ddd")
async def ddd(c: megux, m: Message):
    if await is_disabled(m.chat.id, "ddd"):
        return
    try:
         ddd = m.text.split(maxsplit=1)[1]
    except IndexError:
        await m.reply_text("**Você esqueceu do DDD.**\n<b>Uso do comando:</b> /ddd (ddd).")
        return

    base_url = "https://brasilapi.com.br/api/ddd/v1"
    res = await http.get(f"{base_url}/{ddd}")
    state = res.json().get("state")
    states = await http.get(f"https://brasilapi.com.br/api/ibge/uf/v1/{state}")
    state_name = states.json().get("nome")
    cities = res.json().get("cities")
    cidade = ", ".join(cities).lower().title() + "."

    rep = await get_string(m.chat.id, "DDD_RESULT")
    

    await m.reply_text(rep.format(ddd, state_name, state, cidade))
