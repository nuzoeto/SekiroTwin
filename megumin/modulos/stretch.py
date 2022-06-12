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
    if not text and m.reply_to_message:
        if (m.reply_to_message.text or m.reply_to_message.caption) is not None:
             text = m.reply_to_message.text or m.reply_to_message.caption
        else:
             await m.reply_text("`Vou esticar o vento?!`")
             return
    
    if not text and not m.reply_to_message:
        await m.reply_text("Eu preciso de texto...")
        return
    
        reply = re.sub(
            r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])",
            (r"\1" * random.randint(3, 10)),
            text,
        )
    
        try:
            if m.reply_to_message:
                await m.reply_to_message.reply_text(reply)
            else:
                await m.reply_text(reply)
        except BadRequest as err:
            return await m.reply(err)
