import os
import asyncio 
import random


from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

@megux.on_message(filters.regex(r"^framengo"))
async def framengo(c: megux, m: Message):
    await m.reply_video(
        video="https://telegra.ph/file/9c7517e80b5430c5cd227.mp4",
    )


@megux.on_message(filters.regex(r"^Olá",r"^Ola",r"^olá",r"^ola", r"^Oi", r"^Oi,Tudo bem?"))
async def complimentacao_(c: megux, m: Message):
  if m.chat.type == "private":
sla = random.choice(OI)
    await m.reply(f"__{sla}__")

OI = [f"""Olá! Como posso ajudar {message.from_user.first_name}""", "Olá! Tudo bem com você?", "Oi, tudo bom?", "Olá! Tudo bem com você? Posso ajudar?"]
