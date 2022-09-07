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
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, User

from megumin import megux, Config
from megumin.utils import get_collection, check_rights, tld, add_user_count
from megumin.utils.decorators import input_str

BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\(buttonurl:(?:/{0,2})(.+?)(:same)?\))")

SMART_OPEN = "“"
SMART_CLOSE = "”"
START_CHAR = ("'", '"', SMART_OPEN)


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




@megux.on_message(filters.command(["filter", "savefilter", "addfilter"], Config.TRIGGER))
async def save_notes(c: megux, m: Message):
    chat_id = m.chat.id
    user_id = m.from_user.id
    if not await check_rights(chat_id, user_id, "can_change_info"):
        return await m.reply("Você não tem permissoes suficientes para adicionar/remover filtros", quote=True)
    if m.reply_to_message is None and len(input_str(m)) < 2:
        await m.reply_text("Você Precisa dar um nome ao filtro.", quote=True)
        return
    db = get_collection(f"CHAT_FILTERS {m.chat.id}")
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
        filter_type = "photo"
    elif m.reply_to_message and m.reply_to_message.document:
        file_id = m.reply_to_message.document.file_id
        raw_data = (
            m.reply_to_message.caption.html
            if m.reply_to_message.caption is not None
            else None
        )
        filter_type = "document"
    elif m.reply_to_message and m.reply_to_message.video:
        file_id = m.reply_to_message.video.file_id
        raw_data = (
            m.reply_to_message.caption.html
            if m.reply_to_message.caption is not None
            else None
        )
        filter_type = "video"
    elif m.reply_to_message and m.reply_to_message.audio:
        file_id = m.reply_to_message.audio.file_id
        raw_data = (
            m.reply_to_message.caption.html
            if m.reply_to_message.caption is not None
            else None
        )
        filter_type = "audio"
    elif m.reply_to_message and m.reply_to_message.voice:
        file_id = m.reply_to_message.voice.file_id
        raw_data = (
            m.reply_to_message.caption.html
            if m.reply_to_message.caption is not None
            else None
        )
        filter_type = "voice"
    elif m.reply_to_message and m.reply_to_message.animation:
        file_id = m.reply_to_message.animation.file_id
        raw_data = (
            m.reply_to_message.caption.html
            if m.reply_to_message.caption is not None
            else None
        )
        filter_type = "animation"
    elif m.reply_to_message and m.reply_to_message.sticker:
        file_id = m.reply_to_message.sticker.file_id
        raw_data = split_text[1] if len(split_text) > 1 else None
        filter_type = "sticker"
    else:
        if m.reply_to_message and m.reply_to_message.text:
            file_id = None
            raw_data = m.reply_to_message.text
            filter_type = "text"
        else:
            await m.reply("<i>Responda algo para salvar o filtro.</i>")
            return

    check_note = await db.find_one({"name": trigger})
    if check_note:
        await db.delete_one({"chat_id": chat_id, "name": trigger})
        await db.insert_one({"chat_id": chat_id, "name": trigger, "raw_data": raw_data, "file_id": file_id, "type": filter_type})
    else:
        await db.insert_one({"chat_id": chat_id, "name": trigger, "raw_data": raw_data, "file_id": file_id, "type": filter_type})
    await m.reply("Filtro {} foi adicionado em <b>{}.</b>".format(trigger, m.chat.title))
    await m.stop_propagation()


@megux.on_message(filters.command("filters", Config.TRIGGER) & filters.group)
async def get_all_chat_note(c: megux, m: Message):
    if not await check_rights(m.chat.id, m.from_user.id, "can_change_info"):
        return
    db = get_collection(f"CHAT_FILTERS {m.chat.id}")
    chat_id = m.chat.id
    reply_text = "<b>Lista de filtros em {}:</b>\n\n".format(m.chat.title)
    all_filters = db.find()          
    async for filter_s in all_filters:
        keyword = filter_s["name"]
        reply_text += f" • <code>{keyword}</code> \n"
    if not await db.find_one():
        await m.reply_text("<i>Esse chat não tem filtros.</i>", quote=True)
    else:
        await m.reply_text(reply_text, quote=True)
    await m.stop_propagation()
        
        
