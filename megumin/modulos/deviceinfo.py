from pyrogram import filters
from pyrogram.types import Message

from megumin import megux, Config
from megumin.utils import disableable_dec, is_disabled, http
from megumin.utils.decorators import input_str

@megux.on_message(filters.command(["deviceinfo", "di"], Config.TRIGGER))
@disableable_dec("deviceinfo")
async def deviceinfo(c: megux, m: Message):
    if await is_disabled(m.chat.id, "deviceinfo"):
        return
    if input_str(m):
        name = input_str(m) 
        search = f"{name}".replace(" ", "+")
        get_search_api = (await http.get(f"http://api.davitudo.tk/search/{search}")).json()
        if get_search_api == '[]':
            return await m.reply("<code>Não encontrei esse dispositivo!!</code> <i>:(</i>")        
        id = get_search_api[0]['url']
        img = get_search_api[0]['img']
        link_base = f"http://api.davitudo.tk/device/{id}"
        try:
            get_device_api = (await http.get(link_base)).json()
            name_cll = get_device_api['title'] or None
            s1 = get_device_api['spec_detail'][0]['specs'][0]['value'] 
            s1_name = get_device_api['spec_detail'][0]['specs'][0]['name'] 
            s2 = get_device_api['spec_detail'][1]['specs'][0]['value']
            s2_name = get_device_api['spec_detail'][1]['specs'][0]['name']
            s3 = get_device_api['spec_detail'][2]['specs'][3]['value']
            s3_name = get_device_api['spec_detail'][2]['specs'][3]['name']
            s4 = get_device_api['spec_detail'][5]['specs'][1]['value']
            s4_name = get_device_api['spec_detail'][5]['specs'][1]['name']
            await m.reply(f"<b>Foto Device</b>: {img}\n<b>URL Fonte:</b>: https://www.gsmarena.com/{id}\n\n<b>- Aparelho</b>:  <i>{name_cll}</i>\n<b>- {s1_name}</b>: <i>{s1}</i>\n<b>- {s2_name}</b>: <i>{s2}</i>\n<b>- {s3_name}</b>: <i>{s3}</i>\n<b>- {s4_name}</b>: <i>{s4}</i>", disable_web_page_preview=False)
        except Exception as err:
            return await m.reply(f"Não consegui obter resultados sobre o aparelho. O gsmarena pode estar offline. <i>Erro</i>: <b>{err}</b>")
    else:
        return await m.reply("Não consigo advinhar o dispositivo!! woobs!!")
