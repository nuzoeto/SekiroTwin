import html

from pyrogram.types import Message

from megumin import megux
from megumin.utils import get_collection, is_dev, sw, tld, check_rights, is_self

db = get_collection("ANTISPAM_CHATS")
gban_db = get_collection("GBAN")

LOGS = Config.GBAN_LOGS

async def gban_user(m: Message, user_id: int, user_name: str, admin_name: str, reason: str):
    if is_dev(user_id):
        await m.reply(await tld(m.chat.id, "ANTISPAM_ERR_USR_SUDO"))
        await gban_db.delete_many({"user_id": user_id})
        return
    elif await is_self(user_id):
        await m.reply(await tld(m.chat.id, "ANTISPAM_ERR_USR_BOT"))
    else:
        gban_results = await gban_db.find_one({"user_id": user_id})
        if not gban_results:
            if reason == "None":
                await m.reply(await tld(m.chat.id, "ANTISPAM_NO_REASON"))
                return
            
            await gban_db.insert_one({"user_id": user_id, "reason": reason})

            find_chats = db.find()
        
            for chats in find_chats:
                chat_id = chats["chat_id"]
#               # Try ban user gbanned
                try:
                    if not await check_rights(chat_id, megux.me.id, "can_restrict_members"):
                        pass
                
                    await megux.ban_chat_member(chat_id, user_id)
                except Exception:
                    continue
            await m.reply((await tld(m.chat.id, "ANTISPAM_NEW_GBAN")).format(user_name, user_id, reason))
            if not LOGS == "None":
                group_logs = LOGS
                try:
                    id_log = int(group_logs)
                    await megux.send_message(id_log, (await tld(id_logs, "ANTISPAM_LOGGER_NEW_GBAN")).format(admin_name, user_name, user_id, reason))
                    return
                except Exception as e:
                    await asyncio.gather(megux.send_err(e))
                    return
        else:
            if reason == "None":
                await m.reply(await tld(m.chat.id, "ANTISPAM_ERR_NO_NEW_REASON"))
                return
            else:
                try:
                    old_find = await gban_db.find_one({"user_id": user_id})
                    old_reason = old_find["reason"]
                    await gban_db.update_one({"user_id" : user_id}, {"$set": {"reason": reason}})
                except Exception as e:
                    await m.reply(e)
                    return
                await m.reply((await tld("ANTISPAM_REASON_UPDATED")).format(old_reason, reason))
                if not LOGS == "None":
                    group_logs = LOGS
                    try:
                        id_log = int(group_logs)
                        await megux.send_message(id_log, (await tld(id_logs, "ANTISPAM_LOGGER_UPDATE_GBAN")).format(admin_name, user_name, user_id, reason))
                        return
                    except Exception as e:
                        await asyncio.gather(megux.send_err(e))
                        return
