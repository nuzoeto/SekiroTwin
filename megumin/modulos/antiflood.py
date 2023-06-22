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
    if limit and "limit" in limit:
        chat_limit = int(limit["limit"])
    else:
        chat_limit = int(5)
    return chat_limit

async def time_flood(chat_id: int):
    time = await DB.find_one({"chat_id": chat_id})
    if time and "cooldown" in time:
        chat_time = int(limit["cooldown"])
    else:
        chat_time = int(10)
    return chat_time

async def check_flood_on(chat_id: int):
    if await DB.find_one({"chat_id": chat_id, "status": "on"}):
        return True
    else:
        return False


@megux.on_message(~filters.private & ~filters.bot & filters.all, group=11)
async def flood_control_func(_, message: Message):
    if message.sender_chat:
        return
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


async def check_flood(chat_id: int, user_id: int, chat_limit: int):
    current_time = datetime.now().time()
    cooldown = await time_flood(chat_id)

    user_info = await DB_.find_one({"chat_id": chat_id, "user_id": user_id})

    if not user_info:
        # Se o usuário não estiver no banco de dados, adiciona-o com as informações iniciais
        user_info = {
            "chat_id": chat_id,
            "user_id": user_id,
            "timestamp": current_time,
            "count": 1
        }
        await DB_.insert_one(user_info)
        return False

    last_message_time = user_info["timestamp"]
    elapsed_time = current_time - last_message_time

    if elapsed_time >= cooldown:
        # Se o tempo decorrido for maior ou igual ao intervalo de cooldown, reinicia as informações do usuário
        await DB_.update_one({"chat_id": chat_id, "user_id": user_id}, {"$set": {"timestamp": current_time, "count": 1}})
        return False

    message_count = user_info["count"]

    if message_count >= chat_limit:
        # Se o número de mensagens exceder o limite, é um flood
        await DB_.update_one({"chat_id": chat_id, "user_id": user_id}, {"$set": {"timestamp": current_time, "count": 1}})
        return True
    else:
        # Atualiza as informações do usuário no banco de dados
        await DB_.update_one({"chat_id": chat_id, "user_id": user_id}, {"$set": {"timestamp": current_time, "count": message_count + 1}})
        return False


