import os

from shazamio import Shazam

from megumin import megux, Config

shazam = Shazam()

@megux.on_message(filters.command(["whichsong"], Config.TRIGGER))
async def which_song(c: megux, message: Message):
    """ discover song using shazam"""
    replied = message.reply_to_message
    if not replied or not replied.audio:
        await message.reply("<code>Reply audio needed.</code>")
        return
    sent = await message.reply("<i>Downloading audio..</i>")
    file = await c.download_media(
                message=message.reply_to_message,
                file_name=Config.DOWN_PATH
            )
    try:
        await sent.edit("<i>Detecting song...</i>")
        res = await shazam.recognize_song(file)
    except Exception as e:
        await message.reply(e)
        os.remove(file)
        return await sent.edit("<i>Failed to get sound data.</i>")
    song = res["track"]
    out = f"<b>Song Detected!\n\n{song['title']}</b>\n<i>- {song['subtitle']}</i>"
    try:
        await sent.delete()
        await message.reply_photo(photo=song["images"]["coverart"], caption=out)
    except KeyError:
        await sent.edit(out)
    except Exception:
        os.remove(file)
        return await sent.edit("<i>Failed to get sound data.</i>")
    os.remove(file)
