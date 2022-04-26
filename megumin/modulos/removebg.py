import os
from datetime import datetime

from removebg import RemoveBg

from pyrogram import filters 
from pyrogram.types import Message 

from megumin import megux, Config 


IMG_PATH = Config.DOWN_PATH + "dl_image.jpg"



@megux.on_message(filters.command("removebg", Config.TRIGGER))
async def remove_background(_, message: Message):
    if not Config.REMOVE_BG_API_KEY:
        await message.reply(
            "Get the API from <a href='https://www.remove.bg/b/background-removal-api'>HERE "
            "</a> & add it to Heroku Config Vars <code>REMOVE_BG_API_KEY</code>",
            disable_web_page_preview=True,
            parse_mode="html",
        )
        return
    replied = message.reply_to_message
    if (
        replied
        and replied.media
        and (
            replied.photo
            or (replied.document and "image" in replied.document.mime_type)
        )
    ):
        msg = await message.reply("Analisando...")
        start_t = datetime.now()
        if os.path.exists(IMG_PATH):
            os.remove(IMG_PATH)
        await megux.download_media(
            message=replied,
            file_name=IMG_PATH,
        )
        await msg.edit("Baixando imagem...")
        end_t = datetime.now()
        m_s = (end_t - start_t).seconds
        await msg.edit(f"Image saved in {m_s} seconds.\nRemoving Background Now...")
        # Cooking Image
        try:
            await msg.edit("Enviando imagem...")
            rmbg = RemoveBg(Config.REMOVE_BG_API_KEY, "removebg_error.log")
            rmbg.remove_background_from_img_file(IMG_PATH)
            rbg_img_path = IMG_PATH + "_no_bg.png"
            start_t = datetime.now()
            await megux.send_document(
                chat_id=message.chat.id,
                document=rbg_img_path,
                disable_notification=True,
            )
            await msg.delete()
        except Exception:
            await message.reply("Something went wrong!\nCheck your usage quota!")
            return
    else:
        await message.reply("Reply to a photo to remove background!")
