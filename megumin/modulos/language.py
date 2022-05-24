import asyncio

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import Message

from megumin import megux
from megumin.utils import get_collection, check_rights, get_string, add_lang
from megumin.utils.decorators import input_str 


CHAT_LANG = get_collection("CHAT_LANG")
LANGS = ["en", "pt"]


@megux.on_message(filters.command(["setlang", "lang"]))
async def set_lang(_, m: Message):
    if m.chat.type == ChatType.SUPERGROUP:
        if not await check_rights(m.chat.id, m.from_user.id, "can_change_info"):
            return
    lang = input_str(m).lower()
    if not lang:
        return await m.reply(await get_string(gid=m.chat.id, "LANG"))
    if not lang.split()[0] in LANGS:
        return await m.reply(await get_string(gid=m.chat.id, "LANG_"))
    await add_lang(m.chat.id, lang.split()[0])
    await asyncio.sleep(2)
    await m.reply(await get_string(gid=m.chat.id, "LANG_SET"))


@megux.on_message(filters.command(["l"]))
async def test_lang(_, m: Message):
    await m.reply(await get_string(gid=m.chat.id, "language"))
