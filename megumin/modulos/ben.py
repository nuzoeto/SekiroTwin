import asyncio
import os
import random
import re
import requests
import wget
import datetime

from pyrogram import filters

from megumin import megux

@megux.on_message(filters.command(["bun"], prefixes=["/", "!"]))
async def get_stats(_, message):
    if not message.reply_to_message:
    await m.reply("Você precisará responder a alguém para ser banido com fakeban.")
    else:
    sent = await message.reply("```Banindo usuario...```")
    await asyncio.sleep(1.1)
    await sent.edit(f"Usuário <a href='tg://user?id={message.reply_to_message.from_user.id}'>{message.reply_to_message.from_user.first_name}</a> foi banido por <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> no chat: **{message.chat.title}**")
