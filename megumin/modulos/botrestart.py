import sys
import os
import asyncio
import random
import re
import requests
import wget
import datetime

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

@megux.on_message(filters.command("restart") & filters.user(1715384854))
async def broadcast(c: megux, m: Message):
    sent = await m.reply("__Reiniciando aguarde...__")
    await asyncio.sleep(24.2)
    await sent.edit("**WhiterKang Reiniciado com Sucesso!**") 
    args = [sys.executable, "-m", "megumin"]
    os.execl(sys.executable, *args)
