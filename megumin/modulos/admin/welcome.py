import asyncio
import re
import math
import inspect
import os.path

from pyrogram import filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ParseMode

from datetime import datetime, timedelta
from functools import partial, wraps
from string import Formatter
from typing import Callable, List, Optional, Union


from megumin import megux, Config
from megumin.utils import get_collection, check_rights



BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\(buttonurl:(?:/{0,2})(.+?)(:same)?\))")

def get_format_keys(string: str) -> List[str]:
    """Return a list of formatting keys present in string."""
    return [i[1] for i in Formatter().parse(string) if i[1] is not None]


def button_parser(markdown_note):
    note_data = ""
    buttons = []
    if markdown_note is None:
        return note_data, buttons
    if markdown_note.startswith("/") or markdown_note.startswith("!"):
        args = markdown_note.split(None, 2)
        markdown_note = args[2]
    prev = 0
    for match in BTN_URL_REGEX.finditer(markdown_note):
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and markdown_note[to_check] == "\\":
            n_escapes += 1
            to_check -= 1

        if n_escapes % 2 == 0:
            if bool(match.group(4)) and buttons:
                buttons[-1].append(
                    InlineKeyboardButton(text=match.group(2), url=match.group(3))
                )
            else:
                buttons.append(
                    [InlineKeyboardButton(text=match.group(2), url=match.group(3))]
                )
            note_data += markdown_note[prev : match.start(1)]
            prev = match.end(1)

        else:
            note_data += markdown_note[prev:to_check]
            prev = match.start(1) - 1

    note_data += markdown_note[prev:]

    return note_data, buttons


@megux.on_message(filters.command("setwelcome", Config.TRIGGER))
async def set_welcome_message(c: megux, m: Message):
    db = get_collection(f"WELCOME {m.chat.id}")
    if not await check_rights(m.chat.id, m.from_user.id, "can_change_info"):
        return
    if len(m.text.split()) > 1:
        message = m.text.html.split(None, 1)[1]
        try:
            # Try to send message with default parameters
            sent = await m.reply_text(
                message.format(
                    id=m.from_user.id,
                    username=m.from_user.username,
                    mention=m.from_user.mention,
                    first_name=m.from_user.first_name,
                    # full_name and name are the same
                    full_name=m.from_user.first_name,
                    name=m.from_user.first_name,
                    # title and chat_title are the same
                    title=m.chat.title,
                    chat_title=m.chat.title,
                    count=(await c.get_chat_members_count(m.chat.id)),
                )
            )
            await asyncio.sleep(0.7)
        except (KeyError, BadRequest) as e:
            await m.reply_text(
                "<b>Erro:</b> {error}".format(
                    error=e.__class__.__name__ + ": " + str(e)
                )
            )
        else:
            await db.drop()
            await db.insert_one({"msg": message})
            await sent.edit_text(
                "Boas Vindas Alterada em {chat_title}".format(chat_title=m.chat.title)
            )
    else:
        await m.reply_text(
            "De um argumento exemplo: /setwelcome Olá {mention}",
            disable_web_page_preview=True,
        )

@megux.on_message(filters.command("welcome on", Config.TRIGGER) & filters.group)
async def enable_welcome_message(c: megux, m: Message):
    db = get_collection(f"WELCOME_STATUS {m.chat.id}")
    if not await check_rights(m.chat.id, m.from_user.id, "can_change_info"):
        return
    await db.drop()
    await db.insert_one({"status": True})
    await m.reply_text("Boas Vindas agora está Ativadas.")
    
    
@megux.on_message(filters.command("welcome off", Config.TRIGGER) & filters.group)
async def enable_welcome_message(c: megux, m: Message):
    db = get_collection(f"WELCOME_STATUS {m.chat.id}")
    if not await check_rights(m.chat.id, m.from_user.id, "can_change_info"):
        return
    await db.drop()
    await db.insert_one({"status": False})
    await m.reply_text("Boas Vindas agora está Desativadas.")
    
    
@megux.on_message(filters.command("welcome", Config.TRIGGER) & filters.group)
async def enable_welcome_message(c: megux, m: Message):
    if not await check_rights(m.chat.id, m.from_user.id, "can_change_info"):
        return
    await m.reply_text("Dê um argumento exemplo: /welcome on/off")
 

@megux.on_message(filters.new_chat_members & filters.group)
async def greet_new_members(c: megux, m: Message):
    db = get_collection(f"WELCOME {m.chat.id}")
    db_ = get_collection(f"WELCOME_STATUS {m.chat.id}")
    members = m.new_chat_members
    chat_title = m.chat.title
    first_name = ", ".join(map(lambda a: a.first_name, members))
    full_name = ", ".join(
        map(lambda a: a.first_name + " " + (a.last_name or ""), members)
    )
    user_id = ", ".join(map(lambda a: str(a.id), members))
    username = ", ".join(
        map(lambda a: "@" + a.username if a.username else a.mention, members)
    )
    mention = ", ".join(map(lambda a: a.mention, members))
    if not m.from_user.is_bot:
        welcome_enabled = await db_.find_one({"status": True})
        welcome_pack = await db.find_one()
        if welcome_enabled:
            if not welcome_pack:
                welcome = "Hey {first_name}, how are you?"
            else:
                welcome = welcome_pack["msg"]
            if "count" in get_format_keys(welcome):
                count = await c.get_chat_members_count(m.chat.id)
            else:
                count = 0

            welcome = welcome.format(
                id=user_id,
                username=username,
                mention=mention,
                first_name=first_name,
                first=first_name,
                # full_name and name are the same
                full_name=full_name,
                name=full_name,
                # title and chat_title are the same
                title=chat_title,
                chat_title=chat_title,
                count=count,
            )
            welcome, welcome_buttons = button_parser(welcome)
            await m.reply_text(
                welcome,
                disable_web_page_preview=True,
                reply_markup=(
                    InlineKeyboardMarkup(welcome_buttons)
                    if len(welcome_buttons) != 0
                    else None
                ),
            )

    
@megux.on_message(filters.command("getwelcome", Config.TRIGGER))
async def get_welcome(c: megux, m: Message):
    db = get_collection(f"WELCOME {m.chat.id}")
    resp = await db.find_one()
    if resp:
        welcome = resp["msg"]
    else:
        welcome = "Hey {first}, how are you?"
        
    await m.reply(welcome)

    
@megux.on_message(filters.command("resetwelcome", Config.TRIGGER))
async def rm_welcome(c: megux, m: Message):
    db = get_collection(f"WELCOME {m.chat.id}")
    r = await db.find_one()
    if r:
        await db.drop()
        await m.reply("A mensagem de boas vindas foi resetada!") 
    else:
        return await m.reply("Nenhuma mensagem de boas vindas foi definida.")
