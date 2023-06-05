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
import esprima
import filetype


from yt_dlp import YoutubeDL
from urllib.parse import unquote
from typing import Tuple, Callable
from functools import wraps, partial
from bs4 import BeautifulSoup

from pyrogram.helpers import ikb
from pyrogram import filters, enums
from pyrogram.errors import BadRequest, FloodWait, Forbidden, MediaEmpty, MessageNotModified, UserNotParticipant
from pyrogram.raw.types import InputMessageID
from pyrogram.raw.functions import channels, messages
from pyrogram.types import Message, CallbackQuery, InputMediaVideo, InputMediaPhoto


from megumin import megux, Config 
from megumin.utils import humanbytes, tld, csdl, cisdl


http = httpx.AsyncClient()


YOUTUBE_REGEX = re.compile(
    r"(?m)http(?:s?):\/\/(?:www\.)?(?:music\.)?youtu(?:be\.com\/(watch\?v=|shorts/|embed/)|\.be\/|)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?"
)

SDL_REGEX_LINKS = r"(?:htt.+?//)?(?:.+?)?(?:instagram|twitter|tiktok|facebook).com\/(?:\S*)"


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


class LegacyDownloadMedia:
    def __init__(self):
        self.cors: str = "https://cors-bypass.amanoteam.com/"
        self.TwitterAPI: str = "https://api.twitter.com/2/"

    async def download(self, url: str, captions):
        self.files: list = []
        if re.search(r"instagram.com/", url):
            await self.instagram(url, captions)
        elif re.search(r"tiktok.com/", url):
            await self.TikTok(url, captions)
        elif re.search(r"twitter.com/", url):
            await self.Twitter(url, captions)

        if captions is False:
            self.caption = f"<a href='{url}'>🔗 Link</a>"

        return self.files, self.caption

    async def instagram(self, url: str, captions: str):
        res = await http.post("https://igram.world/api/convert", data={"url": url})
        data = res.json()

        self.caption = f"\n<a href='{url}'>🔗 Link</a>"

        if data:
            data = [data] if isinstance(data, dict) else data

            for media in data:
                url = re.sub(
                    r".*(htt.+?//)(:?ins.+?.fna.f.+?net|s.+?.com)?(.+?)(&file.*)",
                    r"\1scontent.cdninstagram.com\3",
                    unquote(media["url"][0]["url"]),
                )
                file = io.BytesIO((await http.get(url)).content)
                file.name = f"{url[60:80]}.{filetype.guess_extension(file)}"
                self.files.append({"p": file, "w": 0, "h": 0})
            return

    async def Twitter(self, url: str, captions: str):
        # Extract the tweet ID from the URL
        tweet_id = re.match(".*twitter.com/.+status/([A-Za-z0-9]+)", url)[1]
        params: str = "?expansions=attachments.media_keys,author_id&media.fields=\
type,variants,url,height,width&tweet.fields=entities"
        # Send the request and parse the response as JSON
        res = await http.get(
            f"{self.TwitterAPI}tweets/{tweet_id}{params}",
            headers={"Authorization": f"Bearer {BARRER_TOKEN}"},
        )
        tweet = rapidjson.loads(res.content)
        self.caption = f"<b>{tweet['includes']['users'][0]['name']}</b>\n{tweet['data']['text']}"

        # Iterate over the media attachments in the tweet
        for media in tweet["includes"]["media"]:
            if media["type"] in ("animated_gif", "video"):
                bitrate = [
                    a["bit_rate"] for a in media["variants"] if a["content_type"] == "video/mp4"
                ]
                media["media_key"]
                for a in media["variants"]:
                    if a["content_type"] == "video/mp4" and a["bit_rate"] == max(bitrate):
                        path = io.BytesIO((await http.get(a["url"])).content)
                        path.name = f"{media['media_key']}.{filetype.guess_extension(path)}"
            else:
                path = media["url"]
            self.files.append({"p": path, "w": media["width"], "h": media["height"]})

    async def TikTok(self, url: str, captions: str):
        path = io.BytesIO()
        with contextlib.redirect_stdout(path):
            ydl = YoutubeDL({"outtmpl": "-"})
            yt = await extract_info(ydl, url, download=True)
        path.name = yt["title"]
        self.caption = f"{yt['title']}\n\n<a href='{url}'>🔗 Link</a>"
        self.files.append(
            {
                "p": path,
                "w": yt["formats"][0]["width"],
                "h": yt["formats"][0]["height"],
            }
        )
    
