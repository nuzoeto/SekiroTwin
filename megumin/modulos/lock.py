from pyrogram import filters 
from pyrogram.types import Message 

from megumin import megux, Config
from megumin.utils import get_collection
from megumin.utils.decorators import input_str 

LOCK_TYPES = [
    "audio",
    "link",
    "video"
]

@megux.on_message(filters.command("lock", Config.TRIGGER))
async def lock(c: megux, m: Message):
    lock = input_str(m)
