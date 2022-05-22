from pyrogram import filters
from pyrogram.types import Message

from megumin import megux
from megumin.utils import check_bot_rights, check_rights


@kuuhaku.on_message(filters.command("pin", trg))
async def pin_msg(c: kuuhaku, m: Message):
    input_ = input_str(m).split()
    reply = m.reply_to_message
    gid = m.chat.id
    if not await check_rights(gid, m.from_user.id, "can_pin_messages"):
        return await m.reply("Você não tem direitos administrativos suficientes para fazer fixar/desafixar mensagens!")
    if not await check_rights(gid, c.me.id, "can_pin_messages"):
        return await m.reply("Não consigo fixar mensagens aqui! Verifique se sou administrador e posso fixar mensagens.")
    if not reply:
        return await m.reply(await get_string(gid, "PIN_REPLY"))
    silent = False
    msg_id = reply.id
    chat = str(f"{gid}").replace("-100", "")
    link = f"https://t.me/c/{chat}/{reply.id}"
    string = await get_string(gid, "PIN")
    if input_:
        if ("silent" or "s") in input_:
            silent = True
    try:
        await kuuhaku.pin_chat_message(gid, msg_id, disable_notification=silent)
        await m.reply(string.format(link))
    except Exception as e:
        await kuuhaku.send_err(e)


@megux.on_message(filters.command("unpin", trg))
async def pin_msg(c: megux, m: Message):
    input_ = input_str(m).split()
    reply = m.reply_to_message
    gid = m.chat.id
    if not await check_rights(gid, m.from_user.id, "can_pin_messages"):
        return await m.reply("Você não tem direitos administrativos suficientes para fazer fixar/desafixar mensagens!")
    if not await check_rights(gid, c.me.id, "can_pin_messages"):
        return await m.reply("Não consigo fixar mensagens aqui! Verifique se sou administrador e posso fixar mensagens." )
    if input_:
        if "all" in input_:
            try:
                return await megux.unpin_all_chat_messages(gid)
            except Exception as e:
                await megux.send_log(e)
        else:
            pass
    elif reply:
        try:
            return await megux.unpin_chat_message(gid, reply.id)
        except Exception as e:
            await megux.send_log(e)
    else:
        return await m.reply(await get_string(gid, "UNPIN_REPLY"))
