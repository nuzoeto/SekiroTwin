from pyrogram import filters 
from pyrogram.types import Message 

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
    if m.chat.type == "private":
        return await m.reply("Esse comando é para ser usado em grupos.")
    else:
        if not query in NUMBER:
            return await m.reply("__Especifique um número de advertências valido, de 1 a 7.__")
        else:
            found = await LIMIT.find_one()
            if found:
                if await check_rights(chat_id, check_admin, "can_change_info"):
                    await LIMIT.delete_one({"_warnslimit": query})
                    await LIMIT.insert_one({"_warnslimit": query})
                    await m.reply(f" O número de advertência foi alterado para **{query}**")
                else:
                    return await m.reply("`Você precisa de permissão para fazer isso.`")
            else:
                if await check_rights(chat_id, check_admin, "can_change_info"):
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
    if m.chat.type == "private":
        return await m.reply("Esse comando é para ser usado em grupos.")
    else:
        if not query in ACTION:
            return await m.reply("__Especifique uma ação de advertências valida, **ban, mute, kick**__")
        else:
            found = await CHAT_ACTION.find_one()
            if found:
                if await check_rights(chat_id, check_admin, "can_change_info"):
                    await CHAT_ACTION.delete_one({"_action": query})
                    await CHAT_ACTION.insert_one({"_action": query})
                    await m.reply(f"A ação após o número de advertência atingida foi alterado para **{query}**")
                else:
                    return await m.reply("`Você precisa de permissão para fazer isso.`")
            else:
                if await check_rights(chat_id, check_admin, "can_change_info"):
                    await CHAT_ACTION.insert_one({"_action": query})
                    await m.reply(f"A ação após o número de advertência atingida foi alterado para **{query}**")
                else: 
                    return await m.reply("`Você precisa de permissão para fazer isso`")


@megux.on_message(filters.command("warn", Config.TRIGGER))
async def warn_cmd(_, m: Message):
    ids = m.reply_to_message.from_user.id 
    WARN = get_collection(f"WARN {m.chat.id} {ids}")
    if await is_self(m.reply_to_message.from_user.id):
        return await m.reply("Não irei me advertir")
    if await admin_check(m.reply_to_message):
        return await m.reply("Não irei advertir um administrador") 
    if not await check_bot_rights(m.chat.id, "can_restrict_members"):
        return await m.reply("Eu não tenho permissão suficiente para advertir usuários")
    if await check_rights(m.chat.id, m.from_user.id, "can_restrict_members"):          
        name_user = (m.reply_to_message.from_user.mention())
        await WARN.insert_one({"id_": ids, "title": name_user})
        WARNS = await WARN.estimated_document_count()
        if WARNS > 2: 
            await m.reply(f"{WARNS}/3 Advertencias, {name_user} foi banido!")
            await WARN.drop()
            await megux.ban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
        else:
            await m.reply(f"{name_user} tem {WARNS}/3 advertências.") 
    else:
        return await m.reply("Você não tem permissão suficiente para advertir usuários!")
        
      
@megux.on_message(filters.command("unwarn", Config.TRIGGER))
async def warn_cmd(_, m: Message):
    ids = m.reply_to_message.from_user.id 
    WARN = get_collection(f"WARN {m.chat.id} {ids}")
    if await is_self(m.reply_to_message.from_user.id):
        return await m.reply("Eu não tenho advertências.")
    if await admin_check(m.reply_to_message):
        return await m.reply("Como irei remover a advertência de um administrador? já que ele não tem.") 
    if not await check_bot_rights(m.chat.id, "can_restrict_members"):
        return await m.reply("Eu não tenho permissão suficiente para advertir usuários")
    if await check_rights(m.chat.id, m.from_user.id, "can_restrict_members"): 
        if await WARN.find_one():        
            name_user = (m.reply_to_message.from_user.mention())
            await WARN.delete_one({"id_": ids, "title": name_user})
            await m.reply(f"Advertência de {name_user} foi removida")
        else:
            return await m.reply("O usuário não possui advertências.")
    else: 
        return await m.reply("Você não tem permissão suficiente para tirar a advertência de um usuário.")
    
