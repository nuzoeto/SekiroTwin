import io
import os
import time
from datetime import datetime
from pathlib import Path

from PIL import Image
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pyrogram.errors import FloodWait
from pyrogram.enums import ParseMode 
from pyrogram import filters 
from pyrogram.types import Message 

from megumin import megux


async def upload_path(message: Message, path: Path, del_path: bool):
    file_paths = []
    if path.exists():
        def explorer(_path: Path) -> None:
            if _path.is_file() and _path.stat().st_size:
                file_paths.append(_path)
            elif _path.is_dir():
                for i in sorted(_path.iterdir(), key=lambda a: sort_file_name_key(a.name)):
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
            (".mkv", ".mp4", ".webm", ".m4v")) and ('d' not in message.flags):
        await vid_upload(message, path, del_path, extra, with_thumb)
    elif path.name.lower().endswith(
            (".mp3", ".flac", ".wav", ".m4a")) and ('d' not in message.flags):
        await audio_upload(message, path, del_path, extra, with_thumb)
    elif path.name.lower().endswith(
            (".jpg", ".jpeg", ".png", ".bmp")) and ('d' not in message.flags):
        await photo_upload(message, path, del_path, extra)
    else:
        await doc_upload(message, path, del_path, extra, with_thumb)


async def doc_upload(message: Message, path, del_path: bool = False, extra: str = '', with_thumb: bool = True):
    str_path = str(path)
    sent: Message = await megux.send_message(
        message.chat.id, f"`Uploading {str_path} as a doc ... {extra}`")
    start_t = datetime.now()
    await megux.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
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
    await megux.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_VIDEO)
    width = 0
    height = 0
    if thumb:
        t_m = extractMetadata(createParser(thumb))
        if t_m and t_m.has("width"):
            width = t_m.get("width")
        if t_m and t_m.has("height"):
            height = t_m.get("height")
    try:
        msg = await message.client.send_video(
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
