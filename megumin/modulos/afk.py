from pyrogram import filters 
from pyrogram.types import Message 

from megumin import megux, Config
from megumin.utils import get_collection 


@megux.on_message(filters.command("afk", Config.TRIGGER))
async def afk(c: megux, m: Message):
    AFK_STATUS = get_collection(f"_AFK {m.from_user.id}")
    
