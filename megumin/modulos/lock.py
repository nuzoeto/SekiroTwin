from pyrogram import filters 
from pyrogram.types import Message 

from megumin import megux, Config
from megumin.utils import get_collection
from megumin.utils.decorators import input_str 

LOCK_TYPES = ["audio", "link", "video"]


@megux.on_message(filters.command("lock", Config.TRIGGER))
async def lock(c: megux, m: Message):
    LOCK = get_collection(f"LOCK {m.chat.id}")
    res = input_str(m)
    await LOCK.insert_one({"lock" res})


