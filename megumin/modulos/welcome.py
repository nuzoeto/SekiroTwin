import asyncio
import inspect
import math
import os.path
import re

from string import Formatter
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.errors import BadRequest
from pyrogram.types import InlineKeyboardMarkup, Message
from typing import Callable, List, Optional, Union

BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\(buttonurl:(?:/{0,2})(.+?)(:same)?\))")

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


def get_format_keys(string: str) -> List[str]:
    """Return a list of formatting keys present in string."""
    return [i[1] for i in Formatter().parse(string) if i[1] is not None]


from megumin import megux 
from megumin.utils import get_collection 


@megux.on_message(filters.command("setwelcome"))
async def set_welcome_message(c: megux, m: Message):
    if len(m.text.split()) > 1:
        message = m.text.html.split(None, 1)[1]
        WELCOME = get_collection(f"WELCOME {m.chat.id}")
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
        except (KeyError, BadRequest) as e:
            await m.reply_text(
                "Erro: {error}".format(
                    error=e.__class__.__name__ + ": " + str(e)
                )
            )
        else:
            await WELCOME.drop()
            await WELCOME.insert_one({"id_": m.chat.id, "welcome": message})
            await sent.edit_text(
                "Boas vindas alterada com sucesso no chat {chat_title}".format(chat_title=m.chat.title)
            )
    else:
        await m.reply_text(
            "Defina uma mensagem exemplo: Olá  {bot_username}".format(bot_username=c.me.username),
            disable_web_page_preview=True,
        )


@megux.on_message(filters.command("welcome on") & filters.group)
async def enable_welcome_message(c: megux, m: Message):
    data = get_collection(f"WELCOME_ARGS {m.chat.id}")
    await data.insert_one({"id_": m.chat.id, "get": "True"})
    await m.reply_text("As boas vindas foram ativadas no chat {chat_title}".format(chat_title=m.chat.title))


@megux.on_message(filters.command("welcome off") & filters.group)
async def enable_welcome_message(c: megux, m: Message):
    data = get_collection(f"WELCOME_ARGS {m.chat.id}")
    await data.insert_one({"id_": m.chat.id, "get": "False"})
    await m.reply_text("As boas vindas foram ativadas no chat {chat_title}".format(chat_title=m.chat.title))


@megux.on_message(filters.new_chat_members & filters.group)
async def greet_new_members(c: megux, m: Message):
    data = get_collection(f"WELCOME {m.chat.id}")
    data_args = get_collection(f"WELCOME_ARGS {m.chat.id}")
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
        HD = await data.find_one()
        welcome_enabld = await data_args.find_one({"id_": m.chat.id, "get": "True"})
        welcome, welcome_enabled = HD["welcome"]
        if welcome_enabled:
            if not HD:
                welcome = "Olá {mention} Seja bem vindo ao chat {chat_title} Sinta-se a vontade."

            if "count" in get_format_keys(welcome):
                count = await c.get_chat_members_count(m.chat.id)
            else:
                count = 0

            welcome = welcome.format(
                id=user_id,
                username=username,
                mention=mention,
                first_name=first_name,
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
