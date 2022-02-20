import sys
import os

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

class groups(Model):
    id = fields.IntField(pk=True)
    git_repo = fields.TextField(null=True)
    git_repo_name = fields.TextField(null=True)


@megux.on_message(filters.command("broadcast") & filters.user(1715384854))
async def broadcast(c: megux, m: Message):
    sm = await m.reply_text("Broadcasting...")
    command = m.text.split()[0]
    text = m.text[len(command) + 1 :]
    chats = await groups.all()
    success = []
    fail = []
    for chat in chats:
        try:
            if await c.send_message(chat.id, text):
                success.append(chat.id)
            else:
                fail.append(chat.id)
        except:
            fail.append(chat.id)
    await sm.edit_text(
        f"Anúncio feito com sucesso! Sua mensagem foi enviada em um total de <code>{len(success)}</code> grupos e falhou o envio em <code>{len(fail)}</code> grupos."
    )
