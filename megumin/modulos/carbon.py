##
#

from io import BytesIO

from aiohttp import ClientSession
from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

aiohttpsession = ClientSession()


@megux.on_message(filters.command("carbon"))
async def carbon_func(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(
            "`Responda uma mensagem para carbonizar o texto.`"
        )
    if not message.reply_to_message.text:
        return await message.reply_text(
            "`Você precisa responder a um texto para carbonizar.`"
        )
    m = await message.reply_text("`Preparando carbon`")
    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit("`Uploading...`")
    await megux.send_document(message.chat.id, carbon, caption="__Made by:__ @WhiterKangBot")
    await m.delete()
    carbon.close()


async def make_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with aiohttpsession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.jpg"
    return image
