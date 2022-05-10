import httpx

from pyrogram import filters
from pyrogram.types import Message 

from yarl import URL
from megumin import megux, Config


http = httpx.AsyncClient()


@megux.on_message(filters.command("ip", Config.TRIGGER))
async def ip_cmd_(c: megux, m: Message):
    if len(m.text.split()) > 1:
        text = m.text.split(maxsplit=1)[1]
        url: str = URL(text).host or text

        r = await http.get("http://ip-api.com/json/" + url)
        req = r.json()
        x = ""
        for i in req:
            x += "<b>{}</b>: <code>{}</code>\n".format(i.title(), req[i])
        await m.reply_text(x)
    else:
        await m.reply_text("Você deve especificar uma url, ex.: <code>/ip example.com</code>")
