from pyrogram import filters
from pyrogram.types import Message

from megumin import megux
from megumin.utils import check_bot_rights, check_rights


@megux.on_message(filters.command("pin"))
async def pin_(_, message: Message):
    chat_id = message.chat.id
    msg = message.reply_to_message or message
    if not await check_rights(chat_id, message.from_user.id, "can_pin_messages"):
        await reply("`Você não tem permissão pra fazer isso`")
        return
    if not await check_bot_rights(chat_id, "can_pin_messages"):
        await message.reply("`Eu preciso de permissão para fixar mensagens`")
        return
    if not message.reply_to_message:
        await message.reply("`Responda a uma mensagem para que eu possa fixa-la`")
        return
    await message.reply_to_message.pin()
    await message.reply("Eu fixei a mensagem!")


@megux.on_message(filters.command("unpin"))
async def unpin_(_, message: Message):
    chat_id = message.chat.id
    if not await check_rights(chat_id, message.from_user.id, "can_pin_messages"):
        await reply("`Você não tem permissão pra fazer isso`")
        return
    if not await check_bot_rights(chat_id, "can_pin_messages"):
        await message.reply("`Eu preciso de permissão para desfixar mensagens`")
        return
    if not message.reply_to_message:
        await message.reply("`Responda a uma mensagem para que eu possa desfixa-la`")
        return
    await message.reply_to_message.unpin()
    await message.reply(f"""Eu desfixei a [mensagem](t.me/{message.chat.username}/{message.message_id})!""")
