import io
import os
import re
import httpx
import yt_dlp
import datetime
import rapidjson

from pyrogram.types import Message
from pyrogram.errors import BadRequest
from pyrogram import filters

from megumin import megux

@megux.on_message(filters.command("yt"))
async def yt_search_cmd(c: megux, m: Message):
    vids = [
        '{}: <a href="{}">{}</a>'.format(num + 1, i["url"], i["title"])
        for num, i in enumerate(await youtube_search(m.text.split(None, 1)[1]))
    ]
    await m.reply_text(
        "\n".join(vids) if vids else r"¯\_(ツ)_/¯", disable_web_page_preview=True
    )
