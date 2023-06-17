import asyncio
import datetime

from pyrogram import filters, enums
from pyrogram.types import Message, ChatPermissions

from megumin import megux
from megumin.utils import get_collection, is_admin

MSGS_CACHE = {}

DB = get_collection("ANTIFLOOD_CHATS")
DB_ = get_collection("FLOOD_MSGS")


def reset_flood(chat_id, user_id=0):
    for user in MSGS_CACHE[chat_id].keys():
        if user != user_id:
            MSGS_CACHE[chat_id][user] = 0
            
async def flood_limit(chat_id: int):
    limit = await DB.find_one({"chat_id": chat_id})
    if limit:
        chat_limit = int(limit["limit"])
    else:
        chat_limit = int(5)
    return chat_limit

async def check_flood_on(chat_id: int):
    if await DB.find_one({"chat_id": chat_id, "status": "on"}):
        return True
    else:
        return False


@megux.on_message(~filters.service & ~filters.me & ~filters.private & ~filters.channel & ~filters.bot , group=10)
async def flood_control_func(_, message: Message):
    chat_id = message.chat.id
    if not await check_flood_on(chat_id):
        return
    chat_limit = await flood_limit(chat_id)
    




async def remove_old_messages(chat_id, user_id):
    current_time = datetime.utcnow()
    threshold = current_time - timedelta(seconds=10)
    chat_flood = await DB_.find_one({"chat_id": chat_id, "user_id": user_id})
    count = chat_flood["count"]
    await DB_.delete_many({"chat_id": chat_id, "user_id": user_id, "count": count, "time": {"$lt": threshold}})


async def check_flood(chat_id: int, user_id: int, chat_limit: int):
    time = datetime.utcnow()
    if not await DB_.find_one({"chat_id": chat_id}) or await DB_.find_one({"chat_id": chat_id, "user_id": user_id})
        await DB_.insert_one({"chat_id": chat_id, "user_id": user_id, "count": 1, "time": time})
        return False
    chat_flood = await DB_.find_one({"chat_id": chat_id, "user_id": user_id})
    count = chat_flood["count"]

    addcount += 1

    if count >= chat_limit:
        await DB_.delete_many({"chat_id": chat_id, "user_id": user_id, "count": count})
        return True
    await DB_.update_one({"chat_id": chat_id, "user_id": user_id, {"$set": {"count": addcount}}, "time": time})
    await remove_old_messages(chat_id, user_id):
    return False                    
