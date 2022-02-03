import sys
import os

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

@megux.on_message(filters.command("restart"))
async def broadcast(c: megux, m: Message):
    await m.reply_text("Reiniciando aguarde...")
    args = [sys.executable, "-m", "megux"]
    os.execl(sys.executable, *args)
