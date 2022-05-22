import os
import re

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import Message
from pyrogram.errors import BadRequest, Forbidden

from megumin import megux
from megumin.utils import (
    admin_check,
    extract_time,
    check_bot_rights,
    check_rights,
    is_admin,
    is_dev,
    is_self,
    sed_sticker,
)


@megux.on_message(filters.command(["cleanup", "zombies"], prefixes=["/", "!"]))
async def cleanup(c: megux, m: Message):
    chat_id = m.chat.id
    if m.chat.type == ChatType.PRIVATE:
        await m.reply_text("Este comando é para ser usado em grupos!")
        return
    if await check_rights(chat_id, m.from_user.id, "can_restrict_members"): 
        deleted = []
        sent = await m.reply_text("Limpando...")
        async for t in c.iter_chat_members(chat_id=m.chat.id, filter="all"):
            if t.user.is_deleted:
                try:
                    await c.ban_chat_member(m.chat.id, t.user.id)
                    deleted.append(t)
                except BadRequest:
                    pass
                except Forbidden as e:
                    await m.reply_text(
                        f"<b>Erro:</b> <code>{e}</code>"
                    )
                    return
        if deleted:
            await sent.edit_text(
                f"Eu removi todas as contas excluídas do grupo **{m.chat.title}**!"
            )
        else:
            await sent.edit_text("Não há contas excluídas no grupo!")
    else:
        await m.reply_text("Balabacheia! Você não tem direitos administrativos suficientes para banir/desbanir usuários!")
