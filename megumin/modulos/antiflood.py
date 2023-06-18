import asyncio

from pyrogram import filters, enums
from pyrogram.types import Message, ChatPermissions

from datetime import datetime, timedelta


from megumin import megux
from megumin.utils import get_collection, is_admin


DB = get_collection("ANTIFLOOD_CHATS")
DB_ = get_collection("FLOOD_MSGS")

      
async def flood_limit(chat_id: int):
    limit = await DB.find_one({"chat_id": chat_id})
    if limit["limit"]:
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
    if not message.from_user:
        return 
    chat_id = message.chat.id
    user_id = message.from_user.id
    if user_id == 777000:  # ignore telegram
        return 
    if await is_admin(chat_id, user_id): # ignore admins
        return 
    if not await check_flood_on(chat_id):
        return
    chat_limit = await flood_limit(chat_id)
    should_mute = await check_flood(chat_id, user_id, chat_limit)
    if should_mute:
        try:
            await message.chat.restrict_member(user_id, ChatPermissions())
            await message.reply_text(f"Você fala muito. Ficara mutado por flood ate um admin remover o mute.")
            return
        except Exception:
            return await message.reply("Você fala muito por favor fale menos")


async def remove_old_messages(chat_id: int, user_id: int):
    current_time = datetime.utcnow()
    threshold = current_time - timedelta(seconds=10)
    chat_flood = await DB_.find_one({"chat_id": chat_id, "user_id": user_id})
    count = chat_flood["count"]
    await DB_.delete_many({"chat_id": chat_id, "user_id": user_id, "time": {"$lt": threshold}})


async def check_flood(chat_id: int, user_id: int, chat_limit: int):
    time = datetime.utcnow()
    if not await DB_.find_one({"chat_id": chat_id}) and await DB_.find_one({"chat_id": chat_id, "user_id": user_id}):
        await DB_.insert_one({"chat_id": chat_id, "user_id": user_id, "time": time})
        return False
    count = await DB_.count_documents({"chat_id": chat_id, "user_id": user_id})

    if count >= chat_limit:
        await DB_.delete_many({"chat_id": chat_id, "user_id": user_id})
        return True
    await DB_.insert_one({"chat_id": chat_id, "user_id": user_id, "time": time})
    await remove_old_messages(chat_id, user_id)
    return False                    
