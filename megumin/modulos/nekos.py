import re

import httpx
import requests
from pyrogram import Client, filters, types
from pyrogram.types import Message

from megumin import megux
from megumin.utils.decorators import input_str


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
    qu = input_str(message)
    if qu:
        msg = await m.reply(f"<i>Searching wallpapers...</i> <b>{qu}</b>")
        results = requests.get(f"https://kuuhaku-api-production.up.railway.app/api/wallpaper?query={qu}")
        _json = results.json()['url']
        await megux.send_document(message.chat.id, document=_json)
        await msg.delete()
    

@megux.on_message(filters.command(["bird", "passaro"], prefixes=["/", "!"]))
async def bird_photo(c: megux, m: Message):
   http = httpx.AsyncClient()
   r = await http.get("http://shibe.online/api/birds")
   bird = r.json()
   await m.reply_photo(bird[0], caption="🐦")


@megux.on_message(filters.command(["rpanda", "redpanda", "red_panda"], prefixes=["/", "!"]))
async def redpanda_photo(c: megux, m: Message):
   http = httpx.AsyncClient()
   r = await http.get("https://some-random-api.ml/img/red_panda")
   rpanda = r.json()
   await m.reply_photo(rpanda["link"], caption="🐼")


@megux.on_message(filters.command(["panda"], prefixes=["/", "!"]))
async def panda_photo(c: megux, m: Message):
   http = httpx.AsyncClient()
   r = await http.get("https://some-random-api.ml/img/panda")
   panda = r.json()
   await m.reply_photo(panda["link"], caption="🐼")


@megux.on_message(filters.command(["fox", "raposa"], prefixes=["/", "!"]))
async def fox_photo(c: megux, m: Message):
   http = httpx.AsyncClient()
   r = await http.get("https://some-random-api.ml/img/fox")
   fox = r.json()
   await m.reply_photo(fox["link"], caption="O que a Raposa diz?")
