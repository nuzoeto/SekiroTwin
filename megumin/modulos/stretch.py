import html
import random
import re

from pyrogram import filters
from pyrogram.errors import BadRequest
from pyrogram.types import Message

from megumin import megux
from megumin.utils.decorators import input_str 


@megux.on_message(filters.command("stretch"))
async def stretch(c: megux, m: Message):
    text = input_str(m)
    if not text or m.reply_to_message.text:
        return await m.reply("`Vou esticar o vento?!`")
    if m.reply_to_message.text or m.reply_to_message.caption:
        text = message.reply_to_message.text or m.reply_to_message.caption 
    reply = re.sub(
            r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])",
            (r"\1" * random.randint(3, 10)),
            text,
        )
    await m.reply(reply)

