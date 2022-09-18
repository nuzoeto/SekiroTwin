from megumin.utils import get_collection, tld


async def check_afk(m, user_id, user_fn, user):
    if user_id == user.id:
        return
      
    AFK = get_collection("_AFK")
    REASON = get_collection("REASON_AFK")
      
    if await AFK.find_one({"user_id": user_id, "_afk": "on"}):
        try:
            await m.chat.get_member(int(user_id))  # Check if the user is in the group
        except (UserNotParticipant, PeerIdInvalid):
            return

        
        if await REASON.find_one({"user_id": user_id}):
            db = await REASON.find_one({"user_id": user_id})
            r = db["_reason"]
            afkmsg = (await tld(m.chat.id, "IS_AFK_REASON")).format(user_fn, r)
        else:
            afkmsg = (await tld(m.chat.id, "IS_AFK")).format(user_fn)
        try:
            return await m.reply_text(afkmsg)
        except ChatWriteForbidden:
            return
