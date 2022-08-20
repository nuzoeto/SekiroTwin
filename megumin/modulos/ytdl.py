#CREDITS https://github.com/ruizlenato/SmudgeLord/blob/rewrite/smudge/plugins/videos.py
import io
import os
import re
import random
import rapidjson
import shutil
import asyncio
import tempfile
import datetime
import httpx
import gallery_dl


from yt_dlp import YoutubeDL
from typing import Tuple, Callable
from functools import wraps, partial

from pyrogram.helpers import ikb
from pyrogram import filters, enums
from pyrogram.errors import BadRequest, FloodWait, Forbidden, MediaEmpty, MessageNotModified
from pyrogram.types import Message, CallbackQuery, InputMediaVideo, InputMediaPhoto

from megumin import megux, Config 
from megumin.utils import humanbytes, tld


http = httpx.AsyncClient()


YOUTUBE_REGEX = re.compile(
    r"(?m)http(?:s?):\/\/(?:www\.)?(?:music\.)?youtu(?:be\.com\/(watch\?v=|shorts/|embed/)|\.be\/|)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?"
)

SDL_REGEX_LINKS = r"^http(?:s)?:\/\/(?:www\.)?(?:v\.)?(?:mobile.|m.)?(?:instagram.com|twitter.com|vm.tiktok.com|tiktok.com|facebook.com)\/(?:\S*)"

TIME_REGEX = re.compile(r"[?&]t=([0-9]+)")

MAX_FILESIZE = 1000000000


def aiowrap(func: Callable) -> Callable:
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run

@aiowrap
def extract_info(instance: YoutubeDL, url: str, download=True):
    return instance.extract_info(url, download)


@aiowrap
def gallery_down(path, url: str):
    gallery_dl.config.set(("output",), "mode", "null")
    gallery_dl.config.set((), "directory", [])
    gallery_dl.config.set((), "base-directory", [path])
    gallery_dl.config.set(
        (),
        "cookies",
        "~/instagram.com_cookies.txt",
    )
    return gallery_dl.job.DownloadJob(url).run()


@megux.on_message(filters.command("ytdl", Config.TRIGGER))
async def ytdlcmd(c: megux, m: Message):
    user = m.from_user.id

    if m.reply_to_message and m.reply_to_message.text:
        url = m.reply_to_message.text
    elif len(m.command) > 1:
        url = m.text.split(None, 1)[1]
    else:
        await m.reply_text(await tld(m.chat.id, "NO_ARGS_YT"))
        return

    ydl = YoutubeDL({"noplaylist": True})

    rege = YOUTUBE_REGEX.match(url)

    t = TIME_REGEX.search(url)
    temp = t.group(1) if t else 0

    if not rege:
        yt = await extract_info(ydl, f"ytsearch:{url}", download=False)
        try:
            yt = yt["entries"][0]
        except IndexError:
            return
    else:
        yt = await extract_info(ydl, rege.group(), download=False)

    for f in yt["formats"]:
        if f["format_id"] == "140":
            afsize = f["filesize"] or 0
        if f["ext"] == "mp4" and f["filesize"] is not None:
            vfsize = f["filesize"] or 0
            vformat = f["format_id"]

    keyboard = [
        [
            (
                await tld(m.chat.id, "SONG_BNT"),
                f'_aud.{yt["id"]}|{afsize}|{vformat}|{temp}|{user}|{m.id}',
            ),
            (
                await tld(m.chat.id, "VID_BNT"),
                f'_vid.{yt["id"]}|{vfsize}|{vformat}|{temp}|{user}|{m.id}',
            ),
        ]
    ]

    if " - " in yt["title"]:
        performer, title = yt["title"].rsplit(" - ", 1)
    else:
        performer = yt.get("creator") or yt.get("uploader")
        title = yt["title"]

    text = f"🎧 <b>{performer}</b> - <i>{title}</i>\n"
    text += f"💾 <code>{humanbytes(afsize)}</code> (audio) / <code>{humanbytes(int(vfsize))}</code> (video)\n"
    text += f"⏳ <code>{datetime.timedelta(seconds=yt.get('duration'))}</code>"

    await m.reply_text(text, reply_markup=ikb(keyboard))


