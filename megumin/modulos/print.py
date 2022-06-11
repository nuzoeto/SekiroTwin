import httpx

from httpx import HTTPError
from pyrogram import filters
from pyrogram.types import Message

from megumin import megux
from megumin.utils import get_collection, get_string  


http = httpx.AsyncClient()

@megux.on_message(filters.command("print", prefixes=["/","!"]))
async def prints(c: megux, message: Message):
    DISABLED = get_collection(f"DISABLED {message.chat.id}")
    query = "print"
    off = await DISABLED.find_one({"_cmd": query})
    if off:
        return 
    msg = message.text
    the_url = msg.split(" ", 1)
    wrong = False

    if len(the_url) == 1:
        if message.reply_to_message:
            the_url = message.reply_to_message.text
            if len(the_url) == 1:
                wrong = True
            else:
                the_url = the_url[1]
        else:
            wrong = True
    else:
        the_url = the_url[1]

    if wrong:
        await message.reply_text(await get_string(message.chat.id, "NO_ARGS_PRINT"))
        return
    if "xvideos.com" or "xvideos.com.br" == the_url:
         return await m.reply((await get_string(m.chat.id, "ERROR_PRINT_DNS")).format(the_url))

    try:
        sent = await message.reply_text(await get_string(message.chat.id, "TAKING_PRINT"))
        res_json = await cssworker_url(target_url=the_url)
    except BaseException as e:
        await message.reply(f"<b>Failed due to:</b> <code>{e}</code>")
        return

    if res_json:
        # {"url":"image_url","response_time":"147ms"}
        image_url = res_json["url"]
        if image_url:
            try:
                await message.reply_photo(image_url)
                await sent.delete()
            except BaseException:
                # if failed to send the message, it's not API's
                # fault.
                # most probably there are some other kind of problem,
                # for example it failed to delete its message.
                # or the bot doesn't have access to send media in the chat.
                return
        else:
            await message.reply(
                "Couldn't get url value, most probably API is not accessible."
            )
    else:
        await message.reply("Failed because API is not responding, try again later.")


@megux.on_message(filters.command(["google", "search"], prefixes=["/","!"]))
async def prints_google(c: megux, message: Message):
    msg = message.text
    the_url = msg.split(" ", 1)
    wrong = False

    if len(the_url) == 1:
        if message.reply_to_message:
            the_url = message.reply_to_message.text
            if len(the_url) == 1:
                wrong = True
            else:
                the_url = the_url[1]
        else:
            wrong = True
    else:
        the_url = the_url[1]

    if wrong:
        await message.reply_text("Uso:</b> <code>/search texto</code> - Tira uma captura de tela da pesquisa especificada.")
        return

    try:
        sent = await message.reply_text(await get_string(message.chat.id, "TAKING_PRINT"))
        search_google = f"{the_url}".replace(" ", "+")
        res_json = await cssworker_url(target_url=f"https://www.google.com/search?q={search_google}&oq={search_google}")
    except BaseException as e:
        await message.reply(f"<b>Failed due to:</b> <code>{e}</code>")
        return

    if res_json:
        # {"url":"image_url","response_time":"147ms"}
        image_url = res_json["url"]
        if image_url:
            try:
                await message.reply_photo(image_url)
                await sent.delete()
            except BaseException:
                # if failed to send the message, it's not API's
                # fault.
                # most probably there are some other kind of problem,
                # for example it failed to delete its message.
                # or the bot doesn't have access to send media in the chat.
                return
        else:
            await message.reply(
                "Couldn't get url value, most probably API is not accessible."
            )
    else:
        await message.reply("Failed because API is not responding, try again later.")


async def cssworker_url(target_url: str):
    url = "https://htmlcsstoimage.com/demo_run"
    my_headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
    }

    data = {
        "url": target_url,
        "render_when_ready": False,
        "viewport_width": 1280,
        "viewport_height": 720,
        "device_scale": 1,
    }

    try:
        resp = await http.post(url, headers=my_headers, json=data)
        return resp.json()
    except HTTPError:
        return None
