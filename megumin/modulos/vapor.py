import html
import random
import re

from pyrogram import filters
from pyrogram.errors import BadRequest
from pyrogram.types import Message

from megumin import megux, trg
from megumin.utils import get_collection 

DISABLED = get_collection("DISABLED")

@megux.on_message(filters.command("vapor", trg))
async def vapor(c: megux, m: Message):
    gid = m.chat.id 
    query = "vapor"
    off = await DISABLED.find_one({"_id": gid, "_cmd": query})
    if off:
        return
    text = m.text.split(maxsplit=1)[1]
    if not text and m.reply_to_message:
        if (m.reply_to_message.text or m.reply_to_message.caption) is not None:
            text = m.reply_to_message.text or m.reply_to_message.caption 
        else:
            await m.reply_text("`Vou vaporizar o vento?!`")
            return

    if not text and not m.reply_to_message:
        await m.reply_text("`Vou vaporizar o vento?!`")
        return

    reply = []
    for charac in text:
        if 0x21 <= ord(charac) <= 0x7F:
            reply.append(chr(ord(charac) + 0xFEE0))
        elif ord(charac) == 0x20:
            reply.append(chr(0x3000))
        else:
            reply.append(charac)

    vaporized_text = "".join(reply)

    try:
        if m.reply_to_message:
            await m.reply_to_message.reply_text(f"{html.escape(vaporized_text)}")
        else:
            await m.reply_text(f"{html.escape(vaporized_text)}")
    except BadRequest:
        return
