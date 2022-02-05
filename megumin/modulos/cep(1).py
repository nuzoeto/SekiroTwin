import requests

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

@megux.on_message(filters.command(["cota"]))
async def pegar_cotacoes(_, message):
    try:
        cep = m.text.split(maxsplit=1)[1]

    requisicao = http.get("https://brasilapi.com.br/api/cep/v1")

    base_url = requisicao.json()
    res = await http.get(f"{base_url}/{cep}")
    city = res.json().get("city")
    state = res.json().get("state")

    result = f'''
Cidade: {city} outros {state}
'''

    await message.reply_photo(photo="https://telegra.ph/file/d60e879db1cdba793a98c.jpg",
    caption=result)
