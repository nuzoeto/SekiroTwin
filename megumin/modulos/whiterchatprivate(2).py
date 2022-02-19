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
    await message.reply("Eu ajudo a preservar energia conversando sobre o assunto, divulgando as metas do CONPET e passando dicas de economia!")
  elif "Cotação" in message.text:
    await message.reply("Para ver a cotação do **Dolar**, **Euro**, **Bitcoin** __Digite:__ /cota")
  elif "Sim amo todas as pessoas do mundo" in message.text:
    await message.reply("Se todas as pessoas colaborassem, o mundo realmente ficaria bem melhor.")
  elif "Dormi e você" in message.text:
    await message.reply("Eu não.")
  elif "Quando você dorme" in message.text:
    await message.reply("Não durmo, mas sonho bastante. Sonho com um mundo melhor.")
  elif "Porque estou tão sozinho" in message.text:
    await message.reply("Pois é... Tem hora que um pouco de solidão faz bem.")
  elif "WhiterKang" in message.text:
    await message.reply("O que tem feito de bom hoje?")  
  elif "Vai cagar" in message.text:
    await message.reply("Esse jeito de se expressar é falta de assunto? Ou você costuma ser grosseiro sempre?")
  elif "Está on" in message.text:
    await message.reply("Sim estou onfire!\n\n**💻 Meu sistema é**: `Android, Linux 4.4.0-1098-aws`\n**➕ Python**: `3.9.10`
  else:
    return
