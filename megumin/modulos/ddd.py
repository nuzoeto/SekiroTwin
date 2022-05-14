import os
import httpx
import rapidjson

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import BadRequest

from megumin import megux
from megumin.utils import get_collection 

http = httpx.AsyncClient()

DISABLED = get_collection("DISABLED")


@megux.on_message(filters.command(["ddd"], prefixes=["/", "!"]))
async def ddd(c: megux, m: Message):
    gid = m.chat.id 
    query = "ddd"
    off = await DISABLED.find_one({"_id": gid, "_cmd": query})
    if off:
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

    rep = f"📞 <b>DDD - {ddd}</b> \n<b>- Estado:</b> {state_name} - {state}\n\n<b>Cidades:</b> <code>{cidade}</code>"
    

    await m.reply_text(rep)
