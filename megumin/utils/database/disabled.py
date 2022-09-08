from megumin.utils import get_collection

from pyrogram import filters
from pyrogram.types import Message

from typing import List

DISABLABLE_CMDS: List[str] = []


async def is_disabled(gid: int, query: str) -> bool:
    DISABLED = get_collection(f"DISABLED {gid}")
    off = await DISABLED.find_one({"_cmd": query})
    return bool(off)


def disableable_dec(command):
    print(
        "[%s] Adding %s to the disableable commands...",
        megux.__name__,
        command,
    )

    if command not in DISABLABLE_CMDS:
        DISABLABLE_CMDS.append(command)

    def decorator(func):
        async def wrapper(c: megux, message: Message, *args, **kwargs):
            chat_id = message.chat.id

            check = await is_disabled(chat_id, command)
            if check and not await filters.admin(c, message):
                return

            return await func(bot, message, *args, **kwargs)

        return wrapper

    return decorator
