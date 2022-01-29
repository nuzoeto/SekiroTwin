# reserved


import asyncio

from pyrogram import filters
from pyrogram.errors import PeerIdInvalid, UserIdInvalid, UsernameInvalid
from pyrogram.types import Message

from megumin import megux
from megumin.utils import (
    check_bot_rights,
    check_rights,
    is_admin,
    is_dev,
    is_self,
    sed_sticker,
)


@megux.on_message(filters.command("promote"))
async def _promote_user(_, message: Message):
    chat_id = message.chat.id
    if not await check_rights(chat_id, message.from_user.id, "can_promote_members"):
        await message.reply("`Você precisa de permissão para fazer isso.`")
        return
    replied = message.reply_to_message
    args = len(message.text)
    if replied:
        id_ = replied.from_user.id
    elif len(message.text) > 8:
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
        await message.reply("`Usuario ja foi promovido`")
        return
    if not await check_bot_rights(chat_id, "can_promote_members"):
        await message.reply("`Dê-me privilegios admin para promover usuarios.`")
        await sed_sticker(message)
        return
    sent = await message.reply("`Temtando promover usuario.. Aguarde!! ⏳`")
    try:
        await megux.promote_chat_member(
            chat_id,
            user_id,
            can_change_info=True,
            can_delete_messages=True,
            can_restrict_members=True,
            can_invite_users=True,
            can_pin_messages=True,
        )
        if args:
            await asyncio.sleep(2)
            await megux.set_administrator_title(chat_id, user_id, args)
        await sent.edit("`👑 Promovido com sucesso..`")
    except Exception as e_f:
        await sent.edit(f"`Algo deu errado! 🤔`\n\n**ERROR:** `{e_f}`")


@megux.on_message(filters.command("demote"))
async def _demote_user(_, message: Message):
    chat_id = message.chat.id
    if not await check_rights(chat_id, message.from_user.id, "can_promote_members"):
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
        await sed_sticker(message)
        return
    if is_dev(user_id):
        return
    if not await check_bot_rights(chat_id, "can_promote_members"):
        await message.reply("`Dê-me privilegios admin para rebaixar usuarios.`")
        await sed_sticker(message)
        return
    sent = await message.reply("`Tentando rebaixar usuario.. Aguarde!! ⏳`")
    try:
        await megux.promote_chat_member(
            chat_id,
            user_id,
            can_change_info=False,
            can_delete_messages=False,
            can_restrict_members=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_manage_chat=False,
        )
        await sent.edit("`🛡 Rebaixado com sucesso..`")
    except Exception as e_f:
        await sent.edit(f"`Algo deu errado! 🤔`\n\n**ERROR:** `{e_f}`")
