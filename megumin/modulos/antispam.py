import asyncio
from pyrogram import filters
from pyrogram.types import Message

from megumin import megux, Config
from megumin.utils import check_rights, get_collection, is_dev, tld

@megux.on_message(filters.command(["antispam on", "antispam true"], Config.TRIGGER) & filters.group)
async def enable_antispam_message(c: megux, m: Message):
    db = get_collection("ANTISPAM_CHATS")
    if not await check_rights(m.chat.id, m.from_user.id, "can_change_info"):
        return
    await db.update_one({"chat_id": m.chat.id}, {"$set": {"status": True}}, upsert=True)
    await m.reply_text("Antispam Ativado.")
    
    
@megux.on_message(filters.command(["antispam off", "antispam false"], Config.TRIGGER) & filters.group)
async def disable_antispam_message(c: megux, m: Message):
    db = get_collection("ANTISPAM_CHATS")
    if not await check_rights(m.chat.id, m.from_user.id, "can_change_info"):
        return
    await db.update_one({"chat_id": m.chat.id}, {"$set": {"status": False}}, upsert=True)
    await m.reply_text("Antispam Desativado.")
    
    
@megux.on_message(filters.command("antispam", Config.TRIGGER) & filters.group)
async def enable_welcome_message(c: megux, m: Message):
    if not await check_rights(m.chat.id, m.from_user.id, "can_change_info"):
        return
    await m.reply_text("Dê um argumento exemplo: /antispam on/off/true/false")
