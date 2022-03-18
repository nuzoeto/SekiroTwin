from pyrogram import filters
from pyrogram.types import Message

from megumin import megux
from megumin.utils import check_bot_rights, check_rights


@megux.on_message(filters.command("pin", prefixes=["/", "!"]))
async def pin_(_, message: Message):
    chat_id = message.chat.id
    ids_chat = str(chat_id).replace("-100", "")
    if not await check_rights(chat_id, message.from_user.id, "can_pin_messages"):
        await message.reply("Você não tem direitos administrativos suficientes para fazer fixar/desafixar mensagens!")
        return
    if not await check_bot_rights(chat_id, "can_pin_messages"):
        await message.reply("Não consigo fixar mensagens aqui! Verifique se sou administrador e posso fixar mensagens.")
        return
    if not message.reply_to_message:
        await message.reply("Responda a uma mensagem para que eu possa fixa-la")
        return
    await message.reply_to_message.pin()
    await message.reply(f"""__Eu fixei</b> <a href='t.me/c/{ids_chat}/{message.reply_to_message.message_id}'>esta mensagem</a>.__""", disable_web_page_preview=True, disable_notification=True)


@megux.on_message(filters.command("loudpin", prefixes=["/", "!"]))
async def pin_(_, message: Message):
    chat_id = message.chat.id
    ids_chat = str(chat_id).replace("-100", "")
    if not await check_rights(chat_id, message.from_user.id, "can_pin_messages"):
        await message.reply("Você não tem direitos administrativos suficientes para fazer fixar/desafixar mensagens!")
        return
    if not await check_bot_rights(chat_id, "can_pin_messages"):
        await message.reply("Não consigo fixar mensagens aqui! Verifique se sou administrador e posso fixar mensagens.")
        return
    if not message.reply_to_message:
        await message.reply("Responda a uma mensagem para que eu possa fixa-la")
        return
    await message.reply_to_message.pin()
    await message.reply(f"""__Eu fixei</b> <a href='t.me/c/{ids_chat}/{message.reply_to_message.message_id}'>esta mensagem</a> e notifiquei todos os membros.__""", disable_web_page_preview=True, disable_notification=False)


@megux.on_message(filters.command("unpin", prefixes=["/", "!"]))
async def unpin_(_, message: Message):
    chat_id = message.chat.id
    ids_chat = str(chat_id).replace("-100", "")
    if not await check_rights(chat_id, message.from_user.id, "can_pin_messages"):
        await message.reply("Você não tem direitos administrativos suficientes para fazer fixar/desafixar mensagens!")
        return
    if not await check_bot_rights(chat_id, "can_pin_messages"):
        await message.reply("Não consigo fixar mensagens aqui! Verifique se sou administrador e posso fixar mensagens.")
        return
    if not message.reply_to_message:
        await message.reply("`Responda a uma mensagem para que eu possa desfixa-la`")
        return
    await message.reply_to_message.unpin()
    await message.reply(f"""__Eu desfixei</b> <a href='t.me/c/{ids_chat}/{message.reply_to_message.message_id}'>esta mensagem</a>.__""", disable_web_page_preview=True)
