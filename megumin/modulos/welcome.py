import asyncio
import inspect
import math
import os.path
import re

from string import Formatter
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.errors import BadRequest
from pyrogram.types import InlineKeyboardMarkup, Message

from megumin import megux, Config 
from megumin.utils import get_collection, get_string, check_rights  
from megumin.utils.decorators import input_str 


@megux.on_message(filters.command("setwelcome", Config.TRIGGER))
async def set_welcome(c: megux, m: Message):
    data = get_collection("WELCOME {m.chat.id}")
    text_ = ""
    if input_str(m):
        text_ = m.text.split(None, 1)[1]
    if m.reply_to_message: 
        text_ = message.reply_to_message.text
    if text_ in "":
        return await m.reply("Responda uma mensagem ou de algum argumento após o comando!")
    else:
        if await check_rights(m.chat.id, m.from_user.id, "can_change_info"):
            await data.drop()
            await data.insert_one({"_welcome": text_})
            await m.reply("Boas vidas definidas com sucesso")


    
