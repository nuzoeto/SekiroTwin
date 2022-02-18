import random

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

@megux.on_message(filters.command(["warm"]))
async def printer(_, message: Message):
    warmf = random.choice(rep)
    await message.reply(f"{warmf}")

rep = [f"**<a href='tg://user?id={message.reply_to_message.from_user.id}'>{message.reply_to_message.from_user.first_name}</a> foi advertido!**\nEle(a) têm 1/3 Advertencias.",
f"**<a href='tg://user?id={message.reply_to_message.from_user.id}'>{message.reply_to_message.from_user.first_name}</a> foi advertido!**\nEle(a) têm 2/3 Advertencias.", 
f"**<a href='tg://user?id={message.reply_to_message.from_user.id}'>{message.reply_to_message.from_user.first_name}</a> foi advertido!**\nEle(a) têm 3/3 Advertencias **esta banido**" ]
