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
async def create_new_fed(c: megux, m: Message):
    if m.chat.type != ChatType.PRIVATE:
        return await m.reply("You can your federation in my PM, not in a group.")
    if not (len(m.command) >= 2):
        return await m.reply("Give your federation a name!")
    if (len(' '.join(m.command[1:])) > 60):
        return await m.reply("Your fed must be smaller than 60 words.")
    fed_name = ' '.join(m.command[1:])
    fed_id = str(uuid.uuid4())
    owner_id = m.from_user.id 
    await new_fed(m, fed_name, fed_id, owner_id)
