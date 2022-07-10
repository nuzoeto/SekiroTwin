##BubbalooTeam contribute from WhiterKang


##module by DAVI

import wikipedia
import re

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux, Config


@megux.on_message(filters.command("wikipt", Config.TRIGGER))
async def wikipt(c: megux, m: Message):
    if len(m.command) == 0:
        await m.reply("Ei! Você parado cade os argumentos? Você esqueceu.")
        return
    query = m.text
    if m.reply_to_message:
        query = m.reply_to_message.text 
    kueri = re.split(pattern="wikipt", string=query)
    try:
        wikipedia.set_lang("pt")
        await m.reply("<b>Resultados da pesquisa no wikipedia:\n\n{}".format(wikipedia.summary(kueri, sentences=2)))
    except wikipedia.PageError as e:
        return await m.reply("error: {}".format(e))
    except BadRequest as et:
        return await m.reply("error: {}".format(et))
        
