from pyrogram import filters
from pyrogram.errors import Forbidden
from pyrogram.types import Message

from megumin import megux 


@megux.on_message(filters.command("del", prefixes=["/", "!"]))
async def del_message(c: megux, m: Message):
    if m.chat.type != "private":
        member = await c.get_chat_member(chat_id=m.chat.id, user_id=m.from_user.id)

    if m.chat.type == "private" or member.status in [
        "administrator",
        "creator",
    ]:
        try:
            if m.reply_to_message:
                await c.delete_messages(
                    chat_id=m.chat.id,
                    message_ids=[m.reply_to_message.message_id, m.message_id],
                    revoke=True,
                )
            if Forbidden:
                return await m.reply_text("Não é possível excluir essa mensagem. Essa mensagem podem ser muito antiga, talvez eu não tenha direitos de exclusão ou isso pode não ser um supergrupo.")
    else:
        await m.reply_text("Você não é um administrador(a)...")
