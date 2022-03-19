import time

from pyrogram import filters
from pyrogram.errors import PeerIdInvalid, UserIdInvalid, UsernameInvalid
from pyrogram.types import Message

from megumin import megux
from megumin.utils import (
    check_bot_rights,
    check_rights,
    is_admin,
    is_dev,
    is_self,
    sed_sticker,
)


@megux.on_message(filters.command("banc", prefixes=["/", "!"]))
async def _ban_channel(_, message: Message):
  chat_id = message.chat.id
  if not check_rights(chat_id, message.from_user.id, "can restrict members"):
    await message.reply("Você não tem direitos administrativos suficientes para banir/desbanir usuários!")
    return
  replied = message.reply_to_message
  if not replied:
    return await message.reply("__Responda a uma mensagem.__")
    if not replied.sender_chat:
      return await message.reply("A mensagem respondida nao e de um canal.")
      id_ = replied.sender_chat.id
      title_ = replied.sender_chat.title
      username_ = replied.sender_chat.username
      text = f"#BAN_CHANNEL\nNome: {title_}\nID: {id_}"
      if username_:
        text += f"Username: {username_}"
        try:
          await megux.ban_chat_member(chat_id, id_)
          await message.reply(text)
      except Exception as e:
        await m.reply(f"Error: {e}")
  
  
