from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import PeerIdInvalid, Forbidden, UsernameInvalid, PeerIdInvalid, UserIdInvalid
from pyrogram.enums import ChatMemberStatus, ChatMembersFilter


from megumin import megux 
from megumin.utils import get_collection, is_dev, is_admin, check_bot_rights, check_rights, tld
from megumin.utils.decorators import input_str


admin_status = [ChatMemberStatus.ADMINISTRATOR or ChatMemberStatus.OWNER]

@megux.on_message(
    (filters.command("report", prefixes=["/", "!"]) | filters.regex("^@admin"))
    & filters.group
)
async def report_admins(c: megux, m: Message):
    if not m.reply_to_message:
        return await m.reply("Responda a mensagem que deseja reportar.")
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
            callback_data="kick|{}|{}".format(
                chat_id, reported_user_id)),
        InlineKeyboardButton(
            u"⛔️ Ban",
            callback_data="ban|{}|{}".format(
                chat_id, reported_user_id)),
        ],       
        [
        InlineKeyboardButton(
            u"❎ Delete Message",
            callback_data="del|{}|{}".format(
                chat_id, msg))
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
    data, chat_id, mid = cb.data.split("|")
    uid = cb.from_user.id
    if not await check_rights(chat_id, uid, "can_delete_messages"):
        await cb.answer("Você não tem permissões suficientes para apagar mensagens.")
        return
    if not await check_bot_rights(chat_id, "can_delete_messages"):
        await cb.answer("Não consigo excluir mensagens aqui! Verifique se eu sou um(a) administrador(a) e posso excluir mensagens de outros usuários.")
        return
    try:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=int(mid),
            revoke=True
        )
        await cb.answer("✅ Message Deleted", show_alert=True)
    except Exception:
        await cb.answer("🛑 Failed to delete message!", show_alert=True)
  

@megux.on_callback_query(filters.regex(pattern=r"^kick\|(.*)"))
async def delete_report(client: megux, cb: CallbackQuery):
    data, chat_id, user_id = cb.data.split("|")
    uid = cb.from_user.id
    if not await check_rights(chat_id, uid, "can_restrict_members"):
        await cb.answer(await tld(chat_id, "NO_BAN_USER"))
        return
    if not await check_bot_rights(chat_id, "can_restrict_members"):
        await cb.answer(await tld(chat_id, "NO_BAN_BOT"))
        return
    if await is_admin(chat_id, user_id):
        await cb.answer(await tld(chat_id, "BAN_IN_ADMIN"))
        return
    if is_dev(user_id):
        await cb.answer(await tld(chat_id, "BAN_IN_DEV"))
        return
    if await is_self(user_id):
        await cb.awswer(await get_string(chat_id, "BAN_MY_SELF"))
        return
    try:
        await client.ban_chat_member(
            chat_id,
            user_id,
        )
        await client.unban_chat_member(
            chat_id,
            user_id,
        )
        await cb.answer("✅ Succesfully kicked", show_alert=True)
    except Exception:
        await cb.answer("🛑 Failed to kick!", show_alert=True)
    
@megux.on_callback_query(filters.regex(pattern=r"^ban\|(.*)"))
async def delete_report(client: megux, cb: CallbackQuery):
    data, chat_id, user_id = cb.data.split("|")
    uid = cb.from_user.id
    if not await check_rights(chat_id, uid, "can_restrict_members"):
        await cb.answer(await tld(chat_id, "NO_BAN_USER"))
        return
    if not await check_bot_rights(chat_id, "can_restrict_members"):
        await cb.answer(await tld(chat_id, "NO_BAN_BOT"))
        return
    if await is_admin(chat_id, user_id):
        await cb.answer(await tld(chat_id, "BAN_IN_ADMIN"))
        return
    if is_dev(user_id):
        await cb.answer(await tld(chat_id, "BAN_IN_DEV"))
        return
    if await is_self(user_id):
        await cb.answer(await get_string(chat_id, "BAN_MY_SELF"))
        return
    try:
        await client.ban_chat_member(
            chat_id,
            user_id,
        )
        await cb.answer("✅ Succesfully Banned", show_alert=True)
    except Exception:
        await cb.answer("🛑 Failed to ban!", show_alert=True)
        
