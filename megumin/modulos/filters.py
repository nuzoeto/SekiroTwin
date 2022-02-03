from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

@megux.on_message(filters.regex(r"^framengo"))
async def framengo(c: megux, m: Message):
    await m.reply_video(
        video="https://telegra.ph/file/edead6d5de1df2eb2ab84.mp4",
    )
