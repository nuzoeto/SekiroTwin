import asyncio
import datetime

from pyrogram import filters, enums
from pyrogram.types import Message, ChatPermissions

from megumin import megux
from megumin.utils import get_collection, is_admin

MSGS_CACHE = {}

DB = get_collection("ANTIFLOOD_CHATS")

async def check_flood(chat_id: int, user_id: int):
    if not MSGS_CACHE.get(chat_id) or MSGS_CACHE[chat_id]["user"] != user_id:
        MSGS_CACHE[chat_id] = {
            "user": user_id,
            "count": 1
        }
        return False
     
    #check_flood
    chat_flood = MSGS_CACHE[chat_id]
    count = chat_flood["count"]

    count += 1

    limit_pack  = await DB.find_one({"chat_id": chat_id}) 

    if limit_pack:
        limit = limit_pack["limit"]
    else: 
        limit = 5


    if count >=  limit:
        del MSGS_CACHE[chat_id]
        return True
    MSGS_CACHE[chat_id] = {"cur_user": user_id, "count": count}
    return False


@megux.on_message(filters.group & filters.incoming, group=10)
async def flood(c: megux, m: Message):

    if not m.from_user: #ignore_channels
        return

    if m.from_user.id == 777000: #ignore_telegram
        return

    chat_id = m.chat.id
    user_id = m.from_user.id

    if not await DB.find_one({"chat_id": chat_id, "status": "on"}):
        return

    if await is_admin(chat_id, user_id):
        if chat_id in MSGS_CACHE:
            del MSGS_CACHE[chat_id]
        return
    
    if check_flood(chat_id, user_id):
        await c.restrict_chat_member(chat_id, user_id, ChatPermissions())
        await m.reply("Você fala muito. Ficará mutado por flood ate um admin remover o mute!")
        return