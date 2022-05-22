from pyrogram import filters
from pyrogram.types import Message

from megumin import megux


@megux.on_message(filters.command("admins", prefixes=["/", "!"]) & filters.group)
async def mentionadmins(c: megux, m: Message):
    mention = ""
    async for i in m.chat.get_members(m.chat.id, filter=ChatMemberFilter.ADMINISTRATORS):
        if not (i.user.is_deleted or i.is_anonymous):
            mention += f"{i.user.mention}\n"
    await c.send_message(
        m.chat.id,
        "<b>Administradores no chat</b> <code>{chat_title}</code>:\n\n{admins_list}".format(chat_title=m.chat.title, admins_list=mention),
    )
