from pyrogram import filters
from pyrogram.types import Message

from megumin import megux, Config  
from megumin.utils import (
    check_bot_rights,
    check_rights,
    is_admin,
    is_dev,
    is_self,
    sed_sticker,
    get_collection,
    get_string
)
from megumin.utils.decorators import input_str 

@megux.on_message(filters.command("setgrouppic", prefixes=["/", "!"]))
async def set_chat_photo(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    reply = message.reply_to_message

    if not reply:
        return await message.reply_text(
            "Marque uma foto ou documento para que eu possa alterar a foto do Grupo"
        )
    if not await check_rights(chat_id, message.from_user.id, "can_change_info"):
        await message.reply("Você não tem direitos administrativos suficientes para alterar dados do grupo!")
        return

    file = reply.document or reply.photo
    if not file:
        return await message.reply_text(
            "Marque uma foto ou documento para que eu possa alterar a foto do Grupo"
        )

    if file.file_size > 5000000:
        return await message.reply("__Esse arquivo é muito grande__")

    photo = await reply.download()
    sucess = await message.chat.set_photo(photo)
    await message.reply_text(f"Foto alterada com sucesso no grupo <b>{message.chat.title}</b>")

@megux.on_message(filters.command("setrules", Config.TRIGGER))
async def rules_set(_, m: Message):
    x = ""
    if input_str(m):
        x += m.text.split(None, 1)[1]
    if m.reply_to_message:
        x += m.reply_to_message.text
    data = get_collection(f"RULES {m.chat.id}")
    if x in "":
        return await m.reply(await get_string(m.chat.id, "RULES_NO_ARGS"))
    else:
         if await check_rights(m.chat.id, m.from_user.id, "can_change_info"):
             await data.drop()
             await data.insert_one({"_rules": x})
             await m.reply(await get_string(m.chat.id, "RULES_UPDATED"))


@megux.on_message(filters.command("clearrules", Config.TRIGGER))
async def del_rules_(_, m: Message):
    if await check_rights(m.chat.id, m.from_user.id, "can_change_info"):
        RULES = get_collection(f"RULES {m.chat.id}")
        i = await RULES.find_one()
        res = i["_rules"]
        await RULES.delete_one({"_rules": res})
        await m.reply(await get_string(m.chat.id, "RULES_CLEAR_SUCCESS"))


@megux.on_message(filters.command("setlog", prefixes=["/", "!"]))
async def set_log(_, m: Message):
    chat_log = ""
    chat_log += input_str(m)
    if not "-100" in chat_log:
        return await m.reply("Isso não é um grupo!")
    if await check_rights(m.chat.id, m.from_user.id, "can_change_info"):
        if input_str(m):
            data = get_collection(f"LOGS {m.chat.id}")
            await data.drop()
            await data.insert_one({"log_id": chat_log})
            chat = await data.find_one()
            await m.reply(await get_string(m.chat.id, "LOGS_DEFINED_MESSAGE"))
            await megux.send_message(chat["log_id"], (await get_string(m.chat.id, "LOGS_DEFINED")).format(m.chat.title))
        else:
            return 
