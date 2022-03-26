import io
import os
import re
import httpx
import datetime
import rapidjson
import youtube_search

from pyrogram.types import Message
from pyrogram.errors import BadRequest
from pyrogram import filters
from youtubesearchpython import Search, SearchVideos

from megumin import megux

http = httpx.AsyncClient()

async def search_yt(query):
    page = (
        await http.get(
            "https://www.youtube.com/results",
            params=dict(search_query=query, pbj="1"),
            headers={
                "x-youtube-client-name": "1",
                "x-youtube-client-version": "2.20200827",
            },
        )
    ).json()
    list_videos = []
    for video in page[1]["response"]["contents"]["twoColumnSearchResultsRenderer"][
        "primaryContents"
    ]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]:
        if video.get("videoRenderer"):
            dic = {
                "title": video["videoRenderer"]["title"]["runs"][0]["text"],
                "url": "https://www.youtube.com/watch?v="
                + video["videoRenderer"]["videoId"],
            }
            list_videos.append(dic)
    return list_videos

@megux.on_message(filters.command("yt", prefixes=["/", "!"]))
async def yt_search_cmd(c: megux, m: Message):
    vids = [
        '{}: <a href="{}">{}</a>'.format(num + 1, i["url"], i["title"])
        for num, i in enumerate(await search_yt(m.text.split(None, 1)[1]))
    ]
    await m.reply_text(
        "\n".join(vids) if vids else r"¯\_(ツ)_/¯", disable_web_page_preview=True
    )
