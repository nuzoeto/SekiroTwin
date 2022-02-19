import os
import random


from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

@megux.on_message(filters.regex(r"^Oi") & filters.private)
async def ola_oi_(c: megux, m: Message):
  await m.reply("Oi, tudo bom?")
  
  
@megux.on_message(filters.regex(r"^Olá") & filters.private)
async def ola_oi(c: megux, m: message):
 await m.reply("Olá! Tudo bem com você?")