import os
import re

from pyrogram import filters
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
    if m.chat.type == "private":
        return await m.reply_text("Esse comando não pode ser usado em um grupo privado, use esse comando em um grupo que você administra.")
    else:
        bot = await c.get_chat_member(chat_id=m.chat.id, user_id=(await c.get_me()).id)
        member = await c.get_chat_member(chat_id=m.chat.id, user_id=m.from_user.id)
        if member.status in ["administrator", "creator"]:
            if bot.status in ["administrator"]:
                pass
            else:
                return await m.reply_text("Eu não sou um administrador do grupo!")
        else:
            return await m.reply_text("Você não é um administrador do grupo")
    deleted_users = []
    sent = await m.reply_text("Removendo contas excluídas...")
    async for a in c.iter_chat_members(chat_id=m.chat.id, filter="all"):
        if a.user.is_deleted:
            try:
                await c.ban_chat_member(m.chat.id, a.user.id)
                deleted_users.append(a)
                await sent.edit_text("Contas excluídas: {}".format(
                    {len(deleted_users)}
                )
            except BadRequest:
                pass
            except Forbidden as e:
                return await m.reply_text(f"<b>Erro:</b> {e}")
        else:
            await sent.edit_text("Não há contas excluídas no grupo.")
