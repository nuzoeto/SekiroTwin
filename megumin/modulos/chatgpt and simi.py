import requests 
import openai

from pyrogram import filters 
from pyrogram.types import Message 
from pyrogram.enums import ChatType

from megumin import megux, Config
from megumin.utils import get_collection, get_string 

openai.api_key = Config.API_CHATGPT

async def generate_response(text):
    response = await openai.Completion.create(
        engine='text-davinci-003',  # Especifique o modelo do ChatGPT a ser usado
        prompt=question,  # O texto de entrada ou pergunta para o modelo
        max_tokens=50,  # O número máximo de tokens para a resposta gerada
        n=1,  # O número de respostas a serem geradas
        stop=None,  # Um token opcional para indicar o fim da resposta gerada
    )

    answer = response.choices[0].text.strip()  # Obtém a resposta gerada do ChatGPT
    return answer


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


@megux.on_message(filters.command("ask", Config.TRIGGER))
async def chatgpt(c: megux, m: Message):
    args = m.text.split()[:1]
    text = " ".join(args)
    response = await generate_response(text)
    await m.reply(response)
