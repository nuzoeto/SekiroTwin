import asyncio
import datetime

from pyrogram import filters, enums
from pyrogram.types import Message

from megumin import megux
from megumin.utils import get_collection

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