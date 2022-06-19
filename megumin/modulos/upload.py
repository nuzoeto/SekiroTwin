import asyncio
import math
import os
import re
import stagger
import time
import io

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from datetime import datetime
from pathlib import Path
from typing import Tuple, Union
from urllib.parse import unquote_plus

from pySmartDL import SmartDL

from pyrogram import filters
from pyrogram.enums import ParseMode 
from pyrogram.errors import FloodWait
from pyrogram.types import Message, CallbackQuery  
from megumin import megux, Config 
from megumin.utils import humanbytes
from megumin.utils.decorators import input_str

FINISHED_PROGRESS_STR = os.environ.get("FINISHED_PROGRESS_STR")
UNFINISHED_PROGRESS_STR = os.environ.get("UNFINISHED_PROGRESS_STR")
LOGO_PATH = "resources/blackground.jpeg"
THUMB_PATH = Config.DOWN_PATH + "thumb_image.jpg"


class ProcessCanceled(Exception):
    """raise if thread has terminated"""


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
            url, _ = await url_download(m, url)
        except ProcessCanceled:
            await msg.edit("`Process Canceled!`")
            return
        except Exception as e_e:  # pylint: disable=broad-except
            await m.reply(str(e_e))
            return
    if "|" in url:
        url, file_name = path_.split("|")
        url = path_.strip()
        if os.path.isfile(url):
            new_path = os.path.join(Config.DOWN_PATH, file_name.strip())
            os.rename(path_, new_path)
            path_ = new_path
    try:
        string = Path(url)
    except IndexError:
        await msg.edit("wrong syntax\n`.upload [path]`")
    else:
        await upload_path(message=m, path=string, del_path=del_path)


async def url_download(message: Message, url: str) -> Tuple[str, int]:
    """download from link"""
    msg = await message.reply("`Uploading...`")
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
            for i in range(20 - math.floor(percentage / 5)):
                await msg.edit(f"Downloaded: {percentage}% | {humanbytes(downloaded)}\n\nETA: {estimated_total_time}\n\nSpeed: {speed}\n\nSize: {total_length}", disable_web_page_preview=True)
            await asyncio.sleep(4)
            await msg.delete()
        await asyncio.sleep(1)
    return dl_loc, (datetime.now() - start_t).seconds


async def upload_path(message: Message, path: Path, del_path: bool):
    file_paths = []
    if path.exists():

        def explorer(_path: Path) -> None:
            if _path.is_file() and _path.stat().st_size:
                file_paths.append(_path)
            elif _path.is_dir():
                for i in sorted(_path.iterdir()):
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
            await upload(
                message=message,
                path=p_t,
                del_path=del_path,
                extra=f"{current}/{len(file_paths)}",
            )
        except FloodWait as f_e:
            time.sleep(f_e.x)  # asyncio sleep ?


async def upload(
    message: Message,
    path: Path,
    del_path: bool = False,
    callback: CallbackQuery = None,
    extra: str = "",
    with_thumb: bool = True,
    custom_thumb: str = "",
    log: bool = True,
):
    m_text = input_str(message)
    if "-wt" in m_text:
        with_thumb = False
    if path.name.lower().endswith((".mkv", ".mp4", ".webm")) and (
        "-d" not in m_text
    ):
        return await vid_upload(
            message=message,
            path=path,
            del_path=del_path,
            callback=callback,
            extra=extra,
            with_thumb=with_thumb,
            custom_thumb=custom_thumb,
            log=log,
        )
    elif path.name.lower().endswith((".mp3", ".flac", ".wav", ".m4a")) and (
        "-d" not in m_text
    ):
        return await audio_upload(
            message=message,
            path=path,
            del_path=del_path,
            callback=callback,
            extra=extra,
            with_thumb=with_thumb,
            log=log,
        )
    elif path.name.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")) and (
        "-d" not in m_text 
    ):
        await photo_upload(message, path, del_path, extra)
    else:
        await doc_upload(message, path, del_path, extra, with_thumb)


