import os
import shutil
import tempfile

from megumin import megux

@megux.on_message(filters.command("getsticker"))
async def getsticker(c: megux, m: Message):
    sticker = m.reply_to_message.sticker
    if sticker:
        if sticker.is_animated:
            await m.reply_text("sticker nao suportado!")
        elif not sticker.is_animated:
            with tempfile.TemporaryDirectory() as tempdir:
                path = os.path.join(tempdir, "getsticker")
            sticker_file = await c.download_media(
                message=m.reply_to_message,
                file_name=f"{path}/{sticker.set_name}.png",
            )
            await m.reply_to_message.reply_document(
                document=sticker_file,
                caption=("from @WhiterKangBot")(
                    sticker.emoji, sticker.file_id
                ),
            ),
            shutil.rmtree(tempdir, ignore_errors=True)
    else:
        await m.reply_text("Vou enviar o vento?")
        return