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


@megux.on_message(~filters.service & ~filters.me & ~filters.private & ~filters.channel & ~filters.bot , group=10)
async def flood_control_func(_, message: Message):
    if not message.chat:
        return
    limit = await DB.find_one({"chat_id": chat_id})
    chat_id = message.chat.id
    if not await DB.find_one({"chat_id": chat_id, "status": "on"}):
        return
    if limit:
        chat_limit = limit["limit"]
    else:
        chat_limit = 5
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
    if MSGS_CACHE[chat_id][user_id] >= :
        MSGS_CACHE[chat_id][user_id] = 0
        try:
            if is_admin(chat_id, user_id):
                return
            await message.chat.restrict_member(user_id,permissions=ChatPermissions(),until_date=int(time() + 5))
        except Exception:
            return
        await message.reply_text(f"Você fala muito. Ficara mutado por flood ate um admin remover o mute.")
    MSGS_CACHE[chat_id][user_id] += 1
    await asyncio.sleep(15)
    MSGS_CACHE[chat_id][user_id] = 0

