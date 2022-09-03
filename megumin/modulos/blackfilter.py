import asyncio
import uuid
import inspect
import math
import os.path
import re
from datetime import datetime, timedelta
from functools import partial, wraps
from string import Formatter
from pyrogram.enums import ParseMode
from typing import Callable, List, Optional, Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, User

from megumin import megux, Config
from megumin.utils import get_collection, check_rights, tld, add_user_count
from megumin.utils.decorators import input_str



@megux.on_message(filters.command(["warnfilter"], Config.TRIGGER))
async def save_blackfilter(c: megux, message: Message):
    chat_id = message.chat.id
    cmd = len(message.text)
    if cmd > 11:
        _, args = message.text.split(maxsplit=1)
        if " " in args:
            name, reason = args.split(" ", maxsplit=1)
        else:
            name = args
    else:
        await message.reply("Dê um nome ao filtro")
        return
    FILTER = get_collection(f"CHAT_FILTERS_WARN {chat_id}")
    if await FILTER.find_one({"name": name}):
        await FILTER.delete_one({"name": name})
        await filter.insert_one({"name": name, "reason": reason or f"Digitar a palavra '{name}'."})
    else:
        await filter.insert_one({"name": name, "reason": reason or f"Digitar a palavra '{name}'."})
    await message.reply(f"Se o usuario digitar '{name}' ele será advertido.")


@megux.on_message(filters.command("blackfilters", Config.TRIGGER) & filters.group)
async def get_all_chat_blackfilter(c: megux, m: Message):
    if not await check_rights(m.chat.id, m.from_user.id, "can_change_info"):
        return
    db = get_collection(f"CHAT_FILTERS_WARN {m.chat.id}")
    chat_id = m.chat.id
    reply_text = "<b>Lista de Textos bloqueados em {}:</b>\n\n".format(m.chat.title)
    all_filters = db.find()          
    async for filter_s in all_filters:
        keyword = filter_s["name"]
        reply_text += f" • <code>{keyword}</code> \n"
    if not await db.find_one():
        await m.reply_text("<i>Esse chat não tem filtros.</i>", quote=True)
    else:
        await m.reply_text(reply_text, quote=True)
    await m.stop_propagation()
        
        
@megux.on_message(filters.command(["rmblackfilter", "delblackfilter", "blackstop"]))
async def rmblackfilter(c: megux, m: Message):
    if not await check_rights(m.chat.id, m.from_user.id, "can_change_info"):
        return
    args = m.text.html.split(maxsplit=1)
    trigger = args[1].lower()
    chat_id = m.chat.id
    db = get_collection(f"CHAT_FILTERS_WARN {chat_id}")
    check_note = await db.find_one({"name": trigger})
    if check_note:
        await db.delete_one({"name": trigger})
        await m.reply_text(
            "BlackFilter {} Removido em {}".format(trigger, m.chat.title), quote=True
        )
    else:
        await m.reply_text(
            "Esse não é um blackfiltro ativo - use o comando /filters para todos os filtros ativos.".format(trigger), quote=True
        )
    await m.stop_propagation()

        
@megux.on_message(filters.command(["resetblackfilters", "clearblackfilters"]))
async def clear_blackfilter(c: megux, m: Message):
    chat_id = m.chat.id
    if not await check_rights(chat_id, m.from_user.id, "can_change_info"):
        return
    db = get_collection(f"CHAT_FILTERS_WARN {chat_id}")
    check_note = await db.find_one()
    if check_note:
        await db.drop()
        await m.reply_text(
            "Todos os blackfiltros desse chat foram apagadas.", quote=True
        )
    else:
        await m.reply_text(
            "O grupo não tem blackfiltros.", quote=True
        )  
    await m.stop_propagation()


@megux.on_message(
    (filters.group | filters.private) & filters.text & filters.incoming, group=8
)
async def serve_blackfilter(c: megux, m: Message):
    chat_id = m.chat.id
    db = get_collection(f"CHAT_FILTERS_WARN {m.chat.id}")
    warns = get_collection(f"WARNS {chat_id}")
    limit = get_collection(f"WARN_LIMIT {chat_id}")
    action = get_collection(f"WARN_ACTION {chat_id}")

    get_limit = await limit.find_one()
    get_action = await action.find_one()
    #get limit warns
    if get_limit:
        chat_limit = get_limit["limit"]
    else:
        chat_limit = 3
    #get action warns
    if get_action:
        chat_action = get_action["action"]
    else:
        chat_action = "ban"
    if m and m.from_user:
        user_id = m.from_user.id
        mention = m.from_user.mention
        await add_user_count(chat_id, m.from_user.id)
    else:
        return
    text = m.text

    all_filters = db.find()
    async for filter_s in all_filters:
        keyword = filter_s["name"]
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, text, flags=re.IGNORECASE):
            reason = filter_s["reason"]
            await warns.insert_one({"user_id": user_id, "warn_id": str(uuid.uuid4()), "reason": reason or None})
            user_warns = await warns.count_documents({"user_id": user_id})
            if user_warns >= warns_limit:
                if chat_action == "ban":
                    await m.chat.ban_member(user_id)
                    await m.reply((await get_string(chat_id, "WARNS_BANNED")).format(user_warns, chat_limit, mention))
                elif chat_action == "mute":
                    await m.chat.restrict_member(user_id, ChatPermissions())
                    await m.reply((await get_string(chat_id, "WARNS_MUTED")).format(user_warns, chat_limit, mention))
                elif chat_action == "kick":
                    await m.chat.ban_member(user_id)
                    await m.chat.unban_member(user_id)
                    await m.reply((await get_string(chat_id, "WARNS_KICKED")).format(user_warns, chat_limit, mention))
                else:
                    return
                await warns.delete_many({"user_id": user_id})
            else:
                await m.reply((await get_string(chat_id, "USER_WARNED")).format(mention, user_warns, chat_limit, reason or None))
    await m.stop_propagation()
