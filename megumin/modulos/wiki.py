##BubbalooTeam contribute from WhiterKang


##module by DAVI

import wikipedia
import re

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from megumin import megux, Config
from megumin.utils import tld 
from megumin.utils.decorators import input_str 


@megux.on_message(filters.command("wikipt", Config.TRIGGER))
async def wikipt(c: megux, m: Message):
    if not input_str(m):
        await m.reply("Ei! Você parado cade os argumentos? Você esqueceu.")
        return
    query = m.text 
    kueri = re.split(pattern="wikipt", string=query)
    try:
        wikipedia.set_lang("pt")
        keyboard = [[InlineKeyboardButton(text=await tld(m.chat.id, "MOREINFO_BNT"), url=wikipedia.page(kueri).url)]]
        await m.reply((await tld(m.chat.id, "WIKI_RESULT")).format(wikipedia.summary(kueri, sentences=2)), reply_markup=InlineKeyboardMarkup(keyboard))
    except wikipedia.PageError as e:
        return await m.reply("error: {}".format(e))
    except BadRequest as et:
        return await m.reply("error: {}".format(et))
    except wikipedia.exceptions.DesambiguationError as eet:
        return await m.reply("⚠ Error\n Há muitas coisa! Expresse melhor para achar o resultado!\nPossíveis resultados da consulta:\n{}".format(eet))
 
       
@megux.on_message(filters.command("wikien", Config.TRIGGER))
async def wikipt(c: megux, m: Message):
    if not input_str(m):
        await m.reply("Ei! Você parado cade os argumentos? Você esqueceu.")
        return
    query = m.text 
    kueri = re.split(pattern="wikien", string=query)
    try:
        wikipedia.set_lang("en")
        keyboard = [[InlineKeyboardButton(text=await tld(m.chat.id, "MOREINFO_BNT"), url=wikipedia.page(kueri).url)]]
        await m.reply((await tld(m.chat.id, "WIKI_RESULT")).format(wikipedia.summary(kueri, sentences=3)), reply_markup=InlineKeyboardMarkup(keyboard))
    except wikipedia.PageError as e:
        return await m.reply("error: {}".format(e))
    except BadRequest as et:
        return await m.reply("error: {}".format(et))
    except wikipedia.exceptions.DesambiguationError as eet:
        return await m.reply("⚠ Error\n Há muitas coisa! Expresse melhor para achar o resultado!\nPossíveis resultados da consulta:\n{}".format(eet))
  
      
@megux.on_message(filters.command("wikies", Config.TRIGGER))
async def wikipt(c: megux, m: Message):
    if not input_str(m):
        await m.reply("Ei! Você parado cade os argumentos? Você esqueceu.")
        return
    query = m.text 
    kueri = re.split(pattern="wikies", string=query)
    try:
        wikipedia.set_lang("es")
        keyboard = [[InlineKeyboardButton(text=await tld(m.chat.id, "MOREINFO_BNT"), url=wikipedia.page(kueri).url)]]
        await m.reply((await tld(m.chat.id, "WIKI_RESULT")).format(wikipedia.summary(kueri, sentences=4)), reply_markup=InlineKeyboardMarkup(keyboard))
    except wikipedia.PageError as e:
        return await m.reply("error: {}".format(e))
    except BadRequest as et:
        return await m.reply("error: {}".format(et))
    except wikipedia.exceptions.DesambiguationError as eet:
        return await m.reply("⚠ Error\n Há muitas coisa! Expresse melhor para achar o resultado!\nPossíveis resultados da consulta:\n{}".format(eet))
        
