import asyncio

from pyrogram import filters
from pyrogram.errors import PeerIdInvalid, UserIdInvalid, UsernameInvalid
from pyrogram.types import ChatPermissions, Message

from megumin import megux
from megumin.utils import (
    check_bot_rights,
    check_rights,
    extract_time,
    is_admin,
    is_dev,
    is_self,
    sed_sticker,
)


@megux.on_message(filters.command("mute"))
async def _mute_user(_, message: Message):
    chat_id = message.chat.id
    if not await check_rights(chat_id, message.from_user.id, "can_restrict_members"):
        await message.reply("`Você precisa de permissão para fazer isso.`")
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
        await message.reply("`Nenhum User_id válido ou mensagem especificada.`")
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
        await message.reply("`Lol ele é meu desenvolvedor, não posso muta-lo..`")
        return
    if is_admin(chat_id, user_id):
        await message.reply("`Usuario é admin, não posso muta=lo.`")
        return
    if not await check_bot_rights(chat_id, "can_restrict_members"):
        await message.reply("`Dê-me privilegios admin para Mute Users.`")
        await sed_sticker(message)
        return
    sent = await message.reply("`Tentando mutar usuario.. Aguarde!! ⏳`")
    try:
        await megux.restrict_chat_member(chat_id, user_id, ChatPermissions())
        await asyncio.sleep(1)
        await sent.edit(
            f"#MUTE\n"
            f"USUARIO: {mention}\n"
            f"TEMPO: `Permanente`\n"
            f"MOTIVO: `{reason or None}`"
        )
    except Exception as e_f:
        await sent.edit(f"`Algo deu errado 🤔`\n\n**ERROR**: `{e_f}`")


@megux.on_message(filters.command("tmute"))
async def _tmute_user(_, message: Message):
    chat_id = message.chat.id
    if not await check_rights(chat_id, message.from_user.id, "can_restrict_members"):
        await message.reply("`Você precisa de permissão para fazer isso.`")
        return
    cmd = len(message.text)
    replied = message.reply_to_message
    if replied:
        id_ = replied.from_user.id
        if cmd <= 6:
            await message.reply("`Limite de tempo não encontrado.`")
            return
        _, args = message.text.split(maxsplit=1)
    elif cmd > 6:
        _, text = message.text.split(maxsplit=1)
        if " " in text:
            id_, args = text.split(" ", maxsplit=1)
        else:
            await message.reply("`Limite de tempo não encontrado.`")
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
        await message.reply("`Lol ele é meu mestre, não vou muta-lo.`")
        return
    if is_admin(chat_id, user_id):
        await message.reply("`Ele é admin, não posso muta-lo.`")
        return
    if not await check_bot_rights(chat_id, "can_restrict_members"):
        await message.reply("`Dê-me privilegios admin para Mute Users.`")
        await sed_sticker(message)
        return
    sent = await message.reply("`Tentando silenciar o usuário.. Aguarde!! ⏳`")
    try:
        await megux.restrict_chat_member(chat_id, user_id, ChatPermissions(), time_)
        await asyncio.sleep(1)
        await sent.edit(
            f"#TEMP_MUTE\n"
            f"USUARIO: {mention}\n"
            f"TIME: `{time_val}`\n"
            f"MOTIVO: `{reason or None}`"
        )
    except Exception as e_f:  # pylint: disable=broad-except
        await sent.edit(f"`Algo deu errado 🤔`\n\n**ERROR**: `{e_f}`")


@megux.on_message(filters.command("unmute"))
async def _unmute_user(_, message: Message):
    chat_id = message.chat.id
    if not await check_rights(chat_id, message.from_user.id, "can_restrict_members"):
        await message.reply("`Você precisa de permissão para fazer isso.`")
        return
    replied = message.reply_to_message
    if replied:
        id_ = replied.from_user.id
    elif len(message.text) > 7:
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
        await message.reply("`Usuario é admin.`")
        return
    if not await check_bot_rights(chat_id, "can_restrict_members"):
        await message.reply("`Dê-me privilegios admin para UnMute Users.`")
        await sed_sticker(message)
        return
    sent = await message.reply("`Tentando desmutar usuario.. Aguarde!! ⏳`")
    try:
        await megux.unban_chat_member(chat_id, user_id)
        await sent.edit("`🛡 Desmutado com sucesso..`")
    except Exception as e_f:
        await sent.edit(f"`Algo deu errado!` 🤔\n\n**ERROR:** `{e_f}`")
