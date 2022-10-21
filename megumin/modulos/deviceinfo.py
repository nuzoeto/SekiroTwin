from pyrogram import filters
from pyrogram.types import Message

from megumin import megux, Config
from megumin.utils import disableable_dec, is_disabled, http
from megumin.utils.decorators import input_str

@megux.on_message(filters.command("deviceinfo", Config.TRIGGER))
@disableable_dec("deviceinfo")
async def deviceinfo(c: megux, m: Message):
    if await is_disabled(m.chat.id, "deviceinfo"):
        return
    if input_str(m):
        name = input_str(m) 
        search = f"{name}".replace(" ", "%")
        get_search_api = (await http.get(f"http://api.davitudo.tk/search/motog5")).json()
        if get_search_api == '[]':
            return await m.reply("<code>Não encontrei esse dispositivo!!</code> <i>:(</i>")
        id = get_search_api[0]['url']
        img = get_search_api[0]['img']
        get_device_api = (await http.get(f"http://api.davitdo.tk/device/{id}"))
        try:
            name_cll = get_device_api['title']
            await m.reply(f"<b>Foto Device</b>: {img}\n<b>URL Fonte:</b>: https://www.gsmarena.com/{id}", disable_web_page_preview=False)
        except Exception:
            return await m.reply("Não consegui obter resultados sobre o aparelho. O gsmarena pode estar offline.")
    else:
        return await m.reply("Não consigo advinhar o dispositivo!! woobs!!")
