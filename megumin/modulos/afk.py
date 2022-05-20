from pyrogram import filters 
from pyrogram.types import Message 

from megumin import megux, Config
from megumin.utils import get_collection 


@megux.on_message(filters.command("afk"))
async def setwarnlimit_cmd(_, m: Message):
    AFK_STATUS = get_collection(f"_AFK {m.from_user.id}")
    await AFK_STATUS.insert_one({"_id": m.from_user.id}) 
    await m.reply(f"{m.from_user.first_nane} agora está AFK!")
   



    
