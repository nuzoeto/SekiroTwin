##
#

import time

from pyrogram import filters
from pyrogram.errors import PeerIdInvalid, UserIdInvalid, UsernameInvalid
from pyrogram.types import Message

from megumin import megux
from megumin.utils import (
    admin_check,
    check_bot_rights,
    check_rights,
    is_admin,
    is_dev,
    is_self,
    sed_sticker,
)


@megux.on_message(filters.command("ban"))
async def _ban_user(_, message: Message):
    chat_id = message.chat.id
    if not await check_rights(chat_id, message.from_user.id, "can_restrict_members"):
        await message.reply("Você não tem as seguintes permissões: **Can restrict members**")
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
        await message.reply("`Nenhum user_id válido ou mensagem especificada.`")
        return
    try:
        user = await megux.get_users(id_)
        user_id = user.id
        mention = user.mention
    except (UsernameInvalid, PeerIdInvalid, UserIdInvalid):
        await message.reply(
            "`Nome de usuário ou ID de usuário inválido, tente novamente com informações válidas ⚠`"
        )
        return
    if await is_self(user_id):
        await sed_sticker(message)
        return
    if is_dev(user_id):
        await message.reply("Porque eu iria banir meu desenvolvedor? Isso me parece uma idéia muito idiota.")
        return
    if is_admin(chat_id, user_id):
        await message.reply("Porque eu iria banir um administrador? Isso me parece uma idéia idiota.")
        return
    if not await check_bot_rights(chat_id, "can_restrict_members"):
        await message.reply("Eu não sou um administrador, **Por favor me promova como um administrador!**")
        await sed_sticker(message)
        return
    sent = await message.reply("`Banindo usuário...`")
    try:
        await megux.kick_chat_member(chat_id, user_id)
        await sent.edit(f"Usuário {mention} foi banido por <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> no chat: **{message.chat.title}**\n" f"**Motivo**: `{reason or None}`")
    except Exception as e_f:
        await sent.edit(f"`Algo deu errado 🤔`\n\n**ERROR:** `{e_f}`")


@megux.on_message(filters.command("unban"))
async def _unban_user(_, message: Message):
    chat_id = message.chat.id
    if not await check_rights(chat_id, message.from_user.id, "can_restrict_members"):
        await message.reply("`Você não tem as seguintes permissões: **Can restrict members**")
        return
    replied = message.reply_to_message
    if replied:
        id_ = replied.from_user.id
    elif len(message.text) > 6:
        _, id_ = message.text.split(maxsplit=1)
    else:
        await message.reply("`Nenhum User_id válido ou mensagem especificada.`")
        return
    try:
        user_id = (await megux.get_users(id_)).id
    except (UsernameInvalid, PeerIdInvalid, UserIdInvalid):
        await message.reply(
            "`User_id ou nome de usuário inválido, tente novamente com informações válidas ⚠`"
        )
        return
    if await is_self(user_id):
        return
    if is_admin(chat_id, user_id):
        await message.reply("Este usuário é admin ele não precisa ser desbanido.")
        return
    if not await check_bot_rights(chat_id, "can_restrict_members"):
        await message.reply("Eu não sou um administrador, **Por favor me promova como um administrador!**")
        await sed_sticker(message)
        return
    sent = await message.reply("`Desbanindo Usuário...`")
    try:
        await megux.unban_chat_member(chat_id, user_id)
        await sent.edit ("__Ok, este usuário não está mais banido,__\n**Ele pode entrar novamente.**")
    except Exception as e_f:
        await sent.edit(f"`Algo deu errado! 🤔`\n\n**ERROR:** `{e_f}`")


@megux.on_message(filters.command("kick"))
async def _kick_user(_, message: Message):
    chat_id = message.chat.id
    if not await check_rights(chat_id, message.from_user.id, "can_restrict_members"):
        await message.reply("Você não tem as seguintes permissões: **Can restrict members**")
        return
    cmd = len(message.text)
    replied = message.reply_to_message
    reason = ""
    if replied:
        id_ = replied.from_user.id
        if cmd > 5:
            _, reason = message.text.split(maxsplit=1)
    elif cmd > 5:
        _, args = message.text.split(maxsplit=1)
        if " " in args:
            id_, reason = args.split(" ", maxsplit=1)
        else:
            id_ = args
    else:
        await message.reply("`Nenhum user_id válido ou mensagem especificada.`")
        return
    try:
        user = await megux.get_users(id_)
        user_id = user.id
        mention = user.mention
    except (UsernameInvalid, PeerIdInvalid, UserIdInvalid):
        await message.reply(
            "`User_id ou nome de usuário inválido, tente novamente com informações válidas ⚠`"
        )
        return
    if await is_self(user_id):
        await sed_sticker(message)
        return
    if is_dev(user_id):
        await message.reply("Porque eu iria banir meu desenvolvedor? Isso me parece uma idéia muito idiota.")
        return
    if is_admin(chat_id, user_id):
        await message.reply("Porque eu iria kickar um administrador? Isso me parece uma idéia idiota.")
        return
    if not await check_bot_rights(chat_id, "can_restrict_members"):
        await message.reply("Eu não sou um administrador, **Por favor me promova como um administrador!**")
        await sed_sticker(message)
        return
    sent = await message.reply("`Kickando usuário...`")
    try:
        await megux.kick_chat_member(chat_id, user_id, int(time.time() + 60))
        await megux.unban_chat_member(chat_id, user_id)
        await sent.edit(f"Eu removi o usuário {mention}\n" f"Motivo: `{reason or None}`")
    except Exception as e_f:
        await sent.edit(f"`Algo deu errado! 🤔`\n\n**ERROR:** `{e_f}`")


