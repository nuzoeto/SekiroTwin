import sys
import os
import re
import signal
import asyncio 
import traceback 
import subprocess
import io


from pyrogram import filters
from pyrogram.types import Message
from datetime import datetime 

from megumin import megux
from megumin.utils import is_dev

@megux.on_message(filters.command("restart") & filters.user(1715384854))
async def broadcast(c: megux, m: Message):
    sent = await m.reply("__Reiniciando aguarde...__") 
    args = [sys.executable, "-m", "megumin"]
    await sent.edit("**WhiterKang Reiniciado com Sucesso!**")
    os.execl(sys.executable, *args)


@megux.on_message(filters.command(r"shutdown") & filters.user(1715384854))
async def shutdown(c: megux, m: Message):
    await m.reply_text("**WhiterKang foi desligado!**")
    os.kill(os.getpid(), signal.SIGINT)


@megux.on_message(filters.command(["up", "update"]))
async def restart_(_, message: Message):
    user_id = message.from_user.id
    if not is_dev(user_id):
        return
    process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    kek = await message.reply(f"`{output}`")
    await asyncio.sleep(3)
    await kek.edit("`Reiniciando...`")
    await asyncio.sleep(2)
    await kek.edit("**WhiterKang foi Reiniciado com Sucesso!**")
    os.execv(sys.executable, [sys.executable, "-m", "megumin"])
