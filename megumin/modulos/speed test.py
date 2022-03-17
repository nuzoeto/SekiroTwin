import speedtest
import os
import wget
import sys

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

@megux.on_message(filters.command("speedtest"))
async def test_speed(c: megux, m: Message):
    running = await m.reply("`Rodando speedtest...`") 
    string = "<b>Teste de velocidade</b>\n\n<b>🌀 Nome:</b> `{name}`\n<b>🏁 País:</b> `{country}`\n<b>💻 ISP:</b> `{isp}`\n<b>🌐 Host:</b> <code>{host}</code>\n\n<b>🏓 Latência:</b> <code>{ping} ms</code>\n<b>⬇️ Download:</b> <code>{download} Mbps</code>\n<b>⬆️ Upload:</b> <code>{upload} Mbps</code>"
    sent = string.format(host="", ping="", download="", upload="", isp="", name="", country="")
    test = speedtest.Speedtest()
    bs = test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()  
    path = wget.download(result["share"]) 
    response = await m.reply_photo(
        photo=path, caption=sent
    )
    await sent.edit_text(
        string.format(
            host=bs["sponsor"], ping=int(bs["latency"]), download="", upload="", isp=result["client"]["isp"], name=result["server"]["name"], country=result["server"]["country"]
        )
    )
    dl = round(test.download() / 1024 / 1024, 2)
    await sent.edit_text(
        string.format(
            host=bs["sponsor"], ping=int(bs["latency"]), download=dl, upload="", isp=result["client"]["isp"], name=result["server"]["name"], country=result["server"]["country"]
        )
    )
    ul = round(test.upload() / 1024 / 1024, 2)
    await sent.edit_text(
        string.format(
            host=bs["sponsor"], ping=int(bs["latency"]), download=dl, upload=ul, isp=result["client"]["isp"], name=result["server"]["name"], country=result["server"]["country"]
        )
    )
    

@megux.on_message(filters.command("speed"))
async def test_speed(c: megux, m: Message):
    test = speedtest.Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()  
    path = wget.download(result["share"]) 
    response = await m.reply_photo(
        photo=path, caption="Getting Stats!"
    )
