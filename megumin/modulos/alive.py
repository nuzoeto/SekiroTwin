from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from megumin import megux

@megux.on_message(filters.command(["alive"]))
async def start(_, message):
    text= "ᴏɪ ᴇᴜ ᴇsᴛᴏᴜ ᴠɪᴠᴏ!\n**• Versão do Bot **: {__megumin_version__}\n**• Versão do Python **: {__python_version__}\n**• Versão do Pyrogram **: {__pyro_version__}"
    
    keyboard = InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton (text="✨ Me adicione a um grupo", url="t.me/whiterkangbot?startgroup=new")
                                ]
                            ]
                        )
    
    await message.reply_animation(
     animation="https://telegra.ph/file/a003598d771e24f4abb13.gif",
        caption=text,
        reply_markup=keyboard)
