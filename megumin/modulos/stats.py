import os
from pyrogram import filters
from pyrogram.types import Message 

from megumin import megux
from megumin.utils import get_collection

USERS = get_collection("USERS")
GROUPS = get_collection("GROUPS")

@megux.on_message(filters.command(["neofetch", "sys", "stats"]))
async def get_stats(_, message):
    os.system("neofetch --stdout > neofetch.txt")
    i = open("neofetch.txt", "r")
    read_file = i.read()
    neofetch = (f'''
----------[Neofetch]----------
{read_file}
''')
    i.close()
    stats = (f'''```
{neofetch}
```''')
    await message.reply_text(stats)


@megux.on_message(filters.command(["status"]))
async def status_(_, m: Message):
    user_id = m.from_user.id
    if not is_dev(user_id):
        return
    glist = await GROUPS.estimated_document_count()
    ulist = await USERS.estimated_document_count()
    await m.reply(f"**♬🎷【 Bot Status 】●♪**\n\n**Users**: __{ulist}__\n**Groups**: __{glist}__")  
