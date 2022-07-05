# reserved


import asyncio

from pyrogram import filters
from pyrogram.errors import PeerIdInvalid, UserIdInvalid, UsernameInvalid
from pyrogram.types import Message, ChatPrivileges 
 

from megumin import megux
from megumin.utils import (
    check_bot_rights,
    check_rights,
    is_admin,
    is_dev,
    is_self,
    sed_sticker,
    get_collection,
    tld,
)


@megux.on_message(filters.command("promote", prefixes=["/", "!"]))
async def _promote_user(_, message: Message):
    LOGS = get_collection(f"LOGS {message.chat.id}")
    chat_id = message.chat.id
    if not await check_rights(chat_id, message.from_user.id, "can_promote_members"):
        await message.reply("Você não tem direitos administrativos suficientes para promover/rebaixar alguém!")
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
        user = (await megux.get_users(id_))
        user_id = user.id
        mention = user.mention
    except (UsernameInvalid, PeerIdInvalid, UserIdInvalid):
        await message.reply(
            "`User_id ou nome de usuário inválido, tente novamente com informações válidas ⚠`"
        )
        return
    if await is_self(user_id):
        await message.reply("Eu não posso me promover")
        return
    if is_admin(chat_id, user_id):
        await message.reply("Como devo promover alguém que já é administrador?")
        return
    if not await check_rights(chat_id, megux.me.id, "can_promote_members"):
        await message.reply("Não posso promover/rebaixar pessoas aqui! Verifique se eu sou um(a) administrador(a) e posso adicionar novos administradores.")
        await sed_sticker(message)
        return
    sent = await message.reply("`Promovendo usuário...`")
    try:
        await megux.promote_chat_member(
            chat_id,
            user_id,
            ChatPrivileges(
            can_change_info=True,
            can_delete_messages=True,
            can_restrict_members=True,
            can_invite_users=True,
            can_pin_messages=True,
            )
        ) 
        if args:
            await asyncio.sleep(2)
        await sent.edit(f"{mention} Foi promovido com sucesso!")
        data = await LOGS.find_one()
        if data:
            id = data["log_id"]
            id_log = int(id)
            try:
                await megux.send_message(id_log, (await tld(chat_id, "PROMOTE_LOGGER")).format(m.chat.title, m.from_user.id, mention))
            except PeerIdInvalid:
                return
    except Exception as e_f:
        await sent.edit(f"`Algo deu errado! 🤔`\n\n**ERROR:** `{e_f}`")


@megux.on_message(filters.command("demote", prefixes=["/", "!"]))
async def _demote_user(_, message: Message):
    chat_id = message.chat.id
    if not await check_rights(chat_id, message.from_user.id, "can_promote_members"):
        await message.reply("Você não tem direitos administrativos suficientes para promover/rebaixar alguém!")
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
        user = (await megux.get_users(id_))
        user_id = user.id
        mention = user.mention 
    except (UsernameInvalid, PeerIdInvalid, UserIdInvalid):
        await message.reply(
            "`User_id ou nome de usuário inválido, tente novamente com informações válidas ⚠`"
        )
        return
    if await is_self(user_id):
        await message.reply("Eu não posso me rebaixar!")
        await sed_sticker(message)
        return
    if is_dev(user_id):
        return
    if not await check_rights(chat_id, megux.me.id, "can_promote_members"):
        await message.reply("Não posso promover/rebaixar pessoas aqui! Verifique se eu sou um(a) administrador(a) e posso adicionar novos administradores.")
        await sed_sticker(message)
        return
    sent = await message.reply("`Rebaixando Usuário...`")
    try:
        await megux.promote_chat_member(
            chat_id,
            user_id,
            ChatPrivileges(
            can_change_info=False,
            can_delete_messages=False,
            can_restrict_members=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_manage_chat=False,
            )
        )
        await sent.edit(f"{mention} Foi rebaixado com sucesso! ")
    except Exception as e_f:
        await sent.edit(f"`Algo deu errado! 🤔`\n\n**ERROR:** `{e_f}`")


@megux.on_message(filters.command(["title", "settitle"], prefixes=["/", "!"]))
async def set_user_title(_, message: Message):
    chat_id = message.chat.id
    if not await check_rights(chat_id, message.from_user.id, "can_promote_members"):
        await message.reply("Você não tem direitos administrativos suficientes para promover/rebaixar alguém!")
        return
    if not message.reply_to_message:
        return await message.reply_text(
            "Responda à mensagem do usuário para definir um título de administrador"
        )
    if not message.reply_to_message.from_user:
        return await message.reply_text(
            "Não consigo alterar o título de administrador de uma identidade desconhecida"
        )
    from_user = message.reply_to_message.from_user
    if len(message.command) < 2:
        return await message.reply_text(
            "**Uso:**\n/title <título aqui>."
        )
    title = message.text.split(None, 1)[1]
    await megux.set_administrator_title(chat_id, from_user.id, title)
    await message.reply_text(
        f"Alterado com sucesso o título de administrador de {from_user.mention}'s foi alterado para {title}"
    )
