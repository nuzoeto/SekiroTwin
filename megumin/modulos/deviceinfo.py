from gpytranslate import Translator
from pyrogram import filters
from pyrogram.types import Message

from megumin import megux, Config
from megumin.utils import disableable_dec, is_disabled, http, tld, device_info, search
from megumin.utils.decorators import input_str

tr = Translator()

@megux.on_message(filters.command(["deviceinfo", "d"], Config.TRIGGER))
@disableable_dec("deviceinfo")
async def deviceinfo(c: megux, m: Message):
    if await is_disabled(m.chat.id, "deviceinfo"):
        return
    if input_str(m):
        name = input_str(m) 
        searchi = f"{name}".replace(" ", "+")
        get_search_api = search(searchi)
        if get_search_api == None:
            return await m.reply("<code>Não encontrei esse dispositivo!!</code> <i>:(</i>")    
        name = get_search_api["name"]
        img = get_search_api["image"]
        link = get_search_api["link"]
        id = get_search_api["id"]
        try:
            get_device_api = device_info(link)
            name_cll = name or None
            s1 = get_device_api["processor"]
            s1_name = "Processador"
            s2 = get_device_api["ram"]
            s2_name = "Memoria Ram"
            s3 = get_device_api["wifi"]
            s3_name = "Banda Wi-Fi"
            s4 = get_device_api["connection"]
            s4_name = "Conexão Movel"
            s5 = get_device_api["battery"]
            s5_name = "Bateria"
            await m.reply(f"<b>Foto Device</b>: {img}\n<b>URL Fonte:</b>: https://www.gsmarena.com/{id}.php\n\n<b>- Aparelho</b>:  <i>{name_cll}</i>\n<b>- {s1_name}</b>: <i>{s1}</i>\n<b>- {s2_name}</b>: <i>{s2}</i>\n<b>- {s3_name}</b>: <i>{s3}</i>\n<b>- {s4_name}</b>: <i>{s4}</i>\n<b>- {s5_name}</b>: <i>{s5}</i>\n\n<b>Descrição</b>: {description}", disable_web_page_preview=False)
        except Exception as err:
            return await m.reply(f"Não consegui obter resultados sobre o aparelho. O gsmarena pode estar offline. <i>Erro</i>: <b>{err}</b>")
    else:
        return await m.reply("Não consigo advinhar o dispositivo!! woobs!!")
