import rapidjson
import httpx
import asyncio 
import requests
import math

from bs4 import BeautifulSoup
from babel.dates import format_datetime

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup



from megumin import megux, Config
from megumin.utils import tld
from megumin.utils.decorators import input_str 


http = httpx.AsyncClient()


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


DEVICE_LIST = "https://raw.githubusercontent.com/androidtrackers/certified-android-devices/master/by_device.json"


@megux.on_message(filters.command(["twrp"], prefixes=["/", "!"]))
async def twrp(c: megux, m: Message):
    if not len(m.command) == 2:
        message = "Por favor, escreva seu codinome nele, ou seja, <code>/twrp herolte</code>"
        await m.reply_text(message)
        return
    device = m.command[1]
    url = await http.get(f"https://eu.dl.twrp.me/{device}/")
    if url.status_code == 404:
        await m.reply_text("TWRP atualmente não está disponível para <code>{}</code>".format(device))
    else:
        message = "<b>Último recovery TWRP para {}</b>\n".format(device)
        page = BeautifulSoup(url.content, "lxml")
        date = page.find("em").text.strip()
        message += "<b>Atualizado em:</b> <code>{}</code>\n".format(date)
        trs = page.find("table").find_all("tr")
        row = 2 if trs[0].find("a").text.endswith("tar") else 1
        for i in range(row):
            download = trs[i].find("a")
            dl_link = f"https://eu.dl.twrp.me{download['href']}"
            dl_file = download.text
            size = trs[i].find("span", {"class": "filesize"}).text
        message += "<b>Tamanho:</b> <code>{}</code>\n".format(size)
        message += "<b>Arquivo:</b> <code>{}</code>".format(dl_file.upper())
        keyboard = [[InlineKeyboardButton(text="Download", url=dl_link)]]
        await m.reply_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


@megux.on_message(filters.command(["magisk"], prefixes=["/", "!"]))
async def magisk(c: megux, m: Message):
    repo_url = "https://raw.githubusercontent.com/topjohnwu/magisk-files/master/"
    text = await tld(m.chat.id, "MAGISK_STRING")
    for magisk_type in ["stable", "beta", "canary"]:
        fetch = await http.get(repo_url + magisk_type + ".json")
        data = rapidjson.loads(fetch.content)
        text += (
            f"<b>{magisk_type.capitalize()}</b>:\n"
            f'<a href="{data["magisk"]["link"]}" >Magisk - V{data["magisk"]["version"]}</a>'
            f' | <a href="{data["magisk"]["note"]}" >Changelog</a> \n'
        )
    await m.reply_text(text, disable_web_page_preview=True)


@megux.on_message(filters.command(["device", "whatis"], prefixes=["/", "!"]))
async def device_(_, message: Message):
    if not len(message.command) == 2:
        await message.reply(await tld(message.chat.id, "DEVICE_NO_CODENAME"))
        return
    msg = await message.reply(await tld(message.chat.id, "COM_2"))
    getlist = requests.get(DEVICE_LIST).json()
    target_device = message.text.split()[1].lower()
    if target_device in list(getlist):
        device = getlist.get(target_device)
        text = ""
        for x in device:
            brand = x['brand']
            name = x['name']
            model = x['model']
            text += (await tld(message.chat.id, "DEVICE_SUCCESS")).format(brand, name, model, target_device)
            text += "\n\n"
        await msg.edit(text)
    else:
        await msg.edit((await tld(message.chat.id, "DEVICE_NOT_FOUND")).format(target_device))
        await asyncio.sleep(5)
        await msg.delete()


