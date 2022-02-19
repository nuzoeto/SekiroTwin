import os
import random


from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

@megux.on_message(filters.private)
async def chatbot_(c: megux, message: Message):
  if "Oi" in message.text:
    await message.reply("Oi, tudo bom?")
  elif "Olá" in message.text:
    await message.reply("Olá! Como vai você?")
  else:
    return
