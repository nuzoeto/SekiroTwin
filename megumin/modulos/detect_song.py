import os
import asyncio
import speech_recognition as sr

from shazamio import Shazam

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux, Config


shazam = Shazam()
recognizer = sr.Recognizer()

@megux.on_message(filters.command(["whichsong", "detectsong"], Config.TRIGGER))
async def which_song(c: megux, message: Message):
    """ discover song using shazam"""
    replied = message.reply_to_message
    if not replied or not (replied.audio, replied.voice):
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
        await sent.edit(e)
        os.remove(file)
        return await sent.edit("<i>Failed to get sound data.</i>")
    try:
        song = res["track"]
    except KeyError:
        await sent.edit("<i>Failed to get sound data.</i>")
        return
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

    
@megux.on_message(filters.voice)
async def transcriber(c: megux, m: Message):
    if m.voice:
        sent = await m.reply("<i>Fazendo  Download do Áudio..</i>")
        try:
            file = await c.download_media(
                        message=m.voice,
                        file_name=Config.DOWN_PATH
                    )
        except Exception as e:
            await sent.edit(f"<i>Ocorreu um erro: {e}")
        
        with sr.AudioFile(file) as source:
            audio = recognizer.record(source)
            try:
                await sent.edit("Transcrevendo Fala em Texto...")
                text = recognizer.recognize_google(audio, language="pt-BR")
                await sent.edit(f"<b>Texto:</b> <i>{text}</i>")
            except sr.UnknownValueError:
                await sent.edit("<i>Não consegui, Identificar o que você quis dizer com isso.")
                await asyncio.sleep(5)
                await sent.delete()
            except sr.RequestError:
                await sent.edit("<i>O Serviço de conversão de fala em texto, Não está disponivel no momento.</i>")
                await asyncio.sleep(5)
                await sent.delete()