class DownloadMedia:
    def __init__(self):
        self.cors: str = "https://cors-bypass.amanoteam.com/"
        self.TwitterAPI: str = "https://api.twitter.com/2/"

    async def download(self, url: str, captions: bool):
        self.files: list = []
        if re.search(r"instagram.com/", url):
            await self.instagram(url, captions)
        elif re.search(r"tiktok.com/", url):
            await self.TikTok(url, captions)
        elif re.search(r"twitter.com/", url):
            await self.Twitter(url, captions)

        if captions is False:
            self.caption = f"<a href='{url}'>🔗 Link</a>"

        return self.files, self.caption

    async def instagram(self, url: str, captions: str):
        post_id = re.findall(r"/(?:reel|p)/([a-zA-Z0-9_-]+)/", url)[0]
        r = await http.get(
            f"https://www.instagram.com/p/{post_id}/embed/captioned",
            follow_redirects=True,
        )
        soup = BeautifulSoup(r.text, "html.parser")
        medias = []

        if soup.find("div", {"data-media-type": "GraphImage"}):
            caption = re.sub(
                r'.*</a><br/><br/>(.*)(<div class="CaptionComments">.*)',
                r"\1",
                str(soup.find("div", {"class": "Caption"})),
            ).replace("<br/>", "\n")
            self.caption = f"{caption}\n<a href='{url}'>🔗 Link</a>"
            file = soup.find("img", {"class": "EmbeddedMediaImage"}).get("src")
            medias.append({"p": file, "w": 0, "h": 0})

        data = re.findall(r'<script>(requireLazy\(\["TimeSliceImpl".*)<\/script>', r.text)

        if data and "shortcode_media" in data[0]:
            tokenized = esprima.tokenize(data[0])
            for token in tokenized:
                if "shortcode_media" in token.value:
                    jsoninsta = rapidjson.loads(rapidjson.loads(token.value))["gql_data"]["shortcode_media"]

                    if caption := jsoninsta["edge_media_to_caption"]["edges"]:
                        self.caption = f"{caption[0]['node']['text']}\n<a href='{url}'>🔗 Link</a>"
                    else:
                        self.caption = f"\n<a href='{url}'>🔗 Link</a>"

                    if jsoninsta["__typename"] == "GraphVideo":
                        url = jsoninsta["video_url"]
                        dimensions = jsoninsta["dimensions"]
                        medias.append(
                            {"p": url, "w": dimensions["width"], "h": dimensions["height"]}
                        )
                    else:
                        for post in jsoninsta["edge_sidecar_to_children"]["edges"]:
                            url = post["node"]["display_url"]
                            if post["node"]["is_video"] is True:
                                url = post["node"]["video_url"]
                            dimensions = post["node"]["dimensions"]
                            medias.append(
                                {"p": url, "w": dimensions["width"], "h": dimensions["height"]}
                            )
        for m in medias:
            file = io.BytesIO((await http.get(m["p"])).content)
            file.name = f"{m['p'][60:80]}.{filetype.guess_extension(file)}"
            self.files.append({"p": file, "w": m["w"], "h": m["h"]})
        return

    async def Twitter(self, url: str, captions: str):
        # Extract the tweet ID from the URL
        tweet_id = re.match(".*twitter.com/.+status/([A-Za-z0-9]+)", url)[1]
        params: str = "?expansions=attachments.media_keys,author_id&media.fields=\
type,variants,url,height,width&tweet.fields=entities"
        # Send the request and parse the response as JSON
        res = await http.get(
            f"{self.TwitterAPI}tweets/{tweet_id}{params}",
            headers={"Authorization": f"Bearer {BARRER_TOKEN}"},
        )
        tweet = rapidjson.loads(res.content)
        self.caption = f"<b>{tweet['includes']['users'][0]['name']}</b>\n{tweet['data']['text']}"

        # Iterate over the media attachments in the tweet
        for media in tweet["includes"]["media"]:
            if media["type"] in ("animated_gif", "video"):
                bitrate = [
                    a["bit_rate"] for a in media["variants"] if a["content_type"] == "video/mp4"
                ]
                media["media_key"]
                for a in media["variants"]:
                    if a["content_type"] == "video/mp4" and a["bit_rate"] == max(bitrate):
                        path = io.BytesIO((await http.get(a["url"])).content)
                        path.name = f"{media['media_key']}.{filetype.guess_extension(path)}"
            else:
                path = media["url"]
            self.files.append({"p": path, "w": media["width"], "h": media["height"]})

    async def TikTok(self, url: str, captions: str):
        path = io.BytesIO()
        with contextlib.redirect_stdout(path):
            ydl = YoutubeDL({"outtmpl": "-"})
            yt = await extract_info(ydl, url, download=True)
        path.name = yt["title"]
        self.caption = f"{yt['title']}\n\n<a href='{url}'>🔗 Link</a>"
        self.files.append(
            {
                "p": path,
                "w": yt["formats"][0]["width"],
                "h": yt["formats"][0]["height"],
            }
        )


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
    elif not m.matches and len(m.command) > 1:
        url = m.text.split(None, 1)[1]
        if not re.match(SDL_REGEX_LINKS, url, re.M):
            return await m.reply_text("O Link não é válido.")
                
    elif m.reply_to_message and m.reply_to_message.text:
        url = m.reply_to_message.text
    else:
        return await m.reply_text(await tld(m.chat.id, "NO_ARGS_YT"))

    if m.chat.type == enums.ChatType.PRIVATE:
        method = messages.GetMessages(id=[InputMessageID(id=(m.id))])
    else:
        method = channels.GetMessages(
            channel=await c.resolve_peer(m.chat.id),
            id=[InputMessageID(id=(m.id))],
        )

    rawM = (await c.invoke(method)).messages[0].media
    files, caption = await DownloadMedia().download(url, True)

    medias = []
    for media in files:
        if filetype.is_video(media["p"]) and len(files) == 1:
            await c.send_chat_action(m.chat.id, enums.ChatAction.UPLOAD_VIDEO)
            return await m.reply_video(
                video=media["p"],
                width=media["h"],
                height=media["h"],
                caption=caption,
            )

        if filetype.is_video(media["p"]):
            if medias:
                medias.append(InputMediaVideo(media["p"], width=media["w"], height=media["h"]))
            else:
                medias.append(
                    InputMediaVideo(
                        media["p"],
                        width=media["w"],
                        height=media["h"],
                        caption=caption,
                    )
                )
        elif not medias:
            medias.append(InputMediaPhoto(media["p"], caption=caption))
        else:
            medias.append(InputMediaPhoto(media["p"]))

    if medias:
        if (
            rawM
            and not re.search(r"instagram.com/", url)
            and len(medias) == 1
            and "InputMediaPhoto" in str(medias[0])
        ):
            return

        await c.send_chat_action(m.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
        await m.reply(medias)
        return 
    return 

    
