import asyncio

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux
from megumin.utils import get_collection, is_dev

USERS = get_collection("USERS")
GROUPS = get_collection("GROUPS")
USERS_STARTED = get_collection("USERS_START")
AFK_COUNT = get_collection("AFK_COUNT")

@megux.on_message(filters.command(["status"]))
async def status_(_, m: Message):
    user_id = m.from_user.id
    if not is_dev(user_id):
        return
    glist = await GROUPS.estimated_document_count()
    ulist = await USERS.estimated_document_count()
    afk_status = await AFK_COUNT.estimated_document_count()
    userlist = await USERS_STARTED.estimated_document_count()
    await m.reply(f"**【 WhiterKang Status 】**\n\n**Usuários**: __{userlist}__\n**Usuários em AFK**: __{afk_status}__\n**Regs**: __{ulist}__\n**Grupos**: __{glist}__")
