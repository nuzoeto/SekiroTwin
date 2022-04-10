import rapidjson
import httpx

from bs4 import BeautifulSoup

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup


from megumin import megux 


http = httpx.AsyncClient()


@megux.on_message(filters.command(["twrp"]))
async def twrp(c: megux, m: Message):
    if not len(m.command) == 2:
        message = "Please write your codename into it, i.e <code>/twrp herolte</code>"
        await m.reply_text(message)
        return
    device = m.command[1]
    url = await http.get(f"https://eu.dl.twrp.me/{device}/")
    if url.status_code == 404:
        await m.reply_text(f"TWRP currently is not avaliable for <code>{device}</code>")
    else:
        message = f"<b>Último recovery TWRP para {device}</b>\n"
        page = BeautifulSoup(url.content, "lxml")
        date = page.find("em").text.strip()
        message += f"<b>Atualizado em:</b> <code>{date}</code>\n"
        trs = page.find("table").find_all("tr")
        row = 2 if trs[0].find("a").text.endswith("tar") else 1
        for i in range(row):
            download = trs[i].find("a")
            dl_link = f"https://eu.dl.twrp.me{download['href']}"
            dl_file = download.text
            size = trs[i].find("span", {"class": "filesize"}).text
        message += f"<b>Tamanho:</b> <code>{size}</code>\n"
        message += f"<b>Arquivo:</b> <code>{dl_file.upper()}</code>"
        keyboard = [[InlineKeyboardButton(text="Download", url=dl_link)]]
        await m.reply_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


@Client.on_message(filters.command(["magisk"]))
async def magisk(c: Client, m: Message):
    repo_url = "https://raw.githubusercontent.com/topjohnwu/magisk-files/master/"
    text = "<b>Últimos lançamentos do magisk</b>\n\n"
    for magisk_type in ["stable", "beta", "canary"]:
        fetch = await http.get(repo_url + magisk_type + ".json")
        data = rapidjson.loads(fetch.content)
        text += (
            f"<b>{magisk_type.capitalize()}</b>:\n"
            f'<a href="{data["magisk"]["link"]}" >Magisk - V{data["magisk"]["version"]}</a>'
            f' | <a href="{data["magisk"]["note"]}" >Changelog</a> \n'
        )
    await m.reply_text(text, disable_web_page_preview=True)
