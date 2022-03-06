import httpx

from pyrogram import filters
from pyrogram.errors import BadRequest
from pyrogram.types import Message

from megumin import megux

http = httpx.AsyncClient()

@megux.on_message(filters.command("token", prefixes=["/", "!"]))
async def getbotinfo(c: megux, m: Message):
    if len(m.command) == 1:
        return await m.reply_text("Por favor, especifique um token de bot.")
        )
    text = m.text.split(maxsplit=1)[1]
    req = await http.get(f"https://api.telegram.org/bot{text}/getme")
    fullres = req.json()
    if not fullres["ok"]:
        await m.reply("Token de bot inválido.")
    else:
        res = fullres["result"]
        get_bot_info_text = "<b>Nome</b>: <code>{botname}</code> \n<b>Nome de usuário</b>: <code>{botusername}</code> \n<b>ID</b>: <code>{botid}</code>"
    await m.reply(
        get_bot_info_text.format(
            botname=res["first_name"], botusername=res["username"], botid=res["id"]
        ),
        reply_to_message_id=m.message_id,
    )
