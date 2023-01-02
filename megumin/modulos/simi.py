import requests 

from pyrogram import filters 
from pyrogram.types import Message 
from pyrogram.enums import ChatType

from megumin import megux, Config
from megumin.utils import get_collection, get_string 
 

@megux.on_message(filters.command("simi", Config.TRIGGER))
async def simi_(_, m: Message):
    DISABLED = get_collection(f"DISABLED {m.chat.id}")
    query = "simi"
    off = await DISABLED.find_one({"_cmd": query})
    if off:
        return
    text_ = m.text.split(maxsplit=1)[1]
    API = f"https://api.simsimi.net/v2/?text={text_}&lc=pt&cf=false"
    r = requests.get(API).json()  
    if r["success"] in "Eu não resposta. Por favor me ensine.":
        return await m.reply(await get_string(m.chat.id, "SIMI_NO_RESPONSE"))
    if r["success"]:
        return await m.reply(r["success"])
    else:
        return await m.reply(await get_string(m.chat.id, "SIMI_API_OFF"))


@megux.on_message(filters.command("chatboton", Config.TRIGGER))
async def on_chatbot(_, m: Message):
    CHATBOT_STATUS = get_collection("CHATBOT_STATUS")
    query = "on"
    id = m.from_user.id
    chat_id = m.chat.id
    configure = await CHATBOT_STATUS.update_one({"user_id": id, "chat_id": chat_id, {"$set": "status": query}}, upsert=True)
    await m.reply(f"Olá {m.from_user.mention}, Como posso lhe ajudar amigo(a)\nSobre o que quer conversar?\n, <b>Para parar a conversa<b> digite  <i>/chatbotstop</i>")  
 

@megux.on_message(filters.command("chatbotstop", Config.TRIGGER))
async def off_chatbot(_, m: Message):
    CHATBOT_STATUS = get_collection("CHATBOT_STATUS")
    query = "off"
    id = m.from_user.id
    chat_id = m.chat.id
    configure = await CHATBOT_STATUS.update_one({"user_id": id, "chat_id": chat_id, {"$set": "status": query}}, upsert=True)
    await m.reply("Assunto encerrado {m.from_user.first_name}")  
 

@megux.on_message(
    (filters.group | filters.private) & filters.text)
async def serve_filter(c: megux, m: Message):
    chat_id = m.chat.id
    uid = m.from_user.id
    db = get_collection(f"CHATBOT_STATUS")
    text = m.text

    all_configs = await db.find_one({"user_id": uid, "chat_id": m.chat.id, "status": "on"})
    if all_configs:
        API = f"https://api.simsimi.net/v2/?text={text}&lc=pt&cf=false"
        r = requests.get(API).json()  
        if r["success"] in "Eu não resposta. Por favor me ensine.":
            return await m.reply(await get_string(m.chat.id, "SIMI_NO_RESPONSE"))
        if r["success"]:
            return await m.reply(r["success"])
        else:
            return await m.reply(await get_string(m.chat.id, "SIMI_API_OFF"))
    else:
         pass
