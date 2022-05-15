import io
import os
import re
import rapidjson
import httpx

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import BadRequest

from megumin import megux
from megumin.utils import get_collection 

http = httpx.AsyncClient()

DISABLED = get_collection(f"DISABLED {Message.chat.id}")

@megux.on_message(filters.command("cep", prefixes=["/", "!"]))
async def cep(c: megux, m: Message):
    gid = m.chat.id 
    query = "cep"
    off = await DISABLED.find_one({"_id": gid, "_cmd": query})
    if off:
        return
    try:
        cep = m.text.split(maxsplit=1)[1]
    except IndexError:
        await m.reply("CEP não inserido. **Uso do comando**: /cep (cep)")
        return

    base_url = "https://brasilapi.com.br/api/cep/v1"
    res = await http.get(f"{base_url}/{cep}")
    city = res.json().get("city")
    state = res.json().get("state")
    states = await http.get(f"https://brasilapi.com.br/api/ibge/uf/v1/{state}")
    state_name = states.json().get("nome")
    neighborhood = res.json().get("neighborhood")
    street = res.json().get("street")

    if res.status_code == 404:
        await m.reply("Este CEP é invalido.")
        return
    else:
        rep =  f"""🌏 <b>{cep}</b>\n<b>- Cidade:</b> {city}\n<b>- Estado:</b> {state_name} - {state}\n<b>- Bairro:</b> {neighborhood}\n<b>- Rua:</b> {street}"""
        await m.reply_text(rep)
