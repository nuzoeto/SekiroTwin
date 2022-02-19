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
  elif "Você não presta" in message.text:
    await message.reply("Mas eu presto pra muitas coisas. Não reparou no meu verniz?")
  elif "Robô ED" in message.text:
    await message.reply(f"{message.from_user.first_name} Robo Ed e meu amigo.")
  elif "Bom dia" in message.text:
    await message.reply("Bom dia! Como posso ajudar? Sobre o que quer conversar?")
  elif "Boa tarde" in message.text: 
    await message.reply("Boa tarde! Como posso ajudar? Sobre o que quer conversar?")
  elif "Boa noite" in message.text:
    await message.reply("Boa noite! Como posso ajudar? Sobre o que quer conversar?")
  elif "Nada" in message.text:
    await message.reply("Nada? Impossível.")
  elif "Não" in message.text:
    await message.reply("Eu ajudo a preservar energia conversando sobre o assunto, divulgando as metas do CONPET e passando [dicas de economia]("https://telegra.ph/Dicas-de-economia-02-19")!")
  else:
    return
