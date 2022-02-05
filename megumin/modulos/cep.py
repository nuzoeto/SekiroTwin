import os
import re
import httpx
import datetime
import rapidjson

@Client.on_message(filters.command(["cep"]))
async def lastfm(c: Client, m: Message):
    try:
        cep = m.text.split(maxsplit=1)[1]
    except IndexError:
        await message.reply("CEP NÃO INSERIDO!")
        return

    base_url = "https://brasilapi.com.br/api/cep/v1"
    res = await http.get(f"{base_url}/{cep}")
    city = res.json().get("city")
    state = res.json().get("state")
    states = await http.get(f"https://brasilapi.com.br/api/ibge/uf/v1/{state}")
    state_name = states.json().get("nome")
    neighborhood = res.json().get("neighborhood")
    street = res.json().get("street")

        await message.reply(f"""🌏 <b>{cep}</b>\n<b>- Cidade:</b> {city}\n<b>- Estado:</b>  - \n<b>- Bairro:</b> \n<b>- Rua:</b>""")
        
