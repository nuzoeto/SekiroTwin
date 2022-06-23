from pyrogram import filters 
from pyrogram.enums import ChatType
from pyrogram.types import Message, ChatPermissions

from megumin import megux, Config
from megumin.utils import get_collection, check_rights, is_admin, is_self, admin_check, check_bot_rights   
from megumin.utils.decorators import input_str 


ACTION = [
    "ban",
    "mute",
    "kick",
]

NUMBER = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
]



@megux.on_message(filters.command("setwarnlimit", Config.TRIGGER))
async def setwarnlimit_cmd(_, m: Message):
    LIMIT = get_collection(f"WARNS_LIMIT {m.chat.id}")
    chat_id = m.chat.id 
    check_admin = m.from_user.id  
    query = input_str(m)
    if m.chat.type == ChatType.PRIVATE:
        return await m.reply("Esse comando é para ser usado em grupos.")
    else:
        if not query in NUMBER:
            return await m.reply("__Especifique um número de advertências valido, de 1 a 7.__")
        else:
            found = await LIMIT.find_one()
            if found:
                if await check_rights(chat_id, check_admin, "can_change_info"):
                    await LIMIT.drop()
                    await LIMIT.insert_one({"_warnslimit": query})
                    await m.reply(f" O número de advertência foi alterado para **{query}**")
                else:
                    return await m.reply("`Você precisa de permissão para fazer isso.`")
            else:
                if await check_rights(chat_id, check_admin, "can_change_info"):
                    await LIMIT.drop()
                    await LIMIT.insert_one({"_warnslimit": query})
                    await m.reply(f"O número de advertência foi alterado para **{query}**")
                else: 
                    return await m.reply("`Você precisa de permissão para fazer isso`")


@megux.on_message(filters.command("setwarnmode", Config.TRIGGER))
async def setwarnaction_cmd(_, m: Message):
    CHAT_ACTION = get_collection(f"ACTION {m.chat.id}")
    chat_id = m.chat.id 
    check_admin = m.from_user.id  
    query = input_str(m)
    if m.chat.type == ChatType.PRIVATE:
        return await m.reply("Esse comando é para ser usado em grupos.")
    else:
        if not query in ACTION:
            return await m.reply("__Especifique uma ação de advertências valida, **ban, mute, kick**__")
        else:
            found = await CHAT_ACTION.find_one()
            if found:
                if await check_rights(chat_id, check_admin, "can_change_info"):
                    await CHAT_ACTION.drop()
                    await CHAT_ACTION.insert_one({"_action": query})
                    await m.reply(f"A ação após o número de advertência atingida foi alterado para **{query}**")
                else:
                    return await m.reply("`Você precisa de permissão para fazer isso.`")
            else:
                if await check_rights(chat_id, check_admin, "can_change_info"):
                    await CHAT_ACTION.drop()
                    await CHAT_ACTION.insert_one({"_action": query})
                    await m.reply(f"A ação após o número de advertência atingida foi alterado para **{query}**")
                else: 
                    return await m.reply("`Você precisa de permissão para fazer isso`")


