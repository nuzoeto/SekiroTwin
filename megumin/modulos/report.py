from pyrogram import filters
from pyrogram.types import Message

from megumin import megux 

admin_status = "administrator" or "creator"

@megux.on_message(
    (filters.command("report", prefixes=["/", "!"]) | filters.regex("^@admin"))
    & filters.group
    & filters.reply
)
async def report_admins(c: megux, m: Message):
    if m.reply_to_message.from_user:
        check_admin = await m.chat.get_member(m.reply_to_message.from_user.id)
        if check_admin.status not in admin_status:
            mention = ""
            async for i in m.chat.iter_members(filter="administrators"):
                if not (i.user.is_deleted or i.is_anonymous or i.user.is_bot):
                    mention += f"<a href='tg://user?id={i.user.id}'>\u2063</a>"
            await m.reply_to_message.reply_text(
                "{admins_list}{reported_user} reportado para os administradores.".format(
                    admins_list=mention,
                    reported_user=m.reply_to_message.from_user.mention(),
                ),
            )
