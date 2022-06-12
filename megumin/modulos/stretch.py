import html
import random
import re

from pyrogram import filters
from pyrogram.errors import BadRequest
from pyrogram.types import Message

from megumin import megux, Config 
from megumin.utils.decorators import input_str 


@megux.on_message(filters.command("stretch", Config.TRIGGER))
async def stretch(c: megux, m: Message):
    if input_str(m):
        text = m.text.split(maxsplit=1)[1]
    else:
        if m.reply_to_message:
            text = m.reply_to_message.text or m.reply_to_message.caption
        else:
            return await m.reply("`Vou esticar o Vento?!`")
    reply = re.sub(
        r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэёö])",
        (r"\1" * random.randint(3, 12)),
        f"{text}",
        )
    try:
        await m.reply_text(f"{html.escape(reply)}")
    except BadRequest:
        return 