@megux.on_message(filters.command("warn", Config.TRIGGER))
async def warn_cmd(_, m: Message):
    if m.chat.type == ChatType.PRIVATE:
        return 
    if input_str(m):
        x = input_str(m)
        ids = (await megux.get_users(x)).id
        name_user = (await megux.get_users(x)).mention
    LIMIT = get_collection(f"WARNS_LIMIT {m.chat.id}")
    ACTION = get_collection(f"ACTION {m.chat.id}")
    CHAT_LIMIT = await LIMIT.find_one()
    ACTION_CHAT = await ACTION.find_one()
    if not CHAT_LIMIT:
        return await LIMIT.insert_one({"_warnslimit": "3"})
    if not ACTION_CHAT:
        return await ACTION.insert_one({"_action": "ban"})
    GET1 = await LIMIT.find_one({"_warnslimit": "1"})
    GET2 = await LIMIT.find_one({"_warnslimit": "2"})
    GET3 = await LIMIT.find_one({"_warnslimit": "3"})
    GET4 = await LIMIT.find_one({"_warnslimit": "4"})
    GET5 = await LIMIT.find_one({"_warnslimit": "5"})
    GET6 = await LIMIT.find_one({"_warnslimit": "6"})
    GET7 = await LIMIT.find_one({"_warnslimit": "7"})
    BAN = await ACTION.find_one({"_action": "ban"})
    KICK = await ACTION.find_one({"_action": "kick"})
    MUTE = await ACTION.find_one({"_action": "mute"})
    
    WARN = get_collection(f"WARN {m.chat.id} {ids}")
    if await is_self(m.reply_to_message.from_user.id):
        return await m.reply("Não irei me advertir")
    if await admin_check(m.reply_to_message):
        return await m.reply("Não irei advertir um administrador") 
    if GET1:
        max_count = 1
    if GET2:
        max_count = 2 
    if GET3: 
        max_count = 3
    if GET4:
        max_count = 4
    if GET5:
        max_count = 5
    if GET6:
        max_count = 6
    if GET7:
        max_count = 7    
    if not await check_rights(m.chat.id, megux.me.id, "can_restrict_members"):
        return await m.reply("Eu não tenho permissão suficiente para advertir usuários")
    if await check_rights(m.chat.id, m.from_user.id, "can_restrict_members"):          
        name_user = (m.reply_to_message.from_user.mention())
        await WARN.insert_one({"id_": ids, "title": name_user})
        WARNS = await WARN.estimated_document_count()
        if WARNS == max_count: 
            if BAN:
                await m.reply(f"{WARNS}/{max_count} Advertencias, {name_user} foi banido!")
                await WARN.drop()
                await megux.ban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
            if KICK:
                await m.reply(f"{WARNS}/{max_count} Advertencias, {name_user} foi kickado!")
                await WARN.drop()
                await megux.ban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
                await megux.unban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
            if MUTE:
                await m.reply(f"{WARNS}/{max_count} Advertencias, {name_user} foi silenciado!")
                await WARN.drop()
                await megux.restrict_chat_member(m.chat.id, m.reply_to_message.from_user.id, ChatPermissions())
        else:
            await m.reply(f"{name_user} <b>foi advertido!</b>\nEle(a) tem {WARNS}/{max_count} advertências.") 
    else:
        return await m.reply("Você não tem permissão suficiente para advertir usuários!")
    elif m.reply_to_message:
        ids = m.reply_to_message.from_user.id 
        name_user = (m.reply_to_message.from_user.mention()) 
    LIMIT = get_collection(f"WARNS_LIMIT {m.chat.id}")
    ACTION = get_collection(f"ACTION {m.chat.id}")
    CHAT_LIMIT = await LIMIT.find_one()
    ACTION_CHAT = await ACTION.find_one()
    if not CHAT_LIMIT:
        return await LIMIT.insert_one({"_warnslimit": "3"})
    if not ACTION_CHAT:
        return await ACTION.insert_one({"_action": "ban"})
    GET1 = await LIMIT.find_one({"_warnslimit": "1"})
    GET2 = await LIMIT.find_one({"_warnslimit": "2"})
    GET3 = await LIMIT.find_one({"_warnslimit": "3"})
    GET4 = await LIMIT.find_one({"_warnslimit": "4"})
    GET5 = await LIMIT.find_one({"_warnslimit": "5"})
    GET6 = await LIMIT.find_one({"_warnslimit": "6"})
    GET7 = await LIMIT.find_one({"_warnslimit": "7"})
    BAN = await ACTION.find_one({"_action": "ban"})
    KICK = await ACTION.find_one({"_action": "kick"})
    MUTE = await ACTION.find_one({"_action": "mute"})
    
    WARN = get_collection(f"WARN {m.chat.id} {ids}")
    if await is_self(m.reply_to_message.from_user.id):
        return await m.reply("Não irei me advertir")
    if await admin_check(m.reply_to_message):
        return await m.reply("Não irei advertir um administrador") 
    if GET1:
        max_count = 1
    if GET2:
        max_count = 2 
    if GET3: 
        max_count = 3
    if GET4:
        max_count = 4
    if GET5:
        max_count = 5
    if GET6:
        max_count = 6
    if GET7:
        max_count = 7    
    if not await check_rights(m.chat.id, megux.me.id, "can_restrict_members"):
        return await m.reply("Eu não tenho permissão suficiente para advertir usuários")
    if await check_rights(m.chat.id, m.from_user.id, "can_restrict_members"):          
        name_user = (m.reply_to_message.from_user.mention())
        await WARN.insert_one({"id_": ids, "title": name_user})
        WARNS = await WARN.estimated_document_count()
        if WARNS == max_count: 
            if BAN:
                await m.reply(f"{WARNS}/{max_count} Advertencias, {name_user} foi banido!")
                await WARN.drop()
                await megux.ban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
            if KICK:
                await m.reply(f"{WARNS}/{max_count} Advertencias, {name_user} foi kickado!")
                await WARN.drop()
                await megux.ban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
                await megux.unban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
            if MUTE:
                await m.reply(f"{WARNS}/{max_count} Advertencias, {name_user} foi silenciado!")
                await WARN.drop()
                await megux.restrict_chat_member(m.chat.id, m.reply_to_message.from_user.id, ChatPermissions())
        else:
            await m.reply(f"{name_user} <b>foi advertido!</b>\nEle(a) tem {WARNS}/{max_count} advertências.") 
    else:
        return await m.reply("Você não tem permissão suficiente para advertir usuários!")
        
      
@megux.on_message(filters.command("unwarn", Config.TRIGGER))
async def warn_cmd(_, m: Message):
    if input_str(m):
        x = input_str(m)
        ids = (await megux.get_users(x)).id
        name_user = (await megux.get_users(x)).mention
        return
    if m.reply_to_message:
        ids = m.reply_to_message.from_user.id 
        name_user = (m.reply_to_message.from_user.mention())
        return 
    WARN = get_collection(f"WARN {m.chat.id} {ids}")
    if await is_self(m.reply_to_message.from_user.id):
        return await m.reply("Eu não tenho advertências.")
    if await admin_check(m.reply_to_message):
        return await m.reply("Como irei remover a advertência de um administrador? já que ele não tem.") 
    if not await check_bot_rights(m.chat.id, "can_restrict_members"):
        return await m.reply("Eu não tenho permissão suficiente para advertir usuários")
    if await check_rights(m.chat.id, m.from_user.id, "can_restrict_members"): 
        if await WARN.find_one():        
            await WARN.delete_one({"id_": ids, "title": name_user})
            await m.reply(f"Advertência de {name_user} foi removida")
        else:
            return await m.reply("O usuário não possui advertências.")
    else: 
        return await m.reply("Você não tem permissão suficiente para tirar a advertência de um usuário.")
    
