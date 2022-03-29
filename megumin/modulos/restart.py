import sys
import os
import random
import re
import requests
import wget
import datetime
import signal
import asyncio 

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

@megux.on_message(filters.command("restart") & filters.user(1715384854))
async def broadcast(c: megux, m: Message):
    sent = await m.reply("__Reiniciando aguarde...__") 
    args = [sys.executable, "-m", "megumin"]
    await sent.edit("**WhiterKang Reiniciado com Sucesso!**")
    os.execl(sys.executable, *args)


@megux.on_message(filters.command(["update", "upgrade"]) & filters.user(1715384854))
async def broadcast(c: megux, m: Message):
    sent = await m.reply("__Atualizando aguarde...__")
    pull = await asyncio.create_subprocess_shell(
        "git pull",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,)
        stdout = (await proc.communicate())[0]
        if proc.returncode == 0:
            if "Already up to date." in stdout.decode():
            await sm.edit_text("There's nothing to upgrade.")
        else:
    args = [sys.executable, "-m", "megumin"]
    await sent.edit("__Reiniciando aguarde...__")
    os.execl(sys.executable, *args)
    await sent.edit("**WhiterKang Reiniciado com Sucesso!**")


@megux.on_message(filters.command(r"shutdown") & filters.user(1715384854))
async def shutdown(c: megux, m: Message):
    await m.reply_text("Adeus...")
    os.kill(os.getpid(), signal.SIGINT)
