import asyncio

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux
from megumin.utils import get_collection, is_dev

USERS = get_collection("USERS")
GROUPS = get_collection("GROUPS")

@yuuna.on_message(filters.command(["status"]))
async def status_(_, m: Message):
    user_id = m.from_user.id
    if not is_dev(user_id):
        return
    glist = await GROUPS.estimated_document_count()
    ulist = await USERS.estimated_document_count()
    await m.reply(f"**♬🎷【 Bot Status 】●♪**\n\n**Users**: __{ulist}__\n**Groups**: __{glist}__")
