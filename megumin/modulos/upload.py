import io
import os
import math
import re
import time
import asyncio
from datetime import datetime
from pathlib import Path
from pySmartDL import SmartDL
from PIL import Image
from hachoir.metadata import extractMetadata
from typing import Tuple, Union
from urllib.parse import unquote_plus

from hachoir.parser import createParser
from pyrogram.errors import FloodWait
from pyrogram.enums import ParseMode, ChatAction 
from pyrogram import filters 
from pyrogram.types import Message 

from megumin import megux, Config
from megumin.utils import humanbytes, tld 
from megumin.utils.decorators import input_str

class ProcessCanceled(Exception):
    """raise if thread has terminated"""
    
    
FINISHED_PROGRESS_STR = os.environ.get("FINISHED_PROGRESS_STR")
UNFINISHED_PROGRESS_STR = os.environ.get("UNFINISHED_PROGRESS_STR")
PTN_SPLIT = re.compile(r'(\.\d+|\.|\d+)')



@megux.on_message(filters.command("upload", Config.TRIGGER))
async def upload_(_, m: Message):
    url = input_str(m)
    if not url:
        return await m.reply("Vou enviar o Vento?")
    is_url = re.search(r"(?:https?|ftp)://[^|\s]+\.[^|\s]+", url)
    del_path = False
    if is_url:
        del_path = True
        try:
            path_, _ = await url_download(m, url)
        except ProcessCanceled:
            await m.reply("`Process Canceled!`")
            return
        except Exception as e_e:  # pylint: disable=broad-except
            await m.reply(str(e_e))
            return
    if "|" in path_:
        path_, file_name = path_.split("|")
        path_ = path_.strip()
        if os.path.isfile(path_):
            new_path = os.path.join(Config.DOWN_PATH, file_name.strip())
            os.rename(path_, new_path)
            path_ = new_path
    try:
        string = Path(path_)
    except IndexError:
        await m.reply("wrong syntax\n`.upload [path]`")
    else:
        await upload_path(message=m, path=string, del_path=del_path)
        
        
async def url_download(message: Message, url: str) -> Tuple[str, int]:
    """download from link"""
    msg = await message.reply(await tld(message.chat.id, "DOWNLOAD_YT"))
    start_t = datetime.now()
    custom_file_name = unquote_plus(os.path.basename(url))
    if "|" in url:
        url, c_file_name = url.split("|", maxsplit=1)
        url = url.strip()
        if c_file_name:
            custom_file_name = c_file_name.strip()
    dl_loc = os.path.join(Config.DOWN_PATH, custom_file_name)
    downloader = SmartDL(url, dl_loc, progress_bar=False)
    downloader.start(blocking=False)
    count = 0
    while not downloader.isFinished():
        total_length = downloader.filesize or 0
        downloaded = downloader.get_dl_size()
        percentage = downloader.get_progress() * 100
        speed = downloader.get_speed(human=True)
        estimated_total_time = downloader.get_eta(human=True)
        count += 1
        if count >= 10:
            count = 0
        await asyncio.sleep(1)
    await msg.edit(await tld(message.chat.id, "UPLOAD_DOWNLOAD_FINISHED"))
    await asyncio.sleep(5)
    await msg.delete()
    return dl_loc, (datetime.now() - start_t).seconds

async def upload_path(message: Message, path: Path, del_path: bool):
    file_paths = []
    if path.exists():
        def explorer(_path: Path) -> None:
            if _path.is_file() and _path.stat().st_size:
                file_paths.append(_path)
            elif _path.is_dir():
                for i in sorted(_path.iterdir(), key=lambda a: (a.name)):
                    explorer(i)
        explorer(path)
    else:
        path = path.expanduser()
        str_path = os.path.join(*(path.parts[1:] if path.is_absolute() else path.parts))
        for p in Path(path.root).glob(str_path):
            file_paths.append(p)
    current = 0
    for p_t in file_paths:
        current += 1
        try:
            await upload(message, p_t, del_path, f"{current}/{len(file_paths)}")
        except FloodWait as f_e:
            time.sleep(f_e.value)  


async def upload(message: Message, path: Path, del_path: bool = False, extra: str = '', with_thumb: bool = True):
    if path.name.lower().endswith(
            (".mkv", ".mp4", ".webm", ".m4v")):
        await vid_upload(message, path, del_path, extra, with_thumb)
    elif path.name.lower().endswith(
            (".mp3", ".flac", ".wav", ".m4a")):
        await audio_upload(message, path, del_path, extra, with_thumb)
    elif path.name.lower().endswith(
            (".jpg", ".jpeg", ".png", ".bmp")):
        await photo_upload(message, path, del_path, extra)
    else:
        await doc_upload(message, path, del_path, extra, with_thumb)


