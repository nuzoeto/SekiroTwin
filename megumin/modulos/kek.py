import os

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import BadRequest

from megumin import megux


@megux.on_message(filters.command(["kek"]))
async def lastfm(c: megux, m: Message):
    try:
         kek = m.text.split(maxsplit=1)[1]
    except IndexError:
        await m.reply_text("__Kek..__")
        return

 rep = f"__{kek}__"


        await message.reply(rep)
