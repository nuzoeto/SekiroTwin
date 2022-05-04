import rapidjson
import httpx
import html
import asyncio 

from pyrogram import filters 
from pyrogram.types import Message 

from megumin import megux 

timeout = httpx.Timeout(120)
http = httpx.AsyncClient(http2=True, timeout=timeout)


@megux.on_message(filters.command("short"))
async def short(c: megux, m: Message):
    if len(m.command) < 2:
        return await m.reply_text("Erro.\n\nUso: /short (url)\n\n\nFaça isso para encurtar uma url.")
    else:
        url = m.command[1]
        if not url.startswith("http"):
            url = "http://" + url
        try:
            short = m.command[2]
            shortRequest = await http.get(
                f"https://api.1pt.co/addURL?long={url}&short={short}"
            )
            info = rapidjson.loads(shortRequest.content)
            short = info["short"]
            return await m.reply_text(f"<code>https://1pt.co/{short}</code>")
        except IndexError:
            shortRequest = await http.get(f"https://api.1pt.co/addURL?long={url}")
            info = rapidjson.loads(shortRequest.content)
            short = info["short"]
            return await m.reply_text(f"<i>https://1pt.co/{short}</i>")
        except Exception as e:
            return await m.reply_text(f"<b>{e}</b>")