@megux.on_message(filters.command(["rmfilter", "delfilter", "stop"]))
async def rmnote(c: megux, m: Message):
    if not await check_rights(m.chat.id, m.from_user.id, "can_change_info"):
        return
    args = m.text.html.split(maxsplit=1)
    trigger = args[1].lower()
    chat_id = m.chat.id
    db = get_collection(f"CHAT_FILTERS {chat_id}")
    check_note = await db.find_one({"chat_id": chat_id, "name": trigger})
    if check_note:
        await db.delete_one({"chat_id": chat_id, "name": trigger})
        await m.reply_text(
            "Filtro {} Removido em {}".format(trigger, m.chat.title), quote=True
        )
    else:
        await m.reply_text(
            "Esse não é um filtro ativo - use o comando /filters para todos os filtros ativos.".format(trigger), quote=True
        )
    await m.stop_propagation()

        
@megux.on_message(filters.command(["resetfilters", "clearfilters"]))
async def clear_notes(c: megux, m: Message):
    chat_id = m.chat.id
    if not await check_rights(chat_id, m.from_user.id, "can_change_info"):
        return
    db = get_collection(f"CHAT_FILTERS {chat_id}")
    check_note = await db.find_one()
    if check_note:
        await db.drop()
        await m.reply_text(
            "Todas os filtros desse chat foram apagadas.", quote=True
        )
    else:
        await m.reply_text(
            "O grupo não tem filtros.", quote=True
        )  
    await m.stop_propagation()


@megux.on_message(
    (filters.group | filters.private) & filters.text & filters.incoming, group=2
)
async def serve_filter(c: megux, m: Message):
    chat_id = m.chat.id
    db = get_collection(f"CHAT_FILTERS {m.chat.id}")
    if m and m.from_user:
        await add_user_count(chat_id, m.from_user.id)
        dbu = get_collection(f"TOTAL_GROUPS {user_id}")
        await dbu.drop()
    text = m.text
    target_msg = m.reply_to_message or m

    all_filters = db.find()
    async for filter_s in all_filters:
        keyword = filter_s["name"]
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, text, flags=re.IGNORECASE):
            data, button = button_parser(filter_s["raw_data"])
            if filter_s["type"] == "text":
                await target_msg.reply_text(
                    data,
                    quote=True,
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(button)
                    if len(button) != 0
                    else None,
                )
            elif filter_s["type"] == "photo":
                await target_msg.reply_photo(
                    filter_s["file_id"],
                    quote=True,
                    caption=data if not None else None,
                    reply_markup=InlineKeyboardMarkup(button)
                    if len(button) != 0
                    else None,
                )
            elif filter_s["type"] == "document":
                await target_msg.reply_document(
                    filter_s["file_id"],
                    quote=True,
                    caption=data if not None else None,
                    reply_markup=InlineKeyboardMarkup(button)
                    if len(button) != 0
                    else None,
                )
            elif filter_s["type"] == "video":
                await target_msg.reply_video(
                    filter_s["file_id"],
                    quote=True,
                    caption=data if not None else None,
                    reply_markup=InlineKeyboardMarkup(button)
                    if len(button) != 0
                    else None,
                )
            elif filter_s["type"] == "audio":
                await target_msg.reply_audio(
                    filter_s["file_id"],
                    quote=True,
                    caption=data if not None else None,
                    reply_markup=InlineKeyboardMarkup(button)
                    if len(button) != 0
                    else None,
                )
            elif filter_s["type"] == "voice":
                await target_msg.reply_voice(
                    filter_s["file_id"],
                    quote=True,
                    caption=data if not None else None,
                    reply_markup=InlineKeyboardMarkup(button)
                    if len(button) != 0
                    else None,
                )
            elif filter_s["type"] == "animation":
                await target_msg.reply_animation(
                    filter_s["file_id"],
                    quote=True,
                    caption=data if not None else None,
                    reply_markup=InlineKeyboardMarkup(button)
                    if len(button) != 0
                    else None,
                )
            elif filter_s["type"] == "sticker":
                await target_msg.reply_sticker(
                    filter_s["file_id"],
                    quote=True,
                    reply_markup=InlineKeyboardMarkup(button)
                    if len(button) != 0
                    else None,
                )
    await m.stop_propagation()                
                
