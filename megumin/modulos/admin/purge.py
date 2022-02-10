from pyrogram import filters
from pyrogram.errors import MessageDeleteForbidden
from pyrogram.types import Message

from megumin import megux
from megumin.utils import admin_check


@megux.on_message(filters.command("purge"))
async def purge_command(megux, message: Message):
    await message.reply("```Apagando as mensagens...```")
    can_purge = await admin_check(message)
    if can_purge:
        try:
            message_reply = int(message.reply_to_message.message_id)
        except AttributeError:
            await message.reply(
                "Por favor, marque a mensagem por onde deseja começar o purge."
            )
            return

        while True:
            try:
                await message.edit("**Limpeza completa!**")
                await megux.delete_messages(message.chat.id, message_reply)
                message_reply += 1
            except MessageDeleteForbidden:
                await message.reply(
                    "Infelizmente não tenho permissão para apagar as mensagens."
                )
                return
            except Exception as exc:
                await message.reply(f"ERRO: {exc}")
                return
    else:
        await message.reply("Você precisa ser admin para dar purge.")
