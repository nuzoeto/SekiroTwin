from pyrogram import filters 
from pyrogram.types import Message 

from megumin import megux, Config
from megumin.utils import get_collection, get_string, check_rights, check_bot_rights
from megumin.utils.decorators import input_str 


@megux.on_message(filters.command("addblacklist", Config.TRIGGER))
async def addblacklist(c: megux, m: Message):
    BLACKLIST = get_collection(f"BLACKLIST {m.chat.id}")
    text_ = input_str(m).split()
    if text_:
        await BLACKLIST.insert_one({"m": text_})
        return await m.reply("success")
    elif m.reply_to_message.text:
        text_ = m.reply_to_message.text
        await BLACKLIST.insert_one({"m": text_})
        await m.reply("success")
        return
    elif m.reply_to_message.photo:
       photo = m.reply_to_message
       await BLACKLIST.insert_one({"m": photo})
       msg = await m.reply(photo)
       return await msg.edit("success")
