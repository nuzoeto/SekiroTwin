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
    get_collection,
    get_string,
)


@megux.on_message(filters.command(["cleanup", "zombies"], prefixes=["/", "!"]))
async def cleanup(c: megux, m: Message):
    LOGS = get_collection(f"LOGS {m.chat.id}")
    chat_id = m.chat.id
    if m.chat.type == ChatType.PRIVATE:
        await m.reply_text("Este comando é para ser usado em grupos!")
        return
    if not await check_bot_rights(chat_id, "can_restrict_members"):
        await m.reply(await get_string(chat_id, "NO_BAN_BOT"))
        return 
    if await check_rights(chat_id, m.from_user.id, "can_restrict_members"): 
        count = 0
        sent = await m.reply_text(await get_string(chat_id, "COM_1"))
        async for t in c.get_chat_members(chat_id=m.chat.id):
            if t.user.is_deleted:
                try:
                    await c.ban_chat_member(m.chat.id, t.user.id)
                    count += 1
                except BadRequest:
                    pass
                except Forbidden as e:
                    await m.reply_text(
                        f"<b>Erro:</b> <code>{e}</code>"
                    )
                    return
        if count:
            await sent.edit_text(
                (await get_string(chat_id, "ZOMBIES_BAN")).format(count, m.chat.title)
            )
            data = await LOGS.find_one()
            if data:
                id = data["log_id"]
                id_log = int(id)
                await megux.send_message(id_log, (await get_string(chat_id, "ZOMBIES_LOGGER")).format(m.chat.title, m.from_user.mention(), count))
                return
        else:
            await sent.edit_text("Não há contas excluídas no grupo!")
    else:
        await m.reply_text("Balabacheia! Você não tem direitos administrativos suficientes para banir/desbanir usuários!")
