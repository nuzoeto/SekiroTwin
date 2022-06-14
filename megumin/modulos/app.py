import bs4
import aiohttp

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton 

from megumin import megux, Config
from megumin.utils.decorators import input_str

@megux.on_message(filters.command(["app"], Config.TRIGGER))
async def app(c: megux, message: Message):
    try:
        msg = await message.reply("`Searching...`")
        query_app = input_str(message)
        async with aiohttp.ClientSession() as ses, ses.get(
            f"https://play.google.com/store/search?q={query_app}&c=apps"
        ) as res:
            result = bs4.BeautifulSoup(
                await res.text(),
                "lxml",
                parse_only=bs4.SoupStrainer("div", class_="ipRz4"),
            )

        query_app = result.find("div", class_="vWM94c").text
        app_dev = result.find("div", class_="LbQbAe").text
        app_dev_link = (
            "https://play.google.com/store/apps/developer?id="
            + app_dev.replace(" ", "+")
        )
        app_rating = (
            result.find("div", class_="TT9eCd")["aria-label"]
            .replace("Rated ", "⭐️ ")
            .replace(" out of ", "/")
            .replace(" stars", "", 1)
            .replace(" stars", "⭐️")
            .replace("five", "5")
        )
        app_link = "https://play.google.com" + result.find("a", class_="Qfxief")["href"]
        app_icon = result.find("img", class_="T75of bzqKMd")["src"]

        app_details = f"[📲]({app_icon}) **{query_app}**\n\n"
        app_details += f"`Developer :` [{app_dev}]({app_dev_link})\n"
        app_details += f"`Rating :` {app_rating}\n"
        app_details += f"`Features :` [View in Play Store]({app_link})"
        await message.reply(app_details, disable_web_page_preview=False)
    except IndexError:
        await msg.edit("No result found in search. Please enter **Valid app name**")

