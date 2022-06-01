from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from megumin import megux, Config 
from megumin.utils import get_collection, get_string 


@megux.on_message(filters.command("rules", Config.TRIGGER))
async def rules_(_, m: Message):
    data = get_collection(f"RULES {m.chat.id}")
    res = await data.find_one()
    if res:
        RULES = res["_rules"]
        await m.reply((await get_string(m.chat.id, "RULES")).format(m.chat.title, RULES))
    else:
         await m.reply(await get_string(m.chat.id, "NO_RULES"))
  
