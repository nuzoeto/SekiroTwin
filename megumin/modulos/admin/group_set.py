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
)

@megux.on_message(filters.command("setgrouppic", prefixes=["/", "!"]))
async def set_chat_photo(_, message):
    reply = message.reply_to_message

    if not reply:
        return await message.reply_text(
            "Reply to a photo to set it as chat_photo"
        )
    if not await check_rights(chat_id, message.from_user.id, "can_promote_members"):
        await message.reply("Você não tem direitos administrativos suficientes para alterar dados do grupo!")
        return

    file = reply.document or reply.photo
    if not file:
        return await message.reply_text(
            "Reply to a photo or document to set it as chat_photo"
        )

    if file.file_size > 5000000:
        return await message.reply("__Esse arquivo é muito grande__")

    photo = await reply.download()
    await message.chat.set_photo(photo)
    await message.reply_text("Foto alterada com sucesso no grupo {message.chat.title}")
)
