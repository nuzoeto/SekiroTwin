import html
import random
import io
import re
import httpx

from pyrogram import filters
from pyrogram.errors import BadRequest
from pyrogram.types import Message

from megumin import megux, Config 
from megumin.utils.decorators import input_str 


http = httpx.AsyncClient()


@megux.on_message(filters.command("stretch", Config.TRIGGER))
async def stretch(c: megux, m: Message):
    if input_str(m):
        text = input_str(m)
    elif m.reply_to_message:
        text = m.reply_to_message.text or m.reply_to_message.caption
    else:
        return await m.reply("`Vou esticar o vento?!`")
    reply = re.sub(
        r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэёö])",
        (r"\1" * random.randint(3, 12)),
        f"{text}",
        )
    try:
        if len(reply) < 2950:
            await m.reply_text(f"{html.escape(reply)}")
        else:
            stretch = io.BytesIO(reply.encode())
            stretch.name = "stretch.txt"
            url = "https://nekobin.com/api/documents"
            r = await http.post(url, json={"content": stretch})
            url = f"https://nekobin.com/{r.json()['result']['key']}"
            await m.reply_document(stretch, caption=f"<b>Nekobin [URL]({url})")
    except BadRequest:
        return 
