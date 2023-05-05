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
import contextlib


from yt_dlp import YoutubeDL
from urllib.parse import unquote
from typing import Tuple, Callable
from functools import wraps, partial
from bs4 import BeautifulSoup

from pyrogram.helpers import ikb
from pyrogram import filters, enums
from pyrogram.errors import BadRequest, FloodWait, Forbidden, MediaEmpty, MessageNotModified
from pyrogram.raw.types import InputMessageID
from pyrogram.raw.functions import channels, messages
from pyrogram.types import Message, CallbackQuery, InputMediaVideo, InputMediaPhoto


from megumin import megux, Config 
from megumin.utils import humanbytes, tld, csdl, cisdl


http = httpx.AsyncClient()


YOUTUBE_REGEX = re.compile(
    r"(?m)http(?:s?):\/\/(?:www\.)?(?:music\.)?youtu(?:be\.com\/(watch\?v=|shorts/|embed/)|\.be\/|)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?"
)

SDL_REGEX_LINKS = r"http(?:s)?:\/\/(?:www.|mobile.|m.|vm.)?(?:instagram|twitter|reddit|tiktok|facebook).com\/(?:\S*)"


TWITTER_REGEX = (
    r"(http(s)?:\/\/(?:www\.)?(?:v\.)?(?:mobile.)?(?:twitter.com)\/(?:.*?))(?:\s|$)"
)


TIME_REGEX = re.compile(r"[?&]t=([0-9]+)")

MAX_FILESIZE = 2000000000


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


