import speedtest
import os
import wget
import sys

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

@megux.on_message(filters.command("speedtest"))
async def test_speed(c: megux, m: Message):
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
    path = wget.download(result["share"]) 
    response = await m.reply_photo(
        photo=path, caption=f"🌀 <b>Nome:</b> <code>{name}</code>\n🌐 <b>Host:</b>{host}</code>\n🏁 <b>País:</b> <code>{country}</code>\n\n<b>SpeedTest Results:</b>\n🏓 <b>Latência:</b> <code>{ping} ms</code>\n🔽 <b>Download:</b> <code>{dl} Mbps</code>\n🔼 <b>Upload:</b> <code>{ul} Mbps</code>\n🖥  <b>ISP:</b> <code>{isp}</code>"
    )
    
