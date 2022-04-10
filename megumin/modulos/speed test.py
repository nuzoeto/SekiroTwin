import speedtest
import os
import wget
import sys

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

@megux.on_message(filters.command("speedtest") & filters.user(1715384854))
async def test_speed(c: megux, m: Message):
    try:
        running = await m.reply("`Rodando Speedtest. . .`") 
        test = speedtest.Speedtest()
        bs = test.get_best_server()
        dl = round(test.download() / 1024 / 1024, 2)
        ul = round(test.upload() / 1024 / 1024, 2)
        test.results.share()
        result = test.results.dict()
        name = result["server"]["name"]
        host = bs["sponsor"]
        ping = bs["latency"]
        isp = result["client"]["isp"]   
        country = result["server"]["country"] 
        cc = result["server"]["cc"]
        path = wget.download(result["share"])
    except Exception as e:
        await m.err(text=e)
        return 
        response = await m.reply_photo(
            photo=path, caption=f"🌀 <b>Nome:</b> <code>{name}</code>\n🌐 <b>Host:</b> <code>{host}</code>\n🏁 <b>País:</b> <code>{country}, {cc}</code>\n\n🏓 <b>Latência:</b> <code>{ping} ms</code>\n🔽 <b>Download:</b> <code>{dl} Mbps</code>\n🔼 <b>Upload:</b> <code>{ul} Mbps</code>\n🖥  <b>ISP:</b> <code>{isp}</code>"
        )
        await running.delete()
    

@megux.on_message(filters.command("speed") & filters.user(1715384854))
async def test_speed(c: megux, m: Message):
    running = await m.reply("`Processando...`")
    test = speedtest.Speedtest()
    bs = test.get_best_server()
    dl = round(test.download() / 1024 / 1024, 2)
    ul = round(test.upload() / 1024 / 1024, 2)
    test.results.share()
    result = test.results.dict()
    path = wget.download(result["share"])
    response = await m.reply_photo(
        photo=path
    )
    await running.delete() 
