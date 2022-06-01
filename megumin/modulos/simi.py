import requests 

from pyrogram import filters 
from pyrogram.types import Message 

from megumin import megux 
from megumin.utils import get_collection 
from megumin.utils.decorators import input_str 

@megux.on_message(filters.command("simi", Config.TRIGGER))
async def simi_(_, m: Message):
    text_ = input_str(m)
    API = f"https://api.simsimi.net/v2/?text={text_}&lc=pt&cf=false"
    r = requests.get(API).json()    
    await m.reply(r["success"])
