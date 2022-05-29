from pyrogram import filters
from pyrogram.types import Message

from megumin import megux, Config 
from megumin.utils import check_bot_rights, check_rights, get_string 
from megumin.utils.decorators import input_str 


@megux.on_message(filters.command("pin", Config.TRIGGER))
async def pin_msg(c: megux, m: Message):
    input_ = input_str(m).split()
    reply = m.reply_to_message
    gid = m.chat.id
    if not await check_rights(gid, m.from_user.id, "can_pin_messages"):
        return await m.reply(await get_string(m.chat.id, "NO_PIN_USER"))
    if not await check_rights(gid, c.me.id, "can_pin_messages"):
        return await m.reply(await get_string(m.chat.id, "NO_PIN_BOT"))
    if not reply:
        return await m.reply(await get_string(m.chat.id, "PIN_NO_REPLY"))
    silent = False
    msg_id = reply.id
    chat = str(f"{gid}").replace("-100", "")
    link = f"https://t.me/c/{chat}/{reply.id}"
    string = await get_string(m.chat.id, "PIN_SUCCESS")
    if input_:
        if ("silent" or "s") in input_:
            silent = True
    try:
        await megux.pin_chat_message(gid, msg_id, disable_notification=silent)
        await m.reply(string.format(link))
    except Exception as e:
        await megux.send_log(e)


@megux.on_message(filters.command("unpin", Config.TRIGGER))
async def pin_msg(c: megux, m: Message):
    input_ = input_str(m).split()
    reply = m.reply_to_message
    gid = m.chat.id
    if not await check_rights(gid, m.from_user.id, "can_pin_messages"):
        return await m.reply(await get_string(m.chat.id, "NO_PIN_USER"))
    if not await check_rights(gid, c.me.id, "can_pin_messages"):
        return await m.reply(await get_string(m.chat.id, "NO_PIN_BOT"))
    if input_:
        if "all" in input_:
            try:
                await m.reply(await get_string(m.chat.id, "UNPIN_ALL_SUCCESS"))
                return await megux.unpin_all_chat_messages(gid)
            except Exception as e:
                await megux.send_log(e)
        else:
            pass
    elif reply:
        try:
            chat = str(f"{gid}").replace("-100", "")
            link = f"https://t.me/c/{chat}/{reply.id}"
            string = await get_string(m.chat.id, "UNPIN_SUCCESS")
            await m.reply(string.format(link))
            return await megux.unpin_chat_message(gid, reply.id)
        except Exception as e:
            await megux.send_log(e)
    else:
        return await m.reply(await get_string(m.chat.id, "UNPIN_NO_REPLY"))
