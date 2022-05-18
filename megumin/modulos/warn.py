from pyrogram import filters 
from pyrogram.types import Message 

from megumin import megux, Config
from megumin.utils import get_collection, check_rights  
from megumin.utils.decorators import input_str 


ACTION = [
    "ban",
    "mute",
    "kick",
]

NUMBER = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
]



@megux.on_message(filters.command("setwarnlimit", Config.TRIGGER))
async def setwarnlimit_cmd(_, m: Message):
    LIMIT = get_collection(f"WARNS_LIMIT {m.chat.id}")
    chat_id = m.chat.id 
    check_admin = m.from_user.id  
    query = input_str(m)
    if m.chat.type == "private":
        return await m.reply("Esse comando é para ser usado em grupos.")
    else:
        if not query in NUMBER:
            return await m.reply("__Especifique um número de advertências valido, de 1 a 7.__")
        else:
            found = await LIMIT.find_one({"_warnslimit")
            if found:
                if await check_rights(chat_id, check_admin, "can_change_info"):
                    await LIMIT.update_one({"_warnslimit": query})
                    await m.reply(f" O número de advertência foi alterado para **{query}**")
                else:
                    return await m.reply("`Você precisa de permissão para fazer isso.`")
            else:
                if await check_rights(chat_id, check_admin, "can_change_info"):
                    await LIMIT.insert_one({"_warnslimit": query})
                    await m.reply(f"O número de advertência foi alterado para **{query}**")
                else: 
                    return await m.reply("`Você precisa de permissão para fazer isso`")

