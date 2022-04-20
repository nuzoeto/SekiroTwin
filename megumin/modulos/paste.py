import httpx

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux 

http = httpx.AsyncClient()


@megux.on_message(filters.command("paste", prefixes=["/", "!"]))
async def nekobin(c: megux, m: Message):
    if m.reply_to_message:
        if m.reply_to_message.document:
            tfile = m.reply_to_message
            sm = await m.reply_text("<i>Processando...</i>")
            to_file = await tfile.download()
            with open(to_file, "rb") as fd:
                mean = fd.read().decode("UTF-8")
        if m.reply_to_message.text:
            mean = m.reply_to_message.text

        url = "https://nekobin.com/api/documents"
        r = await http.post(url, json={"content": mean})
        url = f"https://nekobin.com/{r.json()['result']['key']}"
        await sm.edit(f"<b>Nekobin [URL]({url})</b>", disable_web_page_preview=True)
    else:
        await m.reply_text("Por favor, responda a um texto ou documento para colar o conteúdo.")