@megux.on_callback_query(filters.regex("^(_(vid|aud))"))
async def cli_ytdl(c: megux, cq: CallbackQuery):
    try:
        data, fsize, vformat, temp, userid, mid = cq.data.split("|")
    except ValueError:
        return print(cq.data)
    if cq.from_user.id != int(userid):
        return await cq.answer("Isso não é para você...", show_alert=True)
    if int(fsize) > MAX_FILESIZE:
        return await cq.answer(
            await tld(cq.message.chat.id, "YOUTUBE_FILE_BIG"),
            show_alert=True,
            cache_time=60,
        )
    vid = re.sub(r"^\_(vid|aud)\.", "", data)
    url = f"https://www.youtube.com/watch?v={vid}"
    try:
        await cq.message.edit(await tld(cq.message.chat.id, "DOWNLOAD_YT"))
    except MessageNotModified:
        await cq.message.reply_text(await tld(cq.message.chat.id, "DOWNLOAD_YT"))
    with tempfile.TemporaryDirectory() as tempdir:
        path = os.path.join(tempdir, "ytdl")

    ttemp = f"⏰ {datetime.timedelta(seconds=int(temp))} | " if int(temp) else ""
    if "vid" in data:
        ydl = YoutubeDL(
            {
                "outtmpl": f"{path}/%(title)s-%(id)s.%(ext)s",
                "format": f"{vformat}+140",
                "max_filesize": MAX_FILESIZE,
                "noplaylist": True,
            }
        )
    else:
        ydl = YoutubeDL(
            {
                "outtmpl": f"{path}/%(title)s-%(id)s.%(ext)s",
                "format": "bestaudio[ext=m4a]",
                "max_filesize": MAX_FILESIZE,
                "noplaylist": True,
            }
        )
    try:
        yt = await extract_info(ydl, url, download=True)
    except BaseException as e:
        await c.send_log(e)
        await cq.message.edit("<b>Error:</b> <i>{}</i>".format(e))
        return
    try:
        await cq.message.edit(await tld(cq.message.chat.id, "UPLOADING_YT"))
    except MessageNotModified:
        await cq.message.reply_text(await tld(cq.message.chat.id, "UPLOADING_YT"))
    await c.send_chat_action(cq.message.chat.id, enums.ChatAction.UPLOAD_VIDEO)

    filename = ydl.prepare_filename(yt)
    thumb = io.BytesIO((await http.get(yt["thumbnail"])).content)
    thumb.name = "thumbnail.png"
    views = 0
    likes = 0
    if yt.get("view_count"):
        views += yt["view_count"]
    if yt.get("like_count"):
        likes += yt["like_count"]
    if "vid" in data:
        try:
            await c.send_video(
                cq.message.chat.id,
                video=filename,
                width=1920,
                height=1080,
                caption=(await tld(cq.message.chat.id, "YOUTUBE_CAPTION")).format(ttemp + yt["title"], url or "", datetime.timedelta(seconds=yt["duration"]) or 0, yt["channel"] or None, views, likes),
                duration=yt["duration"],
                thumb=thumb,
                reply_to_message_id=int(mid),
            )
            await cq.message.delete()
        except BadRequest as e:
            await c.send_log(e)
            await c.send_message(
                chat_id=cq.message.chat.id,
                text="<b>Error:</b> {errmsg}".format(errmsg=e),
                reply_to_message_id=int(mid),
            )
    else:
        if " - " in yt["title"]:
            performer, title = yt["title"].rsplit(" - ", 1)
        else:
            performer = yt.get("creator") or yt.get("uploader")
            title = yt["title"]
        try:
            await c.send_audio(
                cq.message.chat.id,
                audio=filename,
                title=title,
                performer=performer,
                caption=(await tld(cq.message.chat.id, "YOUTUBE_CAPTION")).format(ttemp + yt["title"], url or "", datetime.timedelta(seconds=yt["duration"]) or 0, yt["channel"] or None, views, likes),
                duration=yt["duration"],
                thumb=thumb,
                reply_to_message_id=int(mid),
            )
        except BadRequest as e:
            await cq.message.edit_text(
                "<b>Error:</b> <i>{errmsg}</i>".format(errmsg=e)
            )
        else:
            await cq.message.delete()

    shutil.rmtree(tempdir, ignore_errors=True)

    
