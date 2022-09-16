import asyncio
import datetime

from pyrogram import filters, enums
from pyrogram.types import Message, ChatPermissions

from megumin import megux
from megumin.utils import get_collection, is_admin

MSGS_CACHE = {}

DB = get_collection("ANTIFLOOD_CHATS")
DB_ = get_collection("STATUS_FLOOD_MSGS")


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
    if not message.chat:
        return
    chat_id = message.chat.id
    if not await check_flood_on(chat_id):
        return
    chat_limit = await flood_limit(chat_id)
    if chat_id not in MSGS_CACHE:
        MSGS_CACHE[chat_id] = {}
    if not message.from_user:
        reset_flood(chat_id)
        return
    user_id = message.from_user.id
    mention = message.from_user.mention
    if user_id not in MSGS_CACHE[chat_id]:
        MSGS_CACHE[chat_id][user_id] = 0
    reset_flood(chat_id, user_id)
    if MSGS_CACHE[chat_id][user_id] >= chat_limit:
        MSGS_CACHE[chat_id][user_id] = 0
        try:
            if is_admin(chat_id, user_id):
                return
            await message.chat.restrict_member(user_id, ChatPermissions())
        except Exception:
            return await messge.reply("Você fala muito por favor fale menos")
        await message.reply_text(f"Você fala muito. Ficara mutado por flood ate um admin remover o mute.")
    MSGS_CACHE[chat_id][user_id] += 1
    await asyncio.sleep(15)
    MSGS_CACHE[chat_id][user_id] = 0

