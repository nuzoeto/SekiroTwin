from pyrogram import filters 
from pyrogram.types import Message 

from megumin import megux, Config
from megumin.utils import get_collection 


@megux.on_message(filters.command("afk"))
async def afk_cmd(_, m: Message):
    AFK_STATUS = get_collection(f"_AFK {m.from_user.id}")
    await AFK_STATUS.drop()
    await AFK_STATUS.insert_one({"_afk": "on"}) 
    await m.reply(f"{m.from_user.first_name} agora está AFK!")


@megux.on_message(filters.group & ~filters.bot, group=2)
async def rem_afk(c: megux, m: Message):
    if not m.from_user:
        return

    if "afk" in m.text:
        return 

    AFK_STATUS = get_collection(f"_AFK {m.from_user.id}") 

    user_afk = await AFK_STATUS.find_one({"_afk": "on"})

    if not user_afk:
        return
    else:

        await AFK.drop()
        await m.reply_text(f"{m.from_user.first_name} não está mais AFK!")

    
@megux.on_message(filters.group & ~filters.bot, group=3)
async def afk_mentioned(c: megux, m: Message):
    if m.reply_to_message and m.reply_to_message.from_user:
        AFK = get_collection(f"_AFK {m.reply_to_message.from_user.id}")
        user_afk = await AFK_STATUS.find_one({"_afk": "on"})
        if not user_afk:
            return 
        else:
            await message.reply(f"{m.from_user.first_name} está AFK!")
