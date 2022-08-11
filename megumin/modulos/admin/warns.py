import uuid

from pyrogram import filters
from pyrogram.errors import PeerIdInvalid, UserIdInvalid, UsernameInvalid
from pyrogram.types import Message

from megumin import megux, Config
from megumin.utils import (
    admin_check,
    extract_time,
    check_bot_rights,
    check_rights,
    is_admin,
    is_dev,
    is_self,
    sed_sticker,
    get_collection,
    get_string,
)


@megux.on_message(filters.command("warn", Config.TRIGGER))
async def warn_users(_, message: Message):
    chat_id = message.chat.id
    if not await check_rights(chat_id, message.from_user.id, "can_restrict_members"):
        await message.reply(await get_string(chat_id, "NO_BAN_USER"))
        return
    cmd = len(message.text)
    replied = message.reply_to_message
    reason = ""
    if replied:
        id_ = replied.from_user.id
        if cmd > 5:
            _, reason = message.text.split(maxsplit=1)
    elif cmd > 5:
        _, args = message.text.split(maxsplit=1)
        if " " in args:
            id_, reason = args.split(" ", maxsplit=1)
        else:
            id_ = args
    else:
        await message.reply(await get_string(message.chat.id, "BANS_NOT_ESPECIFIED_USER"))
        return
    try:
        user = await megux.get_users(id_)
        user_id = user.id
        mention = user.mention
    except (UsernameInvalid, PeerIdInvalid, UserIdInvalid):
        await message.reply(
            await get_string(message.chat.id, "BANS_ID_INVALID")
        )
        return
    if await is_self(user_id):
        await message.reply(await get_string(chat_id, "BAN_MY_SELF"))
        await sed_sticker(message)
        return 
    if is_dev(user_id):
        await message.reply(await get_string(chat_id, "BAN_IN_DEV"))
        return
    if await is_admin(chat_id, user_id):
        await message.reply(await get_string(chat_id, "BAN_IN_ADMIN"))
        return
    if not await check_rights(chat_id, megux.me.id, "can_restrict_members"):
        await message.reply(await get_string(chat_id, "NO_BAN_BOT"))
        await sed_sticker(message)
        return
      
    DB_ACTION = get_collection(f"WARN_ACTION {message.chat.id}")
    DB_WARNS = get_collection(f"WARNS {message.chat.id}")
    DB_LIMIT = get_collection(f"WARN_LIMIT {message.chat.id}")
    
    if await DB_LIMIT.find_one():
        warns_limit = DB_LIMIT["limit"]
    else:
        warns_limit = 3
    
    if await DB_ACTION.find_one():
        warn_action = DB_ACTION["action"]
    else:
        warn_action = "ban"
        
    await DB_WARNS.insert_one({"user_id": user_id, "warn_id": str(uuid.uuid4()), "reason": reason or None})
    
    user_warns = await DB_WARNS.count_documents({"user_id": user_id})
    
    if user_warns >= warns_limit:
        if warn_action == "ban":
            await message.chat.ban_member(user_id)
            await message.reply(f"{user_warns}/{warns_limit} Advertências, {mention} Foi banido!")
        elif warn_action == "mute":
            await message.chat.restrict_member(user_id, ChatPermissions())
            await message.reply(f"{user_warns}/{warns_limit} Advertências, {mention} Foi mutado até que um admin remova o mute!")
        elif warn_action == "kick":
            await message.chat.ban_member(user_id)
            await message.chat.unban_member(user_id)
            await message.reply(f"{user_warns}/{warns_limit} Advertências, {mention} Foi kickado!")
        else:
            return
        await DB_WARNS.delete_many({"user_id": user_id})
    else:
        await message.reply(f"{mention} <b>foi advertido!</b>\nEle(a) têm {user_warns}/{warns_limit} Advertências.\n<b>Motivo:</b> {reason or None}")
        
        
@megux.on_message(filters.command("unwarn", Config.TRIGGER))
async def unwarn_users(_, message: Message):
    chat_id = message.chat.id
    if not await check_rights(chat_id, message.from_user.id, "can_restrict_members"):
        await message.reply(await get_string(chat_id, "NO_BAN_USER"))
        return
    cmd = len(message.text)
    replied = message.reply_to_message
    reason = ""
    if replied:
        id_ = replied.from_user.id
        if cmd > 7:
            _, reason = message.text.split(maxsplit=1)
    elif cmd > 7:
        _, args = message.text.split(maxsplit=1)
        if " " in args:
            id_, reason = args.split(" ", maxsplit=1)
        else:
            id_ = args
    else:
        await message.reply(await get_string(message.chat.id, "BANS_NOT_ESPECIFIED_USER"))
        return
    try:
        user = await megux.get_users(id_)
        user_id = user.id
        mention = user.mention
    except (UsernameInvalid, PeerIdInvalid, UserIdInvalid):
        await message.reply(
            await get_string(message.chat.id, "BANS_ID_INVALID")
        )
        return
    if await is_self(user_id):
        await message.reply(await get_string(chat_id, "BAN_MY_SELF"))
        await sed_sticker(message)
        return 
    if is_dev(user_id):
        await message.reply(await get_string(chat_id, "BAN_IN_DEV"))
        return
    if await is_admin(chat_id, user_id):
        await message.reply(await get_string(chat_id, "BAN_IN_ADMIN"))
        return
    if not await check_rights(chat_id, megux.me.id, "can_restrict_members"):
        await message.reply(await get_string(chat_id, "NO_BAN_BOT"))
        await sed_sticker(message)
        return
    DB_WARNS = get_collection(f"WARNS {message.chat.id}")
    #delete one warn--user
    if await DB_WARNS.find_one({"user_id": user_id}):
        await DB_WARNS.delete_one({"user_id": user_id})
        await message.reply("A última advertencia foi removida!")
    else:
        await message.reply("Este usuário não tem nenhuma advertencia!")
        
        
@megux.on_message(filters.command("setwarnslimit", Config.TRIGGER))
async def set_warns_limit(_, message: Message):
    args = message.text
    if args:
        if args[0].isdigit():
            if int(args[0]) < 3:
                await message.reply("<i>O limite minimo de advertências é 3</i>")
            elif int(args[0]) > 10:
                await message.reply("<i>O limite maximo de advertências é 10</b>")
            else:
                DB = get_collection(f"WARN_LIMIT {message.chat.id}")
                await DB.insert_one({"limit": int(args[0])})
                await message.reply("Limite de advertências foi alterado para {}".format(args[0]))
        else:
            await message.reply("Esse limite é invalido!")
    else:
        await message.reply("Eu preciso de um argumento!")
