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
    if input_str(m):
        text = input_str(m)
    else:
        text = m.reply_to_message.text or m.reply_to_message.caption
    reply = re.sub(
        r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])",
        (r"\1" * random.randint(3, 10)),
        f"{text}",
        )
    await m.reply_text(f"{html.escape(reply)}")
