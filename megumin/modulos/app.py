#Ported from https://github.com/fnixdev/KannaX-Plugins/blob/master/plugins//app.py
import bs4
import requests

from pyrogram import filters 
from pyrogram.types import Message 

from megumin import megux, Config
from megumin.utils.decorators import input_str

@megux.on_message(filters.command(["app"], Config.TRIGGER))
async def app(c: megux, message: Message):
    try:
        msg = await message.reply("`Procurando...`")
        app_name = " ".join(message.text.split()[1:])
        remove_space = app_name.split(" ")
        final_name = "+".join(remove_space)
        page = requests.get(
            f"https://play.google.com/store/search?q={final_name}&c=apps"
        )
        soup = bs4.BeautifulSoup(page.content, "lxml", from_encoding="utf-8")
        results = soup.findAll("div", "ZmHEEd")
        app_name = (
            results[0].findNext("div", "Vpfmgd").findNext("div", "WsMG1c nnK0zc").text
        )
        app_dev = results[0].findNext("div", "Vpfmgd").findNext("div", "KoLSrc").text
        app_dev_link = (
            "https://play.google.com"
            + results[0].findNext("div", "Vpfmgd").findNext("a", "mnKHRc")["href"]
        )
        app_rating = (
            results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "pf5lIe")
            .find("div")["aria-label"]
        )
        app_link = (
            "https://play.google.com"
            + results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "vU6FJ p63iDd")
            .a["href"]
        )
        app_icon = (
            results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "uzcko")
            .img["data-src"]
        )
        app_details = "<a href='" + app_icon + "'>📲&#8203;</a>"
        app_details += " <b>" + app_name + "</b>"
        app_details += "\n\n<b>Desenvolvedor :</b> <a href='" + app_dev_link + "'>"
        app_details += app_dev + "</a>"
        app_details += "\n<b>Avaliação :</b> " + app_rating.replace(
            "Rated ", "⭐️ "
        ).replace(" out of ", "/").replace(" stars", "", 1).replace(
            " stars", "⭐️"
        ).replace(
            "five", "5"
        )
        app_details += (
            "\n<b>Recursos :</b> <a href='"
            + app_link
            + "'>View in Play Store</a>"
        )
        await msg.edit(
            app_details, disable_web_page_preview=False, parse_mode=ParseMode.HTML
        )
    except IndexError:
        await message.reply("Nenhum resultado encontrado na pesquisa. Digite **Nome do aplicativo válido**")
    except Exception as err:
        await message.reply(err)
