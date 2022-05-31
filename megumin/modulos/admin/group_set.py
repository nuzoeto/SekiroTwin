from pyrogram import filters
from pyrogram.types import Message

from megumin import megux 
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

@megux.on_message(filters.command("setrules"))
async def rules_set(_, m: Message):
    if input_str(m):
        x = input_str(m)
    if m.reply_to_message:
        x = m.reply_to_message.text
    data = get_collection(f"RULES {m.chat.id}")
    if not x:
        return await m.reply(await get_string(m.chat.id, "NO_SETRULES_ARGS"))
    else:
         if await check_rights(m.chat.id, m.from_user.id, "can_change_info"):
             await data.drop()
             await data.insert_one({"_rules": x})
             await m.reply(await get_string(m.chat.id, "RULES_UPDATED")
