import speedtest
import os
import wget

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

@megux.on_message(filters.command("speedtest"))
async def test_speed(c: megux, m: Message):
    string = "<b>Teste de velocidade</b>\n\n💻<b>ISP</b> <code>{isp}<code>\n<b>🌐 Host:</b> <code>{host}</code>\n\n<b>🏓 Latência:</b> <code>{ping} ms</code>\n<b>⬇️ Download:</b> <code>{download} Mbps</code>\n<b>⬆️ Upload:</b> <code>{upload} Mbps</code>"
    sent = await m.reply(string.format(host="", ping="", download="", upload="", isp=result["client"]["isp"]))
    s = speedtest.Speedtest()
    bs = s.get_best_server()
    result = s.results.dict()
    await sent.edit_text(
        string.format(
            host=bs["sponsor"], ping=int(bs["latency"]), download="", upload="", isp=result["client"]["isp"]
        )
    )
    dl = round(s.download() / 1024 / 1024, 2)
    await sent.edit_text(
        string.format(
            host=bs["sponsor"], ping=int(bs["latency"]), download=dl, upload="", isp=result["client"]["isp"]
        )
    )
    ul = round(s.upload() / 1024 / 1024, 2)
    await sent.edit_text(
        string.format(
            host=bs["sponsor"], ping=int(bs["latency"]), download=dl, upload=ul, isp=result["client"]["isp"]
        )
    )
    

@megux.on_message(filters.command("speed"))
async def test_speed(c: megux, m: Message):
    s = speedtest.Speedtest()
    bs = s.get_best_server()
    result = s.results.dict()
    path= wget.download(result["share"])
    await m.reply_photo(photo=path)
