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
    path = wget.download(result["share"]) 
    response = await m.reply_photo(
        photo=path, caption=f"<b>Teste de velocidade</b>\n\n<b>🌀 Nome:</b> `{result["server"]["name"]}`\n<b>🏁 País:</b> `{result["server"]["country"]}`\n<b>💻 ISP:</b> `{result["client"]["isp"]}`\n<b>🌐 Host:</b> <code>{bs["sponsor"]}</code>\n\n<b>🏓 Latência:</b> <code>{int(bs["latency"])} ms</code>\n<b>⬇️ Download:</b> <code>{dl} Mbps</code>\n<b>⬆️ Upload:</b> <code>{ul} Mbps</code>"
    )
    
