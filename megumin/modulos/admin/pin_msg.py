from pyrogram import filters
from pyrogram.types import Message

from megumin import megux
from megumin.utils import check_bot_rights, check_rights


@megux.on_message(filters.command("pin"))
async def pin_(_, message: Message):
    chat_id = message.chat.id
    msg = message.reply_to_message or message
    if not await check_rights(chat_id, message.from_user.id, "can_pin_messages"):
        await reply("`Você não tem as seguintes permissões: **Can pin messages**")
        return
    if not await check_bot_rights(chat_id, "can_pin_messages"):
        await message.reply("`Eu não tenho as seguintes permissões: **Can pin messages**")
        return
    if not message.reply_to_message:
        await message.reply("Responda a uma mensagem para que eu possa fixa-la")
        return
    await message.reply_to_message.pin()
    await message.reply(f"""Eu fixei</b> <a href='t.me/{message.chat.username}/{message.reply_to_message.message_id}'>esta mensagem</a>.""", disable_web_page_preview=True, disable_notification=True)


@megux.on_message(filters.command("loudpin"))
async def pin_(_, message: Message):
    chat_id = message.chat.id
    msg = message.reply_to_message or message
    if not await check_rights(chat_id, message.from_user.id, "can_pin_messages"):
        await reply("`Você não tem as seguintes permissões: **Can pin messages**")
        return
    if not await check_bot_rights(chat_id, "can_pin_messages"):
        await message.reply("`Eu não tenho as seguintes permissões: **Can pin messages**")
        return
    if not message.reply_to_message:
        await message.reply("Responda a uma mensagem para que eu possa fixa-la")
        return
    await message.reply_to_message.pin()
    await message.reply(f"""Eu fixei</b> <a href='t.me/{message.chat.username}/{message.reply_to_message.message_id}'>esta mensagem</a> e notifiquei todos os membros.""", disable_web_page_preview=True, disable_notification=False)


@megux.on_message(filters.command("unpin"))
async def unpin_(_, message: Message):
    chat_id = message.chat.id
    if not await check_rights(chat_id, message.from_user.id, "can_pin_messages"):
        await reply("Você não tem as seguintes permissões: **Can pinned messages")
        return
    if not await check_bot_rights(chat_id, "can_pin_messages"):
        await message.reply("Eu não tenho as seguintes permissões: **Can pineed messages**")
        return
    if not message.reply_to_message:
        await message.reply("`Responda a uma mensagem para que eu possa desfixa-la`")
        return
    await message.reply_to_message.unpin()
    await message.reply(f"""Eu desfixei</b> <a href='t.me/{message.chat.username}/{message.reply_to_message.message_id}'>esta mensagem</a>.""", disable_web_page_preview=True)
