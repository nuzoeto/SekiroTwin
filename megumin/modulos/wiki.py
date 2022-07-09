##BubbalooTeam contribute from WhiterKang


##module by DAVI

import wikipedia

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux, Config
from megumin.utils.decorators import input_str

@megux.on_command(filters.command("wikipt", Config.TRIGGER))
async def wikipt(c: megux, m: Message):
    query = input_str(m)
    if message.reply_to_message:
        query = message.reply_to_message.text 
    if not query:
        await m.reply("Ei! Você parado cade os argumentos? Você esqueceu.")
        return
    try:
        wikipedia.set_lang("pt")
        await m.reply("<b>Resultados da pesquisa no wikipedia:\n\n{}".format(wikipedia.summary(query, sentences=2)))
        
