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
    data = get_collection(f"WELCOME {m.chat.id}")
    text_ = ""
    if input_str(m):
        text_ += m.text.split(None, 1)[1]
    if m.reply_to_message: 
        text_ += m.reply_to_message.text
    if text_ in "":
        return await m.reply("Responda uma mensagem ou de algum argumento após o comando!")
    else:
        if await check_rights(m.chat.id, m.from_user.id, "can_change_info"):
            await data.drop()
            await data.insert_one({"_welcome": text_})
            await m.reply("<i>Boas vindas definidas com sucesso!!</i>")



@megux.on_message(filters.new_chat_members & filters.group)
async def welcome(c: megux, m: Message):
    members = m.new_chat_members
    first_name = ", ".join(map(lambda a: a.first_name, members))
    chat_title = m.chat.title
    full_name = ", ".join(
        map(lambda a: a.first_name + " " + (a.last_name or ""), members)
    )
    user_id = ", ".join(map(lambda a: str(a.id), members))
    username = ", ".join(
        map(lambda a: "@" + a.username if a.username else a.mention, members)
    )
    count = await c.get_chat_members_count(m.chat.id)
    mention = ", ".join(map(lambda a: a.mention, members))
    data_msg = get_collection(f"WELCOME {m.chat.id}")
    data = await data_msg.find_one()
    if data:
        msg = data["_welcome"]
        welcome = msg.format(first=first_name, mention=mention, count=count)
        await m.reply(welcome)
    else:
        return await m.reply(f"Olá {mention} Seja bem vindo ao chat {chat_title}")

    
