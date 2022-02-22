from pyrogram import filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from megumin import megux, version
from megumin import START_TIME
from megumin.utils import time_formatter


@megux.on_message(filters.command(["alive"]))
async def start(_, message):
    text= f"""ᴏɪ ᴇᴜ ᴇsᴛᴏᴜ ᴠɪᴠᴏ!\n**• Versão do Bot **: {version.__megumin_version__}\n**• Versão do Python **: {version.__python_version__}\n**• Versão do Pyrogram **: {version.__pyro_version__}"""
    
    keyboard = InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton (text="✨ Me adicione a um grupo", url="t.me/whiterkangbot?startgroup=new"),
                                    InlineKeyboardButton(text="❔Curioso", callback_data="alive_status")
                                ]
                            ]
                        )

@megux.on_callback_query(filters.regex(pattern=r"^alive_status$"))
async def help_ani_(client: megux, cb: CallbackQuery):
    await cb.answer(f"""Uptime: """, show_alert=True)
    

    await message.reply_animation(
     animation="https://telegra.ph/file/a003598d771e24f4abb13.gif",
        caption=text,
        reply_markup=keyboard)
