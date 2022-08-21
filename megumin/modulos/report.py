from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid
from pyrogram.enums import ChatMemberStatus, ChatMembersFilter


from megumin import megux 
from megumin.utils import get_collection
from megumin.utils.decorators import input_str


admin_status = [ChatMemberStatus.ADMINISTRATOR or ChatMemberStatus.OWNER]

@megux.on_message(
    (filters.command("report", prefixes=["/", "!"]) | filters.regex("^@admin"))
    & filters.group
)
async def report_admins(c: megux, m: Message):
    chat_id = m.chat.id
    user = m.from_user.mention
    chat_title = m.chat.title
    if m.reply_to_message:
        reported_user = m.reply_to_message.from_user.mention
        shoud_rpt = True
    else:
        reported_user = m.from_user.mention
        shoud_rpt = False
    admins_list = megux.get_chat_members(chat_id=chat_id, filter=ChatMembersFilter.ADMINISTRATORS)
    # send notification to administrator
    async for admin in admins_list:
        #avoid bots in chat
        if admin.user.is_bot or admin.user.is_deleted:
            continue
        try:    
            await megux.send_message(admin.user.id, f"{user} está chamando os administradores em {chat_title}")
            if shoud_rpt == True:
                msg = message.reply_to_message.mention
                await megux.forward_messages(admin.user.id, chat_id, msg)
            elif input_str(m):
                await megux.send_message(admin.user.id, input_str(m))
            else: 
                return await m.reply("Você precisa marcar alguem para reportar")
        except PeerIdInvalid:
            continue
    await m.reply(f"{reported_user} Reportado para os administradores.")
