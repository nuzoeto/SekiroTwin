import bs4
import aiohttp

from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton 

from megumin import megux, Config
from megumin.utils.decorators import input_str

@megux.on_message(filters.command(["app"], Config.TRIGGER))
async def app(c: megux, message: Message):
    try:
        msg = await message.reply("`Procurando...`")
        app_name = " ".join(message.text.split()[1:])
        async with aiohttp.ClientSession() as ses, ses.get(
            f"https://play.google.com/store/search?q={app_name}&c=apps"
        ) as res:
            result = bs4.BeautifulSoup(
                await res.text(),
                "lxml",
                parse_only=bs4.SoupStrainer("div", class_="ipRz4"),
            )

        app_name = result.find("div", class_="vWM94c").text
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

        app_details = f"**{app_name}**\n\n"
        app_details += f"<i>Desenvolvedor:</i> [{app_dev}]({app_dev_link})\n"
        app_details += f"<i>Classificação:</i> {app_rating}\n"
        app_details += f"`Features :` [View in Play Store]({app_link})"
        keyboard = [[InlineKeyboardButton(text="Ver na PlayStore", url=app_link)]]
        await message.reply_photo(photo=app_icon, caption=app_details, reply_markup=InlineKeyboardMarkup(keyboard))
        await msg.delete()
    except IndexError:
        await message.edit("No result found in search. Please enter **Valid app name**")
    except Exception as err:
        await message.err(err)