@megux.on_message(filters.command("kickme"))
async def kickme_(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    admin_ = await admin_check(message)
    if admin_:
        await message.reply("`Hmmm admin...\nVocê não vai a lugar nenhum senpai.`")
        return
    else:
        try:
            if not await check_bot_rights(chat_id, "can_restrict_members"):
                await message.reply("Eu não sou um administrador, **Por favor me promova como um administrador!**")
                return
            await message.reply("Ate mais, espero que tenha gostado da estadia.")
            await megux.kick_chat_member(chat_id, user_id)
            await megux.unban_chat_member(chat_id, user_id)
        except Exception as e:
            await message.reply(f"**ERRO:**\n{e}")


@megux.on_message(filters.command("banme"))
async def kickme_(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    admin_ = await admin_check(message)
    if admin_:
        await message.reply("Por que eu baniria um(a) administrador(a)? Parece uma ideia bem idiota.")
        return
    else:
        try:
            if not await check_bot_rights(chat_id, "can_restrict_members"):
                await message.reply("Eu não sou um(a) administrador(a)!")
                return
            await message.reply("Sem Problemas.")
            await megux.kick_chat_member(chat_id, user_id)
        except Exception as e:
            await message.reply(f"**ERRO:**\n{e}")


@megux.on_message(filters.command("tban"))
async def _tmute_user(_, message: Message):
    chat_id = message.chat.id
    if not await check_rights(chat_id, message.from_user.id, "can_restrict_members"):
        await message.reply("Você não tem as seguintes permissões: **Can restrict members**")
        return
    cmd = len(message.text)
    replied = message.reply_to_message
    if replied:
        id_ = replied.from_user.id
        if cmd <= 6:
            await message.reply("__Você deve especificar um tempo após o comando. Por exemplo:__ **/tmute 7d.**")
            return
        _, args = message.text.split(maxsplit=1)
    elif cmd > 6:
        _, text = message.text.split(maxsplit=1)
        if " " in text:
            id_, args = text.split(" ", maxsplit=1)
        else:
            await message.reply("__Você deve especificar um tempo após o comando. Por exemplo:__ **/tmute 7d.**")
    else:
        await message.reply("`Nenhum User_id válido ou mensagem especificada.`")
        return
    if " " in args:
        split = args.split(None, 1)
        time_val = split[0].lower()
        reason = split[1]
    else:
        time_val = args
        reason = ""

    time_ = await extract_time(message, time_val)
    if not time_:
        return
    try:
        user = await megux.get_users(id_)
        user_id = user.id
        mention = user.mention
    except (UsernameInvalid, PeerIdInvalid, UserIdInvalid):
        await message.reply(
            "`User_id ou nome de usuário inválido, tente novamente com informações válidas ⚠`"
        )
        return
    if await is_self(user_id):
        await sed_sticker(message)
        return
    if is_dev(user_id):
        await message.reply("Porque eu iria mutar meu desenvolvedor? Isso me parece uma idéia muito idiota.")
        return
    if is_admin(chat_id, user_id):
        await message.reply("Porque eu iria mutar um administrador? Isso me parece uma idéia idiota.")
        return
    if not await check_bot_rights(chat_id, "can_restrict_members"):
        await message.reply("Eu não sou um administrador, **Por favor me promova como um administrador!**")
        await sed_sticker(message)
        return
    sent = await message.reply("`Banindo usuário temporariamente...`")
    try:
        await megux.kick_chat_member(chat_id, user_id, time_)
        await asyncio.sleep(1)
        await sent.edit(
            f"{mention} foi banido por **{time_val}** em **{message.chat.title}**\n"
            f"Motivo: `{reason or None}`"
        )
    except Exception as e_f:  # pylint: disable=broad-except
        await sent.edit(f"`Algo deu errado 🤔`\n\n**ERROR**: `{e_f}`")
