import calendar
from datetime import datetime

from pyrogram import filters 
from pyrogram.types import Message 

from megumin import megux 
from megumin.utils.decorators import input_str

@megux.on_message(filters.command("cal"))
async def cal_(_, message: Message):
    if not message.text.split():
        msg = await message.reply("__Procurando...__")
        try:
            today = datetime.today()
            input_ = calendar.month(today.year, today.month)
            await msg.edit(f"```{input_}```")
        except Exception as e:
            await message.reply(e)
        return
    if "|" not in message.text.split():
        await message.reply("both year and month required!")
        return
    msg = await message.reply("__Procurando...__")
    year, month = (message.text.split("|", maxsplit=1))
    try:
        input_ = calendar.month(int(year.strip()), int(month.strip()))
        await message.reply(f"```{input_}```")
    except Exception as e:
        await msg.edit(e)
