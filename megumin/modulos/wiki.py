##BubbalooTeam contribute from WhiterKang


##module by DAVI

import wikipedia
import re

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux, Config
from megumin.utils.decorators import input_str

@megux.on_message(filters.command("wikipt", Config.TRIGGER))
async def wikipt(c: megux, m: Message):
    query = input_str(m)
    if m.reply_to_message:
        query = m.reply_to_message.text 
    if not query:
        await m.reply("Ei! Você parado cade os argumentos? Você esqueceu.")
        return
    try:
        kueri = re.split(pattern="wikipt", string=query)
        wikipedia.set_lang("pt")
        await m.reply("<b>Resultados da pesquisa no wikipedia:\n\n{}".format(wikipedia.summary(kueri, sentences=2)))
    except wikipedia.PageError as e:
        return await m.reply("error: {}".format(e))
        
