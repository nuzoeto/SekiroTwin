#Copyright BubbalooTeam

import html
import functools
import re
import contextlib

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from pyrogram.errors import PeerIdInvalid, UserIdInvalid, UsernameInvalid

from megumin import megux, Config
from megumin.utils import get_collection, extract_time, check_rights, check_bot_rights, is_self, is_dev, is_admin


@megux.on_message(filters.command("warn", Config.TRIGGER))
async def warn_(c: megux, message: Message):
    chat_id = message.chat.id
    if not await check_rights(chat_id, message.from_user.id, "can_restrict_members"):
        await message.reply("Você não tem permissões suficientes para advertir usuarios.")
        return
    cmd = len(message.text)
    replied = message.reply_to_message
    reason = ""
    if replied:
        id_ = replied.from_user.id
        if cmd > 4:
            _, reason = message.text.split(maxsplit=1)
    elif cmd > 4:
        _, args = message.text.split(maxsplit=1)
        if " " in args:
            id_, reason = args.split(" ", maxsplit=1)
        else:
            id_ = args
    else:
        await message.reply("Você não parece estar se referindo a um usuário.")
        return
    try:
        user = await megux.get_users(id_)
        user_id = user.id
        mention = user.mention
    except (UsernameInvalid, UserIdInvalid, PeerIdInvalid):
        await message.reply("Eu não tenho esse usuário no meu banco de dados de usuários.\nVocê poderá interagir com eles se responder à mensagem dessa pessoa ou encaminhar uma de suas mensagens (isso só funcionará se o usuário não tiver sua conta oculta).")
        return
    if await is_self(user_id):
        await message.reply("Eu não irei me advertir você está louco?")
        return
    if is_admin(chat_id, user_id):
        await message.reply("Eu não vou avisar um administrador!")
        return
    if not await check_bot_rights(chat_id, "can_restrict_members"):
        await message.reply("Eu não tenho permissões para advertir usuarios.")
        return
    db = get_collection("WARNS")
    db_max = get_collection("MAX_WARNS")
    mode = get_collection("CHAT_MODE")
    warn_id = await db.insert_one({
        "user_id": user_id,
        "chat_id": chat_id,
        "reason": reason,
        "by": message.from_user.id
    })
    warn_count = await db.count_documents({"chat_id": chat_id, "user_id": user_id})
    if await db_max.find_one():
        hd = await db.max.find_one()
        max_warns = hd["num"]
    else:
        max_warns = 3

    if max_warns == warn_count:
        await db.delete_many({"user_id": user_id, "chat_id": chat_id})
        if await mode.find_one():
            rex = await mode.find_one({"chat_id": chat_id})
            mode_action = rex["action"]
            if mode_action == "mute":
                await megux.restrict_chat_member(chat_id, user_id, ChatPermissions())
                await message.reply("{}/{} Advertências!\n{} foi silenciado até que um administrador remova o mute.".format(warn_count, max_warns, mention))
                return
            if mode_action == "ban":
                await megux.ban_chat_member(chat_id, user_id)
                await message.reply("{}/{} Advertências!\n{} foi Banido.".format(warn_count, max_warns, mention))
                return
            if mode_action == "kick":
                await megux.ban_chat_member(chat_id, user_id)
                await megux.unban_chat_member(chat_id, user_id)
                await message.reply("{}/{} Advertências!\n{} Removido.")
                return
            else:
                await mode.insert_one({"action": "ban"})
    else:
         text = "<b>{} foi advertido!</b>\nEle(a) têm {}/{} Advertências.\n".format(mention, warn_count, max_warns)

        if reason in "":
            pass
        else:
            text += "<b>Motivo.</b>: {}".format(reason)
            await message.reply(text)
