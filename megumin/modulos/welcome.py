import asyncio
import inspect
import math
import os.path
import re
from datetime import datetime, timedelta
from functools import partial, wraps
from string import Formatter
from typing import Callable, List, Optional, Union

from pyrogram import Client, emoji, filters
from pyrogram.enums import ChatMemberStatus, MessageEntityType
from pyrogram.types import CallbackQuery, InlineKeyboardButton, Message, User

BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\(buttonurl:(?:/{0,2})(.+?)(:same)?\))")

SMART_OPEN = "“"
SMART_CLOSE = "”"
START_CHAR = ("'", '"', SMART_OPEN)

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

from megumin import megux, Config 
from megumin.utils import get_collection, get_string 


@Client.on_message(filters.command("getwelcome", PREFIXES) & filters.group)
@require_admin(permissions=["can_change_info"])
@use_chat_lang()
async def getwelcomemsg(c: Client, m: Message, strings):
    welcome, welcome_enabled = await get_welcome(m.chat.id)
    if welcome_enabled:
        await m.reply_text(
            strings("welcome_default") if welcome is None else welcome,
            parse_mode=ParseMode.DISABLED,
        )
    else:
        await m.reply_text("None")


@Client.on_message(filters.command("welcome on", PREFIXES) & filters.group)
async def enable_welcome_message(c: Client, m: Message):
    DATA = get_collection(f"WELCOME_STATUS chat {m.chat.id}")
    await DATA.drop()
    await DATA.insert_one({"status": "on"})
    await m.reply_text(f"Boas Vindas Desativadas em {m.chat.title}")


@Client.on_message(filters.command("welcome off", Config.TRIGGER) & filters.group)
async def disable_welcome_message(c: Client, m: Message):
    DATA = get_collection(f"WELCOME_STATUS chat {m.chat.id}")
    await DATA.drop()
    await DATA.insert_one({"status": "off"})
    await m.reply_text(f"Boas Vindas Desativadas em {m.chat.title}")


@Client.on_message(
    filters.command(["resetwelcome", "clearwelcome"], Config.TRIGGER) & filters.group
)
async def reset_welcome_message(c: Client, m: Message):
    DATA = get_collection(f"WELCOME chat {m.chat.id}")
    await DATA.drop()
    await DATA.insert_one({"welcome": "None"})
    await m.reply_text(f"Boas Vindas resetadas em {m.chat.title}")
