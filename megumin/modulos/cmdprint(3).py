import io
import os
import re
import httpx
import datetime
import rapidjson

from pyrogram.types import Message
from pyrogram.errors import BadRequest
from pyrogram import filters

from megumin import megux


@megux.on_message(filters.command(["print", "ss"]))
async def prints(c: megux, m: Message):
    msg = m.text
    the_url = msg.split(" ", 1)
    wrong = False

    if len(the_url) == 1:
        wrong = True
    else:
        the_url = the_url[1]

    if wrong:
        await m.reply("Por Favor, especifique um link para eu printar.")
        return

    try:
        sent = await m.reply_text("Obtendo captura de tela...")
        res_json = await cssworker_url(target_url=the_url)
    except BaseException as e:
        return

    if res_json:
        # {"url":"image_url","response_time":"147ms"}
        image_url = res_json["url"]
        if image_url:
            try:
                await m.reply_photo(image_url)
                await sent.delete()
            except BaseException as e:
                user_mention = m.from_user.mention(m.from_user.first_name)
                user_id = m.from_user.id
                return
        else:
            await m.reply(
                "couldn't get url value, most probably API is not accessible."
            )
    else:
        await m.reply("Sua solicitação deu errada!")
        

async def cssworker_url(target_url: str):
    url = "https://htmlcsstoimage.com/demo_run"
    my_headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://htmlcsstoimage.com/",
        "Content-Type": "application/json",
        "Origin": "https://htmlcsstoimage.com",
        "Alt-Used": "htmlcsstoimage.com",
        "Connection": "keep-alive",
    }

    data = {
        "html": "",
        "console_mode": "",
        "url": target_url,
        "css": "",
        "selector": "",
        "ms_delay": "",
        "render_when_ready": "false",
        "viewport_height": "900",
        "viewport_width": "1600",
        "google_fonts": "",
        "device_scale": "",
    }

    try:
        resp = await http.post(url, headers=my_headers, json=data)
        return resp.json()
    except httpx.NetworkError:
        return None


async def print(query):
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