@megux.on_message(filters.command(["sdl", "mdl"]), group=11)
@megux.on_message(filters.regex(SDL_REGEX_LINKS))
async def sdl(c: megux, m: Message):
    if m.matches:
        if m.chat.type == enums.ChatType.PRIVATE or await csdl(m.chat.id) == True:
            url = m.matches[0].group(0)
        else:
            return
    elif len(m.command) > 1:
        url = m.text.split(None, 1)[1]
    elif m.reply_to_message and m.reply_to_message.text:
        url = m.reply_to_message.text
    else:
        await m.reply_text(
            (await tld(m.chat.id, "NO_ARGS_YT"))
        )
        return

    if re.match(
        SDL_REGEX_LINKS,
        url,
        re.M,
    ):
        with tempfile.TemporaryDirectory() as tempdir:
            path = os.path.join(tempdir, f"sdl|{random.randint(0, 300)}")
            try:
                await gallery_down(path, url)
                files = []
                try:
                    files += [
                        InputMediaVideo(os.path.join(path, video))
                        for video in os.listdir(path)
                        if video.endswith(".mp4")
                    ]
                except FileNotFoundError:
                    pass
                if not re.match(
                    r"(http(s)?:\/\/(?:www\.)?(?:v\.)?(?:mobile.)?(?:twitter.com)\/(?:.*?))(?:\s|$)",
                    url,
                    re.M,
                ) and (
                    (
                        m.chat.type == enums.ChatType.PRIVATE
                        or await cisdl(m.chat.id) == True
                    )
                ):
                    try:
                        files += [
                            InputMediaPhoto(os.path.join(path, photo))
                            for photo in os.listdir(path)
                            if photo.endswith((".jpg", ".png", ".jpeg"))
                        ]
                    except FileNotFoundError:
                        pass
                try:
                    if files:
                        await c.send_chat_action(
                            m.chat.id, enums.ChatAction.UPLOAD_DOCUMENT
                        )
                        await m.reply_media_group(media=files)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except MediaEmpty:
                    return
                except Forbidden:
                    return shutil.rmtree(tempdir, ignore_errors=True)
            except gallery_dl.exception.GalleryDLException:
                ydl_opts = {
                    "outtmpl": f"{path}/%(extractor)s-%(id)s.%(ext)s",
                    "wait-for-video": "1",
                    "noplaylist": True,
                    "logger": MyLogger(),
                }

                if re.match(
                    r"https?://(?:vm|vt)\.tiktok\.com/(?P<id>\w+)",
                    url,
                    re.M,
                ):
                    r = await http.head(url, follow_redirects=True)
                    url = r.url

                try:
                    await extract_info(YoutubeDL(ydl_opts), str(url), download=True)
                except BaseException:
                    return
                if videos := [
                    InputMediaVideo(os.path.join(path, video))
                    for video in os.listdir(path)
                ]:
                    await c.send_chat_action(m.chat.id, enums.ChatAction.UPLOAD_VIDEO)
                    try:
                        await m.reply_media_group(media=videos)
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                    except MediaEmpty:
                        return
                    except Forbidden:
                        return shutil.rmtree(tempdir, ignore_errors=True)
        await asyncio.sleep(2)
        shutil.rmtree(tempdir, ignore_errors=True)
    else:
        return await m.reply_text("This is not a valid sdl link")

