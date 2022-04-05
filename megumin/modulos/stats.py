import os
from pyrogram import filters

from megumin import megux 


@megux.on_message(filters.command(["stats", "sys"]))
async def get_stats(_, message):
    os.system("neofetch --stdout > neofetch.txt")
    i = open("neofetch.txt", "r")
    read_file = i.read()
    neofetch = (f'''
----------[Neofetch]----------
{read_file}
''')
    i.close()
    stats = (f'''
```
{neofetch}
```''')
    await message.reply_text(stats)