async def doc_upload(
    message: Message,
    path,
    del_path: bool = False,
    extra: str = "",
    with_thumb: bool = True,
):
    str_path = str(path)
    sent: Message = await megux.send_message(
        message.chat.id, f"`Uploading {str_path} as a doc ... {extra}`"
    )
    start_t = datetime.now()
    thumb = None
    if with_thumb:
        thumb = await get_thumb(str_path)
    try:
        msg = await megux.send_document(
            chat_id=message.chat.id,
            document=str_path,
            thumb=thumb,
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


async def vid_upload(
    message: Message,
    path,
    del_path: bool = False,
    callback: CallbackQuery = None,
    extra: str = "",
    with_thumb: bool = True,
    custom_thumb: str = "",
    log: bool = True,
):
    str_path = str(path)
    thumb = None
    if with_thumb:
        if custom_thumb:
            try:
                thumb = await check_thumb(custom_thumb)
            except Exception as e_r:
                await message.reply(str(e_r))
        if not thumb:
            thumb = await get_thumb(str_path)
    duration = 0
    metadata = extractMetadata(createParser(str_path))
    if metadata and metadata.has("duration"):
        duration = metadata.get("duration").seconds
    sent: Message = await megux.send_message(
        message.chat.id, f"`Uploading {str_path} as a video ... {extra}`"
    )
    start_t = datetime.now()
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
            thumb=thumb,
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
        if log:
            await finalize(message, msg, start_t)
        if os.path.exists(str_path) and del_path:
            os.remove(str_path)
        return msg


async def check_thumb(thumb_path: str):
    f_path = os.path.splitext(thumb_path)
    if f_path[1] != ".jpg":
        new_thumb_path = f"{f_path[0]}.jpg"
        Image.open(thumb_path).convert("RGB").save(new_thumb_path, "JPEG")
        os.remove(thumb_path)
        thumb_path = new_thumb_path
    return thumb_path


async def audio_upload(
    message: Message,
    path,
    del_path: bool = False,
    callback: CallbackQuery = None,
    extra: str = "",
    with_thumb: bool = True,
    log: bool = True,
):
    title = None
    artist = None
    thumb = None
    duration = 0
    str_path = str(path)
    file_size = humanbytes(os.stat(str_path).st_size)
    if with_thumb:
        try:
            album_art = stagger.read_tag(str_path)
            if album_art.picture and not os.path.lexists(Config.THUMB_PATH):
                bytes_pic_data = album_art[stagger.id3.APIC][0].data
                bytes_io = io.BytesIO(bytes_pic_data)
                image_file = Image.open(bytes_io)
                image_file.save("album_cover.jpg", "JPEG")
                thumb = "album_cover.jpg"
        except stagger.errors.NoTagError:
            pass
        if not thumb:
            thumb = await get_thumb(str_path)
    metadata = extractMetadata(createParser(str_path))
    if metadata and metadata.has("title"):
        title = metadata.get("title")
    if metadata and metadata.has("artist"):
        artist = metadata.get("artist")
    if metadata and metadata.has("duration"):
        duration = metadata.get("duration").seconds
    sent: Message = await megux.send_message(
        message.chat.id, f"`Uploading {str_path} as audio ... {extra}`"
    )
    start_t = datetime.now()
    try:
        msg = await megux.send_audio(
            chat_id=message.chat.id,
            audio=str_path,
            thumb=thumb,
            caption=f"{path.name} [ {file_size} ]",
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
        if log:
            await finalize(message, msg, start_t)
        if os.path.exists(str_path) and del_path:
            os.remove(str_path)
    if os.path.lexists("album_cover.jpg"):
        os.remove("album_cover.jpg")
    return msg


async def photo_upload(message: Message, path, del_path: bool = False, extra: str = ""):
    str_path = str(path)
    sent: Message = await megux.send_message(
        message.chat.id, f"`Uploading {path.name} as photo ... {extra}`"
    )
    start_t = datetime.now()
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


async def get_thumb(path: str = ""):
    if os.path.exists(THUMB_PATH):
        return THUMB_PATH
    if path:
        types = (".jpg", ".webp", ".png")
        if path.endswith(types):
            return None
        file_name = os.path.splitext(path)[0]
        for type_ in types:
            thumb_path = file_name + type_
            if os.path.exists(thumb_path):
                if type_ != ".jpg":
                    new_thumb_path = f"{file_name}.jpg"
                    Image.open(thumb_path).convert("RGB").save(new_thumb_path, "JPEG")
                    os.remove(thumb_path)
                    thumb_path = new_thumb_path
                return thumb_path
        metadata = extractMetadata(createParser(path))
        if metadata and metadata.has("duration"):
            return await take_screen_shot(path, metadata.get("duration").seconds)
    if os.path.exists(LOGO_PATH):
        return LOGO_PATH
    return None


async def remove_thumb(thumb: str) -> None:
    if (
        thumb
        and os.path.exists(thumb)
        and thumb != LOGO_PATH
        and thumb != Config.THUMB_PATH
    ):
        os.remove(thumb)

async def finalize(message: Message, msg: Message, start_t):
        end_t = datetime.now()
        m_s = (end_t - start_t).seconds
        await msg.edit(f"Uploaded in {m_s} seconds")
