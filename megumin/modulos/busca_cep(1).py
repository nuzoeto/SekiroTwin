import io
import os
import re
import rapidjson
import httpx
import requests 

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import BadRequest

from megumin import megux

@megux.on_message(filters.command("cep"))
async def lastfm(c: megux, m: Message):
    try:
        cep = m.text.split(maxsplit=1)[1]
    except IndexError:
        await m.reply("CEP não inserido.")
        return

    base_url = "https://brasilapi.com.br/api/cep/v1"
    res = await requests.get(f"{base_url}/{cep}")
    city = res.json().get("city")
    state = res.json().get("state")
    states = await http.get(f"https://brasilapi.com.br/api/ibge/uf/v1/{state}")
    state_name = states.json().get("nome")
    neighborhood = res.json().get("neighborhood")
    street = res.json().get("street")

    if res.status_code == 404:
        await m.reply("cep invalido")
        return
    else:
        rep =  f"""🌏 <b>{cep}</b>\n<b>- Cidade:</b> {city}\n<b>- Estado:</b> {state_name} - {state}\n<b>- Bairro:</b> {neighborhood}\n<b>- Rua:</b> {street}"""
        await m.reply_text(rep)
