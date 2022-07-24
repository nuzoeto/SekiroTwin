import asyncio
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
from pyrogram.types import CallbackQuery, InlineKeyboardButton, Message, User

from megumin import megux, Config
from megumin.utils import get_collection, check_rights
from megumin.utils.decorators import input_str

BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\(buttonurl:(?:/{0,2})(.+?)(:same)?\))")

SMART_OPEN = "“"
SMART_CLOSE = "”"
START_CHAR = ("'", '"', SMART_OPEN)


def remove_escapes(text: str) -> str:
    counter = 0
    res = ""
    is_escaped = False
    while counter < len(text):
        if is_escaped:
            res += text[counter]
            is_escaped = False
        elif text[counter] == "\\":
            is_escaped = True
        else:
            res += text[counter]
        counter += 1
    return res


def split_quotes(text: str) -> List:
    if any(text.startswith(char) for char in START_CHAR):
        counter = 1  # ignore first char -> is some kind of quote
        while counter < len(text):
            if text[counter] == "\\":
                counter += 1
            elif text[counter] == text[0] or (
                text[0] == SMART_OPEN and text[counter] == SMART_CLOSE
            ):
                break
            counter += 1
        else:
            return text.split(None, 1)

        key = remove_escapes(text[1:counter].strip())
        rest = text[counter + 1 :].strip()
        if not key:
            key = text[0] + text[0]
        return list(filter(None, [key, rest]))
    return text.split(None, 1)


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




@megux.on_message(filters.command(["save", "savenote"], Config.TRIGGER))
async def save_notes(c: megux, m: Message):
    if m.reply_to_message is None and len(input_str(m)) < 2:
        await m.reply_text("Você precisa escrever o nome da nota.", quote=True)
        return
    chat_id = m.chat.id
    user_id = m.from_user.id
    if not await check_rights(chat_id, user_id, "can_change_info"):
        return await m.reply("Você não tem permissões suficientes para alterar as notas do grupo.")
    db = get_collection(f"CHAT_NOTES {m.chat.id}")
    args = m.text.html.split(maxsplit=1)
    split_text = f"{args[1]}"
    trigger = split_text.lower()

    
    if m.reply_to_message and m.reply_to_message.photo:
        file_id = m.reply_to_message.photo.file_id
        raw_data = (
            m.reply_to_message.caption.html
            if m.reply_to_message.caption is not None
            else None
        )
        note_type = "photo"
    elif m.reply_to_message and m.reply_to_message.document:
        file_id = m.reply_to_message.document.file_id
        raw_data = (
            m.reply_to_message.caption.html
            if m.reply_to_message.caption is not None
            else None
        )
        note_type = "document"
    elif m.reply_to_message and m.reply_to_message.video:
        file_id = m.reply_to_message.video.file_id
        raw_data = (
            m.reply_to_message.caption.html
            if m.reply_to_message.caption is not None
            else None
        )
        note_type = "video"
    elif m.reply_to_message and m.reply_to_message.audio:
        file_id = m.reply_to_message.audio.file_id
        raw_data = (
            m.reply_to_message.caption.html
            if m.reply_to_message.caption is not None
            else None
        )
        note_type = "audio"
    elif m.reply_to_message and m.reply_to_message.animation:
        file_id = m.reply_to_message.animation.file_id
        raw_data = (
            m.reply_to_message.caption.html
            if m.reply_to_message.caption is not None
            else None
        )
        note_type = "animation"
    elif m.reply_to_message and m.reply_to_message.sticker:
        file_id = m.reply_to_message.sticker.file_id
        raw_data = split_text[1] if len(split_text) > 1 else None
        note_type = "sticker"
    else:
        file_id = None
        raw_data = split_text[1]
        note_type = "text"

    check_note = await db.find_one({"name": trigger})
    if check_note:
        await db.delete_one({"chat_id": chat_id, "name": trigger})
        await db.insert_one({"chat_id": chat_id, "name": trigger, "raw_data": raw_data, "file_id": file_id, "type": note_type})
    else:
        await db.insert_one({"chat_id": chat_id, "name": trigger, "raw_data": raw_data, "file_id": file_id, "type": note_type})
    await m.reply(f"A nota <code>{trigger}</code> foi salva com sucesso!")


@megux.on_message(filters.command("notes", Config.TRIGGER))
async def get_all_chat_note(c: megux, m: Message):
    db = get_collection(f"CHAT_NOTES {m.chat.id}")
    chat_id = m.chat.id
    reply_text = "<b>Notas para esse chat:</b>\n\n"
    all_notes = db.find()          
    async for note_s in all_notes:
        keyword = note_s["name"]
        reply_text += f" - <code>#{keyword}</code> \n"
    text += "\n\nVocê pode obter essas notas digitando <code>/get nomedanota</code>(não ativo)"
    if not await db.find_one():
        await m.reply_text("Notas não encontradas para esse chat.", quote=True)
    else:
        await m.reply_text(reply_text, quote=True)

