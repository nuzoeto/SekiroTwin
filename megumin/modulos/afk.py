import re
import asyncio 

from pyrogram import filters, enums
from pyrogram.errors import FloodWait, UserNotParticipant, BadRequest
from pyrogram.types import Message 

from megumin import megux, Config
from megumin.utils import get_collection, get_string  
from megumin.utils.decorators import input_str



@megux.on_message(filters.command("afk"))
@megux.on_message(filters.regex(r"^(?i)brb(\s(?P<args>.+))?"))
async def afk_cmd(_, m: Message):
    x = ""
    x += input_str(m)
    REASON = get_collection(f"REASON {m.from_user.id}")
    AFK_STATUS = get_collection(f"_AFK {m.from_user.id}")
    await AFK_STATUS.drop()
    await REASON.drop()
    await AFK_STATUS.insert_one({"_afk": "on"}) 
    await REASON.insert_one({"reason": x})
    res = await REASON.find_one()
    r = res["reason"]
    await m.reply((await get_string(m.chat.id, "AFK_IS_NOW")).format(m.from_user.first_name, r))
    await m.stop_propagation()

@megux.on_message(filters.group & ~filters.bot, group=2)
async def rem_afk(c: megux, m: Message):
    if not m.from_user:
        return
 
    AFK_STATUS = get_collection(f"_AFK {m.from_user.id}")
    user_afk = await AFK_STATUS.find_one({"_afk": "on"})

    if not user_afk:
        return

    await AFK_STATUS.drop()
    await m.reply_text(
        (await get_string(m.chat.id, "AFK_LOOGER")).format(m.from_user.first_name)
    )

    
@megux.on_message(filters.group & ~filters.bot, group=3)
async def afk_mentioned(c: megux, m: Message):
    if m.entities:
        for y in m.entities:
            if y.type == enums.MessageEntityType.MENTION:
                x = re.search("@(\w+)", m.text)  # Regex to get @username
                try:
                    user = await c.get_users(x.group(1))
                except FloodWait as e:  # Avoid FloodWait
                    await asyncio.sleep(e.value)
                except (IndexError, BadRequest, KeyError):
                    return
                try:
                    user_id = user.id
                    user_first_name = user.first_name
                except UnboundLocalError:
                    return
                except FloodWait as e:  # Avoid FloodWait
                    await asyncio.sleep(e.value)
            else:
                return
    elif m.reply_to_message and m.reply_to_message.from_user:
        try:
            user_id = m.reply_to_message.from_user.id
            user_first_name = m.reply_to_message.from_user.first_name
        except AttributeError:
            return
    else:
        return

    try:
        if user_id == m.from_user.id:
            return
    except AttributeError:
        return
    except FloodWait as e:  # Avoid FloodWait
        await asyncio.sleep(e.value)

    try:
        await m.chat.get_member(user_id)  # Check if the user is in the group
        pass
    except UserNotParticipant:
        return

    AFK = get_collection(f"_AFK {user_id}") 
    user_afk = await AFK.find_one({"_afk": "on"})

    if not user_afk:
        return
    else:
        afkmsg = (await get_string(m.chat.id, "IS_AFK")).format(user_first_name)
        await m.reply_text(afkmsg)
    await m.stop_propagation()
