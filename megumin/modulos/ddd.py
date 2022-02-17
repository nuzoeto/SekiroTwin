import os
import httpx
import rapidjson

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import BadRequest

from megumin import megux

http = httpx.AsyncClient()


@megux.on_message(filters.command(["ddd"]))
async def lastfm(c: megux, m: Message):
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
    formated_cities = ", ".join(cities).lower() + "."

    rep = f"📞 <b>DDD - {ddd}</b> \n<b>- Estado:</b> {state_name} - {state}\n\n<b> Cidades:</b> <code>{cities}</code>"
    

    await m.reply_text(rep)
