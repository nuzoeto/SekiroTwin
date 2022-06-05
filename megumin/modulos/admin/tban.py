import asyncio

from pyrogram import filters
from pyrogram.errors import PeerIdInvalid, UserIdInvalid, UsernameInvalid
from pyrogram.types import Message

from megumin import megux
from megumin.utils import (
    check_bot_rights,
    check_rights,
    extract_time,
    is_admin,
    is_dev,
    is_self,
    sed_sticker,
    get_collection,
)


@megux.on_message(filters.command("tban", prefixes=["/", "!"]))
async def _tban_user(_, message: Message):
    chat_id = message.chat.id
    if not await check_rights(chat_id, message.from_user.id, "can_restrict_members"):
        await message.reply("Você não tem direitos suficientes para silenciar usuários")
        return
    cmd = len(message.text)
    replied = message.reply_to_message
    if replied:
        id_ = replied.from_user.id
        if cmd <= 6:
            await message.reply("__Você deve especificar um tempo após o comando. Por exemplo:__ <b>/tban 7d.</b>")
            return
        _, args = message.text.split(maxsplit=1)
    elif cmd > 6:
        _, text = message.text.split(maxsplit=1)
        if " " in text:
            id_, args = text.split(" ", maxsplit=1)
        else:
            await message.reply("__Você deve especificar um tempo após o comando. Por exemplo:__ **/tban 7d.**")
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
        await message.reply("Eu não vou mutar!")
        return
    if is_dev(user_id):
        await message.reply("Porque eu iria mutar meu desenvolvedor? Isso me parece uma idéia muito idiota.")
        return
    if is_admin(chat_id, user_id):
        await message.reply("Porque eu iria mutar um(a) administrador(a)? Isso me parece uma idéia bem idiota.")
        return
    if not await check_rights(chat_id, megux.me.id, "can_restrict_members"):
        await message.reply("Não posso restringir as pessoas aqui! Certifique-se de que sou administrador e de que posso adicionar novos administradores.")
        await sed_sticker(message)
        return
    sent = await message.reply("`Banindo usuário temporariamente...`")
    try:
        await megux.ban_chat_member(chat_id, user_id, time_)
        await asyncio.sleep(1)
        await sent.edit(
            f"{mention} foi banido por <b>{time_val}</b> em <b>{message.chat.title}</b>\n"
            f"<b>Motivo</b>: `{reason or None}`"
        )
    except Exception as e_f:  # pylint: disable=broad-except
        await sent.edit(f"`Algo deu errado 🤔`\n\n**ERROR**: `{e_f}`")