async def doc_upload(message: Message, path, del_path: bool = False, extra: str = '', with_thumb: bool = True):
    str_path = str(path)
    sent: Message = await megux.send_message(
        message.chat.id, f"`Uploading {str_path} as a doc ... {extra}`")
    start_t = datetime.now()
    await megux.send_chat_action(message.chat.id, ChatAction.UPLOAD_DOCUMENT)
    try:
        msg = await megux.send_document(
            chat_id=message.chat.id,
            document=str_path,
            caption=path.name,
            parse_mode=ParseMode.HTML,
            force_document=True,
            disable_notification=True,
        )
    except ValueError as e_e:
        await sent.edit(f"Skipping `{str_path}` due to {e_e}")
    except Exception as u_e:
        await sent.edit(str(u_e))
        raise u_e
    else:
        await sent.delete()
        await finalize(message, msg, start_t)
        if os.path.exists(str_path) and del_path:
            os.remove(str_path)


async def vid_upload(message: Message, path, del_path: bool = False, extra: str = '', with_thumb: bool = True):
    str_path = str(path)
    duration = 0
    metadata = extractMetadata(createParser(str_path))
    if metadata and metadata.has("duration"):
        duration = metadata.get("duration").seconds
    sent: Message = await megux.send_message(
        message.chat.id, f"`Uploading {str_path} as a video ... {extra}`")
    start_t = datetime.now()
    await megux.send_chat_action(message.chat.id, ChatAction.UPLOAD_VIDEO)
    width = 0
    height = 0
    if thumb:
        t_m = extractMetadata(createParser(thumb))
        if t_m and t_m.has("width"):
            width = t_m.get("width")
        if t_m and t_m.has("height"):
            height = t_m.get("height")
    try:
        msg = await megux.send_video(
            chat_id=message.chat.id,
            video=str_path,
            duration=duration,
            width=width,
            height=height,
            caption=path.name,
            parse_mode=ParseMode.HTML,
            disable_notification=True,
        )
    except ValueError as e_e:
        await sent.edit(f"Skipping `{str_path}` due to {e_e}")
    except Exception as u_e:
        await sent.edit(str(u_e))
        raise u_e
    else:
        await sent.delete()
        await remove_thumb(thumb)
        await finalize(message, msg, start_t)
        if os.path.exists(str_path) and del_path:
            os.remove(str_path)


async def audio_upload(message: Message, path, del_path: bool = False, extra: str = '', with_thumb: bool = True):
    title = None
    artist = None
    thumb = None
    duration = 0
    str_path = str(path)
    file_size = humanbytes(os.stat(str_path).st_size)
    metadata = extractMetadata(createParser(str_path))
    if metadata and metadata.has("title"):
        title = metadata.get("title")
    if metadata and metadata.has("artist"):
        artist = metadata.get("artist")
    if metadata and metadata.has("duration"):
        duration = metadata.get("duration").seconds
    sent: Message = await megux.send_message(
        message.chat.id, f"`Uploading {str_path} as audio ... {extra}`")
    start_t = datetime.now()
    await megux.send_chat_action(message.chat.id, ChatAction.UPLOAD_AUDIO)
    try:
        msg = await megux.send_audio(
            chat_id=message.chat.id,
            audio=str_path,
            caption=f"{path.name}\n[ {file_size} ]",
            title=title,
            performer=artist,
            duration=duration,
            parse_mode=ParseMode.HTML,
            disable_notification=True,
        )
    except ValueError as e_e:
        await sent.edit(f"Skipping `{str_path}` due to {e_e}")
    except Exception as u_e:
        await sent.edit(str(u_e))
        raise u_e
    else:
        await sent.delete()
        await finalize(message, msg, start_t)
        if os.path.exists(str_path) and del_path:
            os.remove(str_path)

async def photo_upload(message: Message, path, del_path: bool = False, extra: str = ''):
    str_path = str(path)
    sent: Message = await megux.send_message(
        message.chat.id, f"`Uploading {path.name} as photo ... {extra}`")
    start_t = datetime.now()
    await megux.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
    try:
        msg = await megux.send_photo(
            chat_id=message.chat.id,
            photo=str_path,
            caption=path.name,
            parse_mode=ParseMode.HTML,
            disable_notification=True,
        )
    except ValueError as e_e:
        await sent.edit(f"Skipping `{str_path}` due to {e_e}")
    except Exception as u_e:
        await sent.edit(str(u_e))
        raise u_e
    else:
        await sent.delete()
        await finalize(message, msg, start_t)
        if os.path.exists(str_path) and del_path:
            os.remove(str_path)


async def finalize(message: Message, msg: Message, start_t):
    end_t = datetime.now()
    m_s = (end_t - start_t).seconds
    await msg.edit(f"Uploaded in {m_s} seconds")
    
