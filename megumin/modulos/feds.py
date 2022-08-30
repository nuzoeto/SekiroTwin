import uuid 
import re
import os

from io import BytesIO


from megumin import megux, Config
from megumin.utils import new_fed

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatType


@megux.on_message(filters.command(["newfed", "fednew", "fnew"], Config.TRIGGER))
async def create_new_fed(m: Message, c: megux):
    if m.chat.type == (ChatType.SUPERGROUP, ChatType.GROUP):
        return await m.reply("You can your federation in my PM, not in a group.")
    if not (len(message.command) >= 2):
        return await message.reply("Give your federation a name!")
    if (len(' '.join(message.command[1:])) > 60):
        return await message.reply("Your fed must be smaller than 60 words.")
    fed_name = ' '.join(message.command[1:])
    fed_id = str(uuid.uuid4())
    owner_id = message.from_user.id 
    await new_fed(m, fed_name, fed_id, owner_id)
