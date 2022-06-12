##
#

from io import BytesIO

from aiohttp import ClientSession
from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

aiohttpsession = ClientSession()


@megux.on_message(filters.command("carbon", prefixes=["/", "!"]))
async def carbon_func(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(
            "__Responda uma mensagem para carbonizar o texto.__"
        )
    if not message.reply_to_message.text:
        return await message.reply_text(
            "__Você precisa responder a um texto para carbonizar.__"
        )
    m = await message.reply_text("`Preparando carbon`")
    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit("__Uploading...__")
    await megux.send_document(message.chat.id, carbon, caption="__Made by:__ @WhiterKangBOT")
    await m.delete()
    carbon.close()


@megux.on_message(filters.command("carbon -img", prefixes=["/", "!"]))
async def carbon_func(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(
            "__Responda uma mensagem para carbonizar o texto.__"
        )
    if not message.reply_to_message.text:
        return await message.reply_text(
            "__Você precisa responder a um texto para carbonizar.__"
        )
    m = await message.reply_text("`Preparando carbon`")
    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit("__Uploading...__")
    await message.reply_photo(carbon, caption="__Made by:__ @WhiterKangBOT")
    await m.delete()
    carbon.close()


async def make_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with aiohttpsession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image
