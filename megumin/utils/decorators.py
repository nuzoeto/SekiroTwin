# WhiterKang Bot
# Copyright (C) 2023 Davi
#
# This file is a part of < https://github.com/DaviTudoPlugins1234/WhiterKang/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/DaviTudoPlugins1234/WhiterKang/blob/master/LICENSE/>.

## WhiterKang Decorators
import logging

from typing import List, Optional

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux
from megumin.utils import is_disabled

DISABLABLE_CMDS: List[str] = []
INLINE_CMDS = {}
    

def input_str(message) -> str:
    return " ".join(message.text.split()[1:])

def disableable_dec(command):
    if command not in DISABLABLE_CMDS:
        logging.info(
            f"Adding {command} to the disableable commands...",
        )
        DISABLABLE_CMDS.append(command)

    def decorator(func):
        async def wrapper(c: megux, message: Message, *args, **kwargs):
            chat_id = message.chat.id

            check = await is_disabled(chat_id, command)
            if check and not await filters.admin(c, message):
                return

            return await func(c, message, *args, **kwargs)

        return wrapper

    return decorator

