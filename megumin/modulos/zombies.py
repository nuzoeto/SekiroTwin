import os
import re

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import BadRequest, Forbidden

from megumin import megux


@megux.on_message(filters.command(["zombies", "cleanup"], prefixes=["/", "!"]))
async def cleanup(c: megux, m: Message):
    if m.chat.type == "private":
        await m.reply_text("Este comando é para ser usado em grupos!")
        return

    member = await c.get_chat_member(chat_id=m.chat.id, user_id=m.from_user.id)
    if member.status in ["administrator", "creator"]:
        deleted = []
        sent = await m.reply_text("Iniciando limpeza...")
        async for t in c.iter_chat_members(chat_id=m.chat.id, filter="all"):
            if t.user.is_deleted:
                try:
                    await c.ban_chat_member(m.chat.id, t.user.id)
                    await sent.edit("Limpando...")
                    deleted.append(t)
                except BadRequest:
                    pass
                except Forbidden as e:
                    await m.reply_text(
                        f"<b>Error:</b> <code>{e}</code>"
                    )
                    return
        if deleted:
            await sent.edit_text(
                f"Eu removi todas contas excluídas do grupo **{m.chat.title}**!"
            )
        else:
            await sent.edit_text("Não há contas excluídas aqui!")
    else:
        await m.reply_text("Balabacheia! Você não é um(a) administrador(a)")