@megux.on_message(filters.command(["los", "lineageos"], Config.TRIGGER))
async def los(c: megux, m: Message):
    device = input_str(m)
    if not device:
        return await m.reply(await tld(m.chat.id, "LOS_NO_QUERY"))
    fetch = await http.get(f"https://download.lineageos.org/api/v1/{device}/nightly/*")
    if fetch.status_code == 200 and len(fetch.json()["response"]) != 0:
        usr = rapidjson.loads(fetch.content)
        response = usr["response"][-1]
        filename = response["filename"]
        url = response["url"]
        buildsize_a = response["size"]
        buildsize_b = convert_size(int(buildsize_a))
        version = response["version"]
        build_time = response["datetime"]
        romtype = response["romtype"]

        text = (await tld(m.chat.id, "ANDROID_DOWNLOAD")).format(filename, url)
        text += (await tld(m.chat.id, "ANDROID_TYPE")).format(romtype)
        text += (await tld(m.chat.id, "ANDROID_SIZE")).format(buildsize_b)
        text += (await tld(m.chat.id, "ANDROID_VERSION")).format(version)
        text += (await tld(m.chat.id, "ANDROID_DATE")).format(format_datetime(build_time))
        keyboard = [[InlineKeyboardButton(text=await tld(m.chat.id, "ANDROID_BNT_DOWNLOAD"), url=url)]]
        await m.reply(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        return await m.reply(await tld(m.chat.id, "ANDROID_NOT_FOUND"))


@megux.on_message(filters.command("pe", Config.TRIGGER))
async def pixelexperience(c: megux, m: Message):
    try:
        args = m.text.split()
        device = args[1].lower()
    except IndexError:
        device = ""
    try:
        atype = args[2].lower()
    except IndexError:
        atype = "twelve"  
    if device == "":
        return await m.reply(await tld(m.chat.id, "PE_NO_QUERY"))

    fetch = await http.get(
        f"https://download.pixelexperience.org/ota_v5/{device}/{atype}"
    ) 
    if fetch.status_code == 200:
        response = rapidjson.loads(fetch.content)
        if response["error"]:
            return await m.reply(await tld(m.chat.id, "ANDROID_NOT_FOUND"))
        filename = response["filename"]
        url = response["url"]
        buildsize_a = response["size"]
        buildsize_b = convert_size(int(buildsize_a))
        version = response["version"]
        build_time = response["datetime"]

        text = (await tld(m.chat.id, "ANDROID_DOWNLOAD")).format(filename, url)
        text += (await tld(m.chat.id, "ANDROID_SIZE")).format(buildsize_b)
        text += (await tld(m.chat.id, "ANDROID_VERSION")).format(version)
        text += (await tld(m.chat.id, "ANDROID_DATE")).format(format_datetime(build_time))
        keyboard = [[InlineKeyboardButton(text=await tld(m.chat.id, "ANDROID_BNT_DOWNLOAD"), url=url)]]
        await m.reply(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        return await m.reply(await tld(m.chat.id, "ANDROID_NOT_FOUND"))


@megux.on_message(filters.command(["crdroid", "crd"], Config.TRIGGER))
async def crdroid(c: megux, m: Message):
    device = input_str(m)
    if not device:
        return await m.reply(await tld(m.chat.id, "CRD_NO_QUERY"))

    if device == "x00t":
        device = "X00T"

    if device == "x01bd":
        device = "X01BD"

    fetch = await http.get(
        f"https://raw.githubusercontent.com/crdroidandroid/android_vendor_crDroidOTA/11.0/{device}.json"
    )
    if fetch.status_code in [500, 504, 505]:
        return await m.reply(await tld(m.chat.id, "ANDROID_GIT_ERROR"))
    if fetch.status_code in [400, 404]:
        return await m.reply(await tld(m.chat.id, "ANDROID_NOT_FOUND"))
    if fetch.status_code == 200:
        try:
            usr = rapidjson.loads(fetch.content)
            response = usr["response"]
            filename = response[0]["filename"]
            url = response[0]["download"]
            version = response[0]["version"]
            maintainer = response[0]["maintainer"]
            size_a = response[0]["size"]
            size_b = convert_size(int(size_a))
            build_time = response[0]["timestamp"]
            romtype = response[0]["buildtype"]

            text = (await tld(m.chat.id, "ANDROID_DOWNLOAD")).format(filename, url)
            text += (await tld(m.chat.id, "ANDROID_TYPE")).format(romtype)
            text += (await tld(m.chat.id, "ANDROID_SIZE")).format(size_b)
            text += (await tld(m.chat.id, "ANDROID_VERSION")).format(version)
            text += (await tld(m.chat.id, "ANDROID_DATE")).format(format_datetime(build_time))
            text += (await tld(m.chat.id, "ANDROID_MAINTAINER")).format(maintainer)
            keyboard = [[InlineKeyboardButton(text=await tld(m.chat.id, "ANDROID_BNT_DOWNLOAD"), url=url)]]
            await m.reply(text, reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)
            return 
        except ValueError:
            text = await tld(m.chat.id, "ANDROID_ERR_OTA")
            await m.reply(text)


@megux.on_message(filters.command(["evo", "evox"], Config.TRIGGER))
async def evo(c: megux, m: Message):
    device = input_str(m)
    if not device:
        return await m.reply(await tld(m.chat.id, "EVO_NO_QUERY"))
    if device == "x00t":
        device = "X00T"

    if device == "x01bd":
        device = "X01BD"

    fetch = await http.get(
        f"https://raw.githubusercontent.com/Evolution-X-Devices/official_devices/master/builds/{device}.json"
    )

    if fetch.status_code in [500, 504, 505]:
        await message.reply(await tld(m.chat.id, "ANDROID_GIT_ERROR"))
        return

    if fetch.status_code == 200:
        try:
            usr = rapidjson.loads(fetch.content)
            filename = usr["filename"]
            url = usr["url"]
            version = usr["version"]
            maintainer = usr["maintainer"]
            maintainer_url = usr["telegram_username"]
            size_a = usr["size"]
            size_b = convert_size(int(size_a))
  
            text = (await tld(m.chat.id, "ANDROID_DOWNLOAD")).format(filename, url)
            text += (await tld(m.chat.id, "ANDROID_SIZE")).format(size_b)
            text += (await tld(m.chat.id, "ANDROID_VERSION")).format(version)
            text += (await tld(m.chat.id, "ANDROID_MAINTAINER")).format(f"<a href='{maintainer_url}'>{maintainer}</a>")
            keyboard = [[InlineKeyboardButton(text=await tld(m.chat.id, "ANDROID_BNT_DOWNLOAD"), url=url)]]
            await m.reply(text, reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)
            return 
        except ValueError:
            text = await tld(m.chat.id, "ANDROID_ERR_OTA")
            await m.reply(text)
            return

    elif fetch.status_code in [404, 400]:
        text = await tld(m.chat.id, "ANDROID_NOT_FOUND")
        await m.reply(text)
        return


@megux.on_message(filters.command("phh", Config.TRIGGER))
async def phh(_, m: Message):
    fetch = await http.get(
        "https://api.github.com/repos/phhusson/treble_experimentations/releases/latest"
    )

    if fetch.status_code in [500, 504, 505]:
        await message.reply(await tld(m.chat.id, "ANDROID_GIT_ERROR"))
        return

    usr = rapidjson.loads(fetch.content)
    text = await tld(m.chat.id, "ANDROID_PHH")
    text += (await tld(m.chat.id, "ANDROID_PHH_NAME")).format(usr["name"])
    text += (await tld(m.chat.id, "ANDROID_PHH_VERSION")).format(usr["tag_name"])
    text += (await tld(m.chat.id, "ANDROID_PHH_DATE")).format(usr["published_at"])
    for i in range(len(usr)):
        try:
            name = usr["assets"][i]["name"]
            url = usr["assets"][i]["browser_download_url"]
            text += f"<a href='{url}'>{name}</a>\n"
        except IndexError:
            continue

    await m.reply(text, disable_web_page_preview=True)
