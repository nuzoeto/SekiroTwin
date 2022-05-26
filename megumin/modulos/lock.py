from pyrogram import filters 
from pyrogram.types import Message 

from megumin import megux, Config
from megumin.utils import get_collection
from megumin.utils.decorators import input_str 

LOCK_TYPES = ["audio", "link", "video"]

@megux.on_message(filters.command("lock", Config.TRIGGER))
async def lock(c: megux, m: Message):
    LOCKS_ = get_collection(f"LOCKED {m.chat.id}")
    await LOCKS_.insert_one({"lock": "on"})


@megux.on_message(filters.command("locktype", Config.TRIGGER))
async def lock_type(c: megux, m: Message):
    data = input_str(m)
