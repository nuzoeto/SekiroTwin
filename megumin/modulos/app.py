import bs4
import aiohttp

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton 

from megumin import megux, Config
from megumin.utils.decorators import input_str

@megux.on_message(filters.command(["app"], Config.TRIGGER))
async def app(c: megux, message: Message):
    try:
        i = await message.reply("`Procurando...`")
        app_name = "+".join(message.text.split(" "))
        async with aiohttp.ClientSession() as ses, ses.get(
                f"https://play.google.com/store/search?q={app_name}&c=apps") as res:
            result = bs4.BeautifulSoup(await res.text(), "lxml")

        found = result.find("div", class_="vWM94c")
        if found:
            app_name = found.text
            app_dev = result.find("div", class_="LbQbAe").text
            app_rating = result.find(
                "div", class_="TT9eCd").text.replace("star", "")
            _app_link = result.find("a", class_="Qfxief")['href']
            app_icon = result.find("img", class_="T75of bzqKMd")['src']
        else:
            app_name = result.find("span", class_="DdYX5").text
            app_dev = result.find("span", class_="wMUdtb").text
            app_rating = result.find("span", class_="w2kbF").text
            _app_link = result.find("a", class_="Si6A0c Gy4nib")['href']
            app_icon = result.find("img", class_="T75of stzEZd")['src']

        app_dev_link = (
            "https://play.google.com/store/apps/developer?id="
            + app_dev.replace(" ", "+")
        )
        app_link = "https://play.google.com" + _app_link

        app_details = f"[📲]({app_icon}) **{app_name}**\n\n"
        app_details += f"`Developer :` [{app_dev}]({app_dev_link})\n"
        app_details += f"`Rating :` {app_rating} ⭐️\n"
        app_details += f"`Features :` [View in Play Store]({app_link})"
        await i.edit(app_details, disable_web_page_preview=False)
    except IndexError:
        await message.edit("No result found in search. Please enter **Valid app name**")
    except Exception as err:
        await message.err(err)

