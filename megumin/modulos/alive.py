from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from megumin import megux, version

@megux.on_message(filters.command(["alive"]))
async def start(_, message):
    chats = await megux.get_send_as_chats(chat_id)
    text= f"""ᴏɪ ᴇᴜ ᴇsᴛᴏᴜ ᴠɪᴠᴏ!\n**• Versão do Bot **: {version.__megumin_version__}\n**• Versão do Python **: {version.__python_version__}\n**• Versão do Pyrogram **: {version.__pyro_version__} os vejo em {chats}"""
    
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
