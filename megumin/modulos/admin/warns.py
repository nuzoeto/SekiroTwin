import uuid

from pyrogram import filters
from pyrogram.errors import PeerIdInvalid, UserIdInvalid, UsernameInvalid
from pyrogram.types import ChatPermissions, Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

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
    unwarn_bnt,
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
        LIMIT = await DB_LIMIT.find_one()
        warns_limit = LIMIT["limit"]
    else:
        warns_limit = 3
    
    if await DB_ACTION.find_one():
        ACTION = await DB_ACTION.find_one()
        warn_action = ACTION["action"]
    else:
        warn_action = "ban"
        
    await DB_WARNS.insert_one({"user_id": user_id, "warn_id": str(uuid.uuid4()), "reason": reason or None})
    
    user_warns = await DB_WARNS.count_documents({"user_id": user_id})
    
    if user_warns >= warns_limit:
        if warn_action == "ban":
            await message.chat.ban_member(user_id)
            await message.reply((await get_string(chat_id, "WARNS_BANNED")).format(user_warns, warns_limit, mention))
        elif warn_action == "mute":
            await message.chat.restrict_member(user_id, ChatPermissions())
            await message.reply((await get_string(chat_id, "WARNS_MUTED")).format(user_warns, warns_limit, mention))
        elif warn_action == "kick":
            await message.chat.ban_member(user_id)
            await message.chat.unban_member(user_id)
            await message.reply((await get_string(chat_id, "WARNS_KICKED")).format(user_warns, warns_limit, mention))
        else:
            return
        await DB_WARNS.delete_many({"user_id": user_id})
    else:
        keyboard = [[InlineKeyboardButton(await get_string(chat_id, "RULES_WARN_BNT"), callback_data=f"rules|{user_id}"), InlineKeyboardButton(await get_string(chat_id, "UNWARN_BNT"), callback_data=f"rm_warn|{user_id}")]]
        await message.reply((await get_string(chat_id, "USER_WARNED")).format(mention, user_warns, warns_limit, reason or None), reply_markup=InlineKeyboardMarkup(keyboard))
        
        
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
        await message.reply(await get_string(chat_id, "UNWARNED"))
    else:
        await message.reply(await get_string(chat_id, "USER_NOT_WARNS"))
        
        
@megux.on_message(filters.command("setwarnslimit", Config.TRIGGER))
async def set_warns_limit(_, message: Message):
    if not await check_rights(message.chat.id, message.from_user.id, "can_change_info"):
        return
    if len(message.command) == 1:
        await message.reply("Você precisa dar um argumento.")
        return
    try:
        warns_limit = int(message.command[1])
    except ValueError:
        return await message.reply("Esse limite não é valido.")
    DB = get_collection(f"WARN_LIMIT {message.chat.id}")
    await DB.drop()
    await DB.insert_one({"limit": warns_limit})
    await message.reply(f"<i>O limite de advertências foi alterado para {warns_limit}</i>")

    
@megux.on_message(filters.command(["setwarnmode", "setwarnaction"], Config.TRIGGER))
async def set_warns_limit(_, message: Message):
    if not await check_rights(message.chat.id, message.from_user.id, "can_change_info"):
        return
    DB = get_collection(f"WARN_ACTION {message.chat.id}")   
    if len(message.text.split()) > 1:
        if not message.command[1] in ("ban", "mute", "kick"):
            return await message.reply_text("Esse argumento não é valido.")

        warn_action_txt = message.command[1]
        
            
        await DB.drop()
        await DB.insert_one({"action": warn_action_txt})
       
        await message.reply_text(
        f"A ação de advertências do chat foi alterado para: {warn_action_txt}"
    )
    else:
        if await DB.find_one():
            r = await DB.find_one()
            warn_act = r["action"]
        else:
            warn_act = "ban"
        await message.reply_text("A ação atual de advertências é: {action}".format(action=warn_act))
        

@megux.on_message(filters.command("warns", Config.TRIGGER))
async def warns_from_users(_, message: Message):
    chat_id = message.chat.id
    if not await check_rights(chat_id, message.from_user.id, "can_restrict_members"):
        await message.reply(await get_string(chat_id, "NO_BAN_USER"))
        return
    cmd = len(message.text)
    replied = message.reply_to_message
    reason = ""
    if replied:
        id_ = replied.from_user.id
        if cmd > 6:
            _, reason = message.text.split(maxsplit=1)
    elif cmd > 6:
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
    
    if not await check_rights(chat_id, megux.me.id, "can_restrict_members"):
        await message.reply(await get_string(chat_id, "NO_BAN_BOT"))
        await sed_sticker(message)
        return
      
    DB_WARNS = get_collection(f"WARNS {message.chat.id}")
    DB_LIMIT = get_collection(f"WARN_LIMIT {message.chat.id}")
    
    if not await DB_WARNS.find_one({"user_id": user_id}):
        return await message.reply((await get_string(chat_id, "ATT_USER_NO_WARNS")).format(mention))
    
    if await DB_LIMIT.find_one():
        res = await DB_LIMIT.find_one()
        warns_limit = res["limit"]
    else:
        warns_limit = 3
        
    user_warns = await DB_WARNS.count_documents({"user_id": user_id})
    
    await message.reply((await get_string(chat_id, "ATT_USER_WARNS")).format(mention, user_warns, warns_limit))

    
@megux.on_callback_query(filters.regex(pattern=r"^rules\|(.*)"))
async def warn_rules(client: megux, cb: CallbackQuery):
    try:
        data, userid = cb.data.split("|")
    except ValueError:
        return print(cb.data)
    if cb.from_user.id != int(userid):
        await cb.answer(await get_string(cb.message.chat.id, "NO_RULES_WARN_YOU"), show_alert=True)
        return
    chat_id = cb.message.chat.id
    DB = get_collection(f"RULES {chat_id}")
    resp = await DB.find_one()
    if resp:
        RULES = resp["_rules"]
        text = (await get_string(chat_id, "RULES")).format(m.chat.title, RULES)
    else:
        text = await get_string(chat_id, "NO_RULES")
    await cb.edit_message_text(text=text, disable_web_page_preview=True)

    
@megux.on_callback_query(filters.regex(pattern=r"^rm_warn\|(.*)"))
async def unwarn(client: megux, cb: CallbackQuery):
    data, id_ = cb.data.split("|")
    chat_id = cb.message.chat.id
    mention_ = cb.from_user.mention
    uid = cb.from_user.id
    if not await check_rights(chat_id, uid, "can_restrict_members"):
        return await cb.answer(await get_string(chat_id, "NO_BAN_USER"), show_alert=True)
    try:
        user = await megux.get_users(id_)
        user_id = user.id
        mention = user.mention
    except (UsernameInvalid, PeerIdInvalid, UserIdInvalid):
        await message.reply(
            await get_string(message.chat.id, "BANS_ID_INVALID")
        )
    await unwarn_bnt(chat_id, user_id)
    #send as message
    await cb.edit_message_text(text=(await get_string(chat_id, "UNWARNED_CALLBACKQUERY")).format(mention, mention_), disable_web_page_preview=True)
    