class DownloadMedia:
    def __init__(self):
        self.cors: str = "https://cors-bypass.amanoteam.com/"
        self.TwitterAPI: str = "https://api.twitter.com/2/"

    async def download(self, url: str, id: str):
        self.files: list = []
        if re.search(r"instagram.com/", url):
            await self.instagram(url, id)
        elif re.search(r"tiktok.com/", url):
            await self.TikTok(url, id)
        elif re.search(r"twitter.com/", url):
            await self.Twitter(url, id)
        return self.files, self.caption

    async def instagram(self, url: str, id: str):
        instalink = f"<a href='{url}'>🔗 Link</a>"
        url = re.sub(
            r"(?:www.|m.)?instagram.com/(?:reel|p)(.*)/", r"imginn.com/p\1/", url
        )
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0",
            "Accept": "application/json",
        }
        res = await http.get(f"{self.cors}{url}", headers=headers)

        if res.status_code != 200:
            url = re.sub(r"imginn.com", r"imginn.org", url)
            res = await http.get(f"{url}")

        soup = BeautifulSoup(res.text, "html.parser")
        self.caption = f"{soup.find('meta', property='og:description')['content']}\n{instalink}"  # TODO: add option to disable the captions.
        with contextlib.suppress(FileExistsError):
            os.mkdir(f"./downloads/{id}/")
        if swiper := soup.find_all("div", "swiper-slide"):
            for i in swiper:
                urlmedia = re.sub(r".*url=", r"", unquote(i["data-src"]))
                path = f"./downloads/{id}/{urlmedia[90:120]}.{'mp4' if re.search(r'.mp4', urlmedia, re.M) else 'jpg'}"
                with open(path, "wb") as f:
                    f.write((await http.get(f"{self.cors}{urlmedia}")).content)
                self.files.append({"path": path, "width": 0, "height": 0})
        else:
            media = f"{self.cors}{soup.find('a', string='Download', href=True)['href']}"
            path = f"./downloads/{id}/{media[90:120]}.{'mp4' if re.search(r'.mp4', media, re.M) else 'jpg'}"
            with open(path, "wb") as f:
                f.write((await http.get(media)).content)
            self.files.append({"path": path, "width": 0, "height": 0})
        return

    async def Twitter(self, url: str, id: str):
        # Extract the tweet ID from the URL
        tweet_id = re.match(".*twitter.com/.+status/([A-Za-z0-9]+)", url)[1]
        params: str = "?expansions=attachments.media_keys,author_id&media.fields=type,variants,url,height,width&tweet.fields=entities"

        # Send the request and parse the response as JSON
        res = await http.get(
            f"{self.TwitterAPI}tweets/{tweet_id}{params}",
            headers={"Authorization": f"Bearer {Config.BARRER_API}"},
        )
        tweet = rapidjson.loads(res.content)

        self.caption = f"<a href='{url}'>🔗 Link</a>"

        # Iterate over the media attachments in the tweet
        for media in tweet["includes"]["media"]:
            if media["type"] in ("animated_gif", "video"):
                bitrate = [
                    a["bit_rate"]
                    for a in media["variants"]
                    if a["content_type"] == "video/mp4"
                ]
                key = media["media_key"]
                for a in media["variants"]:
                    with contextlib.suppress(FileExistsError):
                        os.mkdir(f"./downloads/{id}/")
                    if a["content_type"] == "video/mp4" and a["bit_rate"] == max(
                        bitrate
                    ):
                        path = f"./downloads/{id}/{key}.mp4"
                        with open(path, "wb") as f:
                            f.write((await http.get(a["url"])).content)
            else:
                path = media["url"]
            self.files.append(
                {"path": path, "width": media["width"], "height": media["height"]}
            )

        return

    async def TikTok(self, url: str, id: int):
        self.caption = f"<a href='{url}'>🔗 Link</a>"
        x = re.match(r".*tiktok.com\/.*?(:?@[A-Za-z0-9]+\/video\/)?([A-Za-z0-9]+)", url)
        ydl = YoutubeDL({"outtmpl": f"./downloads/{id}/{x[2]}.%(ext)s"})
        yt = await extract_info(ydl, url, download=True)
        self.files.append(
            {
                "path": f"./downloads/{id}/{x[2]}.mp4",
                "width": yt["formats"][0]["width"],
                "height": yt["formats"][0]["height"],
            }
        )
        return

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

    
@megux.on_message(filters.command(["sdl", "mdl", "dl"]))
@megux.on_message(filters.regex(SDL_REGEX_LINKS))
async def sdl(c: megux, m: Message):
    if m.matches:
        if m.chat.type is enums.ChatType.PRIVATE or await csdl(m.chat.id) == True:
            url = m.matches[0].group(0)
        else:
            return
    elif len(m.command) > 1:
        url = m.text.split(None, 1)[1]
    elif m.reply_to_message and m.reply_to_message.text:
        url = m.reply_to_message.text
    else:
        return await m.reply_text((await tld(m.chat.id, "NO_ARGS_YT")))

    if not re.match(SDL_REGEX_LINKS, url, re.M):
        return await m.reply_text("This is not a valid sdl link")
    
    if re.match(TWITTER_REGEX, url, re.M) and m.chat.type is not enums.ChatType.PRIVATE:
        with contextlib.suppress(UserNotParticipant):
            # To avoid conflict with @SmudgeLordBOT
            return await m.chat.get_member(909467520)
    
    path = f"{m.chat.id}.{m.id}"
    if m.chat.type == enums.ChatType.PRIVATE:
        method = messages.GetMessages(id=[InputMessageID(id=(m.id))])
    else:
        method = channels.GetMessages(
            channel=await c.resolve_peer(m.chat.id), id=[InputMessageID(id=(m.id))]
        )
    rawM = (await c.invoke(method)).messages[0].media
    files, caption = await DownloadMedia().download(url, path)

    medias = []
    for media in files:
        if media["path"][-3:] == "mp4" and len(files) == 1:
            await c.send_chat_action(m.chat.id, enums.ChatAction.UPLOAD_VIDEO)
            await m.reply_video(
                video=media["path"],
                width=media["width"],
                height=media["height"],
                caption=caption,
            )
            return shutil.rmtree(f"./downloads/{path}/", ignore_errors=True)

        if media["path"][-3:] == "mp4":
            if medias:
                medias.append(
                    InputMediaVideo(
                        media["path"], width=media["width"], height=media["height"]
                    )
                )
            else:
                medias.append(
                    InputMediaVideo(
                        media["path"],
                        width=media["width"],
                        height=media["height"],
                        caption=caption,
                    )
                )
        elif not medias:
            medias.append(InputMediaPhoto(media["path"], caption=caption))
        else:
            medias.append(InputMediaPhoto(media["path"]))

    if medias:
        if (
            rawM
            and not re.search(r"instagram.com/", url)
            and len(medias) == 1
            and "InputMediaPhoto" in str(medias[0])
        ):
            return

        await c.send_chat_action(m.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
        await m.reply_media_group(media=medias)
    return shutil.rmtree(f"./downloads/{path}/", ignore_errors=True)
