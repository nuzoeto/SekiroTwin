from pyrogram import filters 
from pyrogram.types import Message 

from megumin import megux, Config
from megumin.utils import get_collection
from megumin.utils.decorators import input_str 

LOCK_TYPES = ["audio", "link", "video"]
LOCK_MODE = ["on"]

@megux.on_message(filters.command("lock", Config.TRIGGER))
async def lock(c: megux, m: Message):
    LOCKS_ = get_collection(f"LOCKED {m.chat.id}")
    on =  await LOCKS_.find_one({"lock": "on"})
    x = input_str(m)
    if x in LOCK_MODE:
        if not in on:
            await LOCKS_.insert_one({"lock": "on"})
        else:
            return await m.reply("comando já ativo")
    else:
        return await m.reply("insira um argumento valido **on**")


@megux.on_message(filters.command("locktype", Config.TRIGGER))
async def lock_type(c: megux, m: Message):
    data = input_str(m)
  
