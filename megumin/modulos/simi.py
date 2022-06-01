import requests 

from pyrogram import filters 
from pyrogram.types import Message

from megumin import megux 


@megux.on_message(filters.command("simi", prefixes=["/", "!"]))
async def chatbot_(c: megux, m: Message):
    try:
        text_ = m.text.split(maxsplit=1)[1]
        API = f"https://api.simsimi.net/v2/?text={text_}&lc=pt&cf=false"
        r = requests.get(API).json()
        if r["success"] in "Eu não resposta. Por favor me ensine.":
            await m.reply("Desconheço esse assunto, mas sei de outros: história, dicas..")
        else:
            if r["success"]: 
                await m.reply(r["success"])
