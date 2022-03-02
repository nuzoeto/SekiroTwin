import re

import httpx
import requests
from pyrogram import Client, filters, types
from pyrogram.types import Message

from megumin import megux


@Client.on_message(filters.command("cat", prefixes=["/", "!"]))
async def random_cat_commands(c: Client, m: types.Message):
    async with httpx.AsyncClient() as client:
        r = await client.get("https://api.thecatapi.com/v1/images/search")
    if not r.status_code == 200:
        return await m.reply_text(f"<b>Error!</b> <code>{r.status_code}</code>")
    cat = r.json
    await m.reply_photo(cat()[0]["url"], caption= "__Miau!__")


@Client.on_message(filters.command("neko", prefixes=["/", "!"]))
async def random_neko_command(c: Client, m: types.Message):
    while True:
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get("https://nekos.life/")
            midia = re.findall(
                r"<meta property=\"og:image\" content=\"(.*)\"/>", r.text
            )[0]
            return await m.reply_photo(midia)
        except BaseException:
            pass


@Client.on_message(filters.command("dog", prefixes=["/", "!"]))
async def random_dog_commands(c: Client, m: types.Message):
    async with httpx.AsyncClient() as client:
        r = await client.get("https://api.thedogapi.com/v1/images/search")
    if not r.status_code == 200:
        return await m.reply_text(
            f"<b>Error!</b> <code>{r.status_code}</code>", parse_mode="html"
        )
    cat = r.json
    await m.reply_photo(cat()[0]["url"], caption="__Au au!__")


@megux.on_message(filters.command("baka", prefixes=["/", "!"]))
async def baka_(_, message: Message):
    r = requests.get("https://nekos.life/api/v2/img/baka")
    g = r.json().get("url")
    await message.reply_animation(g)


@megux.on_message(filters.command(["wall", "wallpaper"], prefixes=["/", "!"]))
async def baka_(_, message: Message):
    r = requests.get("https://nekos.life/api/v2/img/wallpaper")
    g = r.json().get("url")
    await megux.send_document(message.chat.id, g, caption="__Send by:__ @WhiterKangBOT")


@megux.on_message(filters.command(["bird", "passaro"], prefixes=["/", "!"]))
async def bird_photo(c: megux, m: Message):
   http = httpx.AsyncClient()
   r = await http.get("http://shibe.online/api/birds")
   bird = r.json()
   await m.reply_photo(bird[0], caption="🐦")
