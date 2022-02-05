from pyrogram import filters
from pyrogram.errors import MessageDeleteForbidden
from pyrogram.types import Message

from megumin import megux
from megumin.utils import admin_check


@megux.on_message(filters.command("purge"))
async def purge_command(megux, message: Message):
    can_purge = await admin_check(message)
    if can_purge:
        try:
            message_reply = int(message.reply_to_message.message_id)
        except AttributeError:
            await message.reply(
                "Por favor, marque a mensagem que deseja apagar."
            )
            return

        while True:
            try:
                await megux.delete_messages(message.chat.id, message_reply 
            except MessageDeleteForbidden:
                await message.reply(
                    "Eu não tenho as seguintes permissões: **Can delete messages**.  "
                )
                return
            except Exception as exc:
                await message.reply(f"ERRO: {exc}")
                return
    else:
        await message.reply("👮‍♀ Você precisa ser um administrador!")
