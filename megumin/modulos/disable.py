from pyrogram import filters
from pyrogram.types import Message

from megumin import megux, Config
from megumin.utils import get_collection
from megumin.utils.decorators import input_str 


DISABLED = get_collection("DISABLED")
CMDS = [
    "ping"
]


@megux.on_message(filters.command("disable", Config.TRIGGER))
async def disble_cmd(_, m: Message):
    gid = m.chat.id
    query = input_str(m)
    found = await DISABLED.find_one({'_id': gid, '_cmd': query})
    if found:
        return await m.reply("__Comando já desativado!__") 
    else:
    dis_cmd = await DISABLED.insert_one({'_id': gid, '_cmd': query})
    if not query in CMDS:
        return await m.reply("__Qual comando você deseja desativar?__")
