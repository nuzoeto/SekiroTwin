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
                "Responda a uma mensagem para selecionar por onde iniciar a limpeza."
            )
            return

        while True:
            try:
                await megux.delete_messages(message.chat.id, message_reply)
                message_reply += 1
            except MessageDeleteForbidden:
                await message.reply(
                    "Infelizmente não tenho permissão para apagar as mensagens."
                )
                return
            except Exception as exc:
                await message.reply(f"Não é possível excluir todas as mensagens. As mensagens podem ser muito antigas, talvez eu não tenha direitos de exclusão ou isso pode não ser um supergrupo.")
                return
    else:
        await message.reply("Você precisa ser admin para dar purge.")
        ignore_errors=True
