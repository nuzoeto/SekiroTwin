from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import PeerIdInvalid, Forbidden, UsernameInvalid, PeerIdInvalid, UserIdInvalid
from pyrogram.enums import ChatMemberStatus, ChatMembersFilter


from megumin import megux 
from megumin.utils import get_collection, is_admin, check_bot_rights, check_rights
from megumin.utils.decorators import input_str


admin_status = [ChatMemberStatus.ADMINISTRATOR or ChatMemberStatus.OWNER]

@megux.on_message(
    (filters.command("report", prefixes=["/", "!"]) | filters.regex("^@admin"))
    & filters.group
)
async def report_admins(c: megux, m: Message):
    if not m.reply_to_message:
        return await m.reply("Responda a mensagem que deseja reportar")
    chat_id = m.chat.id
    user = m.from_user.mention
    chat_title = m.chat.title
    reported_user = m.reply_to_message.from_user.mention
    reported_user_id = m.reply_to_message.from_user.id
    msg = m.reply_to_message.id
    chat_ab_id = str(f"{chat_id}").replace("-100", "")
    admins_list = megux.get_chat_members(chat_id=chat_id, filter=ChatMembersFilter.ADMINISTRATORS)
    
    keyboard = [[
        InlineKeyboardButton(
            u"➡ Message",
            url="https://t.me/c/{}/{}".format(
                chat_ab_id,
                str(msg)))
        ],
        [
        InlineKeyboardButton(
            u"⚠ Kick",
            callback_data="kick|{}".format(
                reported_user_id)),
        InlineKeyboardButton(
            u"⛔️ Ban",
            callback_data="ban|{}".format(
                reported_user_id)),
        ],       
        [
        InlineKeyboardButton(
            u"❎ Delete Message",
            callback_data="del|{}".format(
                msg, chat_id))
        ]]
            
    # send notification to administrator
    async for admin in admins_list:
        #avoid bots in chat
        if admin.user.is_bot or admin.user.is_deleted:
            continue
        try:    
            await megux.send_message(admin.user.id, f"{user} está chamando os administradores em {chat_title}", reply_markup=InlineKeyboardMarkup(keyboard))
            await megux.forward_messages(admin.user.id, chat_id, msg)
        except PeerIdInvalid:
            continue
    await m.reply(f"{reported_user} Reportado para os administradores.")

    
@megux.on_callback_query(filters.regex(pattern=r"^del\|(.*)"))
async def delete_report(client: megux, cb: CallbackQuery):
    data, mid, chat_id = cb.data.split("|")
    mention_ = cb.from_user.mention
    uid = cb.from_user.id
    if not await check_rights(chat_id, uid, "can_restrict_members"):
        return await cb.answer(await get_string(chat_id, "NO_BAN_USER"), show_alert=True)
    try:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=mid,
            revoke=True
        )
        await cb.awswer("A mensagem foi apagada com sucesso!", show_alert=True)
    except Forbidden:
        await cb.awswer("Provavelmente a mensage já foi apagada.", show_alert=True)
    
