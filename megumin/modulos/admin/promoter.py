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


@megux.on_message(filters.command("promote", prefixes=["/", "!"]))
async def _promote_user(_, message: Message):
    chat_id = message.chat.id
    if not await check_rights(chat_id, message.from_user.id, "can_promote_members"):
        await message.reply("Você não tem as seguintes permissões: **Change can promote members**")
        return
    replied = message.reply_to_message
    args = message.text.split(maxsplit=1)[1]
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
        await message.reply("Este usuário já é um administrador ele não precisa ser promovido.")
        return
    if not await check_bot_rights(chat_id, "can_promote_members"):
        await message.reply("Eu não tenho as seguintes permissões: **Change can promote members**")
        await sed_sticker(message)
        return
    sent = await message.reply("`Promovendo usuário...`")
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
        if not args:
            await asyncio.sleep(2)
        await sent.edit("<b>Promovido(a)!</b>")
    except Exception as e_f:
        await sent.edit(f"`Algo deu errado! 🤔`\n\n**ERROR:** `{e_f}`")
        return 
        else:
            await asyncio.sleep(2)
        await megux.set_administrator_title(chat_id, user_id, args)
        await sent.edit("<b>Promovido(a)!</b>")
    except Exception as e_f:
        await sent.edit(f"`Algo deu errado! 🤔`\n\n**ERROR:** `{e_f}`")


@megux.on_message(filters.command("demote", prefixes=["/", "!"]))
async def _demote_user(_, message: Message):
    chat_id = message.chat.id
    if not await check_rights(chat_id, message.from_user.id, "can_promote_members"):
        await message.reply("Você não tem as seguintes permissões: **Change can promote members**")
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
        await message.reply("Eu não tem as seguintes permissões: **Change can promote members**")
        await sed_sticker(message)
        return
    sent = await message.reply("`Rebaixando Usuário...`")
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
        await sent.edit("<b>Rebaixado!</b>")
    except Exception as e_f:
        await sent.edit(f"`Algo deu errado! 🤔`\n\n**ERROR:** `{e_f}`")
