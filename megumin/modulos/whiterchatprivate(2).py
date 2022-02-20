import os
import random


from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

@megux.on_message(filters.private)
async def chatbot_(c: megux, message: Message):
  if "Oi" in message.text or "oi" in message.text:
    await message.reply("Oi, como vai você?")
  elif "Olá" in message.text or "olá" in message.text:
    await message.reply("Olá! Como vai você?")
  elif "Você não presta" in message.text or "você não presta" in message.text:
    await message.reply("Mas eu presto pra muitas coisas. Não reparou no meu verniz?")
  elif "Robô ED" in message.text or "robô ed" in message.text or "robô ED" in message.text:
    await message.reply(f"{message.from_user.first_name} Robo Ed e meu amigo.")
  elif "Bom dia" in message.text or "bom dia" in message.text:
    await message.reply("Bom dia! Como posso ajudar? Sobre o que quer conversar?")
  elif "Boa tarde" in message.text or "boa tarde" in message.text: 
    await message.reply("Boa tarde! Como posso ajudar? Sobre o que quer conversar?")
  elif "Boa noite" in message.text or "boa noite" in message.text:
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
  elif "Nossa" in message.text:
    await message.reply("Nossa mesmo...")  
  elif "Vai cagar" in message.text:
    await message.reply("Esse jeito de se expressar é falta de assunto? Ou você costuma ser grosseiro sempre?")
  elif "Está on" in message.text:
    await message.reply(f"Sim estou onfire!\n\n**💻 Meu sistema é**: `Android, Linux 4.4.0-1098-aws`\n**➕ Python**: `3.9.10`")
  elif "Hmm" in message.text:
    await message.reply("Hm, sei não.")
  elif "Geografia" in message.text:
    await message.reply("Gosto muito de geografia. Estudando geografia aprendi qual o oceano mais profundo, o que é fuso horário, jusante, enseada, planalto, planície, camada sedimentar e mais uma porção de coisas.")
  elif "Geográfico" in message.text:
    await message.reply("Estudar geografia é bem legal. Desde seu nascimento aos mais modernos ramos, passando por relevo, camada sedimentar, oasis, fuso horário... E aprendi ainda as diferenças entre geografia e geologia, planalto e planície, mar e oceano, jusante e montante.")
  elif "Google" in message.text:
    await message.reply("Que tipo de informação você costuma procurar em sites de busca?")
  elif "Opa" in message.text:
    await message.reply("Opa opa! Beleza!")
  elif "Piracicaba" in message.text:
    await message.reply("Piracicaba-SP é uma bela cidade, um importante polo de desenvolvimento industrial e agrícola. Me disseram que Piracicaba, na língua tupi, significa lugar onde o peixe chega.")
  elif "Salvador" in message.text:
    await message.reply("Conheço 3 lugares que se chamam Salvador: a capital da Bahia (São Salvador da Bahia de Todos os Santos!), El Salvador (um pequeno país da América Central) e sua capital, San Salvador.")
  elif "Ping" in message.text:
    await message.reply("Ping... Pong.")
  elif "América" in message.text:
    await message.reply("América do Sul e América do Norte fazem parte do continente Americano, também conhecido como Novo Mundo. Os estudiosos dizem que o continente recebeu este nome em homenagem ao navegador Américo Vespúcio.")
  elif "Youtube" in message.text:
    await message.reply("O que você costuma buscar no youtube?")
  elif "Bomba" in message.text:
    await message.reply("Que tipo de bomba?")
  elif "Davi" in message.text:
    await message.reply("Davi significa predileto, amado e respeitado, em hebraico.")
  elif "Kkk" in message.text:
    await message.reply("KKKK.")
  elif "Haha" in message.text:
    await message.reply("Hahaha.")
  elif "Americana" in message.text:
    await message.reply("Americana... é uma cidade perto de Campinas!")
  else:
    return
