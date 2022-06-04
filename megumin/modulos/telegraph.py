##
#
import os

from pyrogram import filters
from pyrogram.types import Message
from telegraph import upload_file

from megumin import megux


@megux.on_message(filters.command(["tg", "telegraph"], prefixes=["/", "!"]))
async def telegraph_(megux, message: Message):
    replied = message.reply_to_message
    if not replied:
        await message.reply("`Responda a alguma mídia.`")
        return
    if not (
        (replied.photo and replied.photo.file_size <= 5242880)
        or (replied.animation and replied.animation.file_size <= 5242880)
        or (
            replied.video
            and replied.video.file_name.endswith(".mp4")
            and replied.video.file_size <= 5242880
        )
        or (
            replied.document
            and replied.document.file_name.endswith(
                (".jpg", ".jpeg", ".png", ".gif", ".mp4")
            )
            and replied.document.file_size <= 5242880
        )
    ):
        await message.reply("`Não suportado!`")
        return
    download_location = await megux.download_media(
        message=message.reply_to_message, file_name="megumin/xcache/"
    )
    msg = await message.reply("`Fazendo upload no telegraph...`")
    try:
        response = upload_file(download_location)
    except Exception as document:
        await msg.edit(document)
    else:
        link = "<b>[Aqui, seu link telegraph!](https://telegra.ph{})</b>"
        await msg.edit(link.format(response[0]), disable_web_page_preview=True)
    finally:
        os.remove(download_location)
