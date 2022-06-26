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
    await m.stop_propagation()


@megux.on_message(filters.group & ~filters.bot, group=2)
async def blacklist_txt(c: megux, m: Message):
    BLACKLIST = get_collection(f"BLACKLIST {m.chat.id}")
    text = m.text.split()
    text_1 = await BLACKLIST.find_one({"m": text_1})
    if text_1:
        await text.delete() 
