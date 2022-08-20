from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus, ChatMembersFilter


from megumin import megux 
from megumin.utils import get_collection 


admin_status = [ChatMemberStatus.ADMINISTRATOR or ChatMemberStatus.OWNER]

@megux.on_message(
    (filters.command("report", prefixes=["/", "!"]) | filters.regex("^@admin"))
    & filters.group
    & filters.reply
)
async def report_admins(c: megux, m: Message):
    chat_id = m.chat.id
    user = m.from_user.id
    chat_title = m.chat.title
    admins_list = await megux.get_chat_members(chat_id=chat_id, filter=ChatMembersFilter.ADMINSTRATORS)
    # send notification to administrator
    for admin in admins_list:
        #avoid bots in chat
        if admin.user.is_bot or admin.user.is_deleted:
            continue
        await megux.send_message(admin.user.id, f"{user} está chamando os administradores em {chat_title}")
    await m.reply(f"{message.reply_to_message.first_name} Reportado para os administradores.")
