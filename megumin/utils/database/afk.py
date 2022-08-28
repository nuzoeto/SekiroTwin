from megumin.utils import get_collection, tld


async def check_afk(m, user_id, user_fn, user):
    if user_id == user.id:
        return
      
    AFK = get_collection(f"_AFK {user_id}")
    REASON = get_collection(f"REASON {user_id}")
      
    if await AFK.find_one({"_afk": "on"}):
        try:
            await m.chat.get_member(int(user_id))  # Check if the user is in the group
        except (UserNotParticipant, PeerIdInvalid):
            return

        
        if await REASON.find_one():
            db = await REASON.find_one()
            r = db["_reason"]
            afkmsg = (await tld(m.chat.id, "IS_AFK_REASON")).format(user_fn, r)
        else:
            afkmsg = (await tld(m.chat.id, "IS_AFK")).format(user_fn)
        try:
            return await m.reply_text(afkmsg)
        except ChatWriteForbidden:
            return
