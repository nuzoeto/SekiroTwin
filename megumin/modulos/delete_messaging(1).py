from pyrogram import filters
from pyrogram.errors import Forbidden
from pyrogram.types import Message
from pyrogram.enums import ChatType,  ChatMemberStatus

from megumin import megux 


@megux.on_message(filters.command("del", prefixes=["/", "!"]))
async def del_message(c: megux, m: Message):
    if m.chat.type != ChatType.PRIVATE:
        member = await c.get_chat_member(chat_id=m.chat.id, user_id=m.from_user.id)

    if m.chat.type == ChatType.PRIVATE or member.status in [
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    ]:
        try:
            if m.reply_to_message:
                await c.delete_messages(
                    chat_id=m.chat.id,
                    message_ids=[m.reply_to_message.id, m.message.id],
                    revoke=True,
                )
        except Forbidden as e:
            await m.reply_text(
                f"<b>Error:</b> <code>{e}</code>, <b>Report in @DaviTudo."
            )
    else:
        await m.reply_text("Você não é um administrador(a)...")
