# Reserved

import json
from datetime import datetime

import flag as cflag
import humanize
from aiohttp import ClientSession
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from megumin import megux, Config

ANIME_QUERY = """
query ($id: Int, $idMal:Int, $search: String, $type: MediaType, $asHtml: Boolean) {
  Media (id: $id, idMal: $idMal, search: $search, type: $type) {
    id
    idMal
    title {
      romaji
      english
      native
    }
    format
    status
    description (asHtml: $asHtml)
    startDate {
      year
      month
      day
    }
    season
    episodes
    duration
    countryOfOrigin
    source (version: 2)
    trailer {
      id
      site
      thumbnail
    }
    coverImage {
      extraLarge
    }
    bannerImage
    genres
    averageScore
    nextAiringEpisode {
      airingAt
      timeUntilAiring
      episode
    }
    isAdult
    characters (role: MAIN, page: 1, perPage: 10) {
      nodes {
        id
        name {
          full
          native
        }
        image {
          large
        }
        description (asHtml: $asHtml)
        siteUrl
      }
    }
    studios (isMain: true) {
      nodes {
        name
        siteUrl
      }
    }
    siteUrl
  }
}
"""


async def return_json_senpai(query, vars_):
    url_ = "https://graphql.anilist.co"
    async with ClientSession() as session:
        async with session.post(
            url_, json={"query": query, "variables": vars_}
        ) as post_con:
            json_data = await post_con.json()
    return json_data


def make_it_rw(time_stamp, as_countdown=False):
    """Converting Time Stamp to Readable Format"""
    if as_countdown:
        now = datetime.now()
        air_time = datetime.fromtimestamp(time_stamp)
        return str(humanize.naturaltime(now - air_time))
    return str(humanize.naturaldate(datetime.fromtimestamp(time_stamp)))


@megux.on_message(filters.command("anime", Config.TRIGGER))
async def anim_arch(client: megux, message: Message):
    """Search Anime Info"""
    query = " ".join(message.text.split()[1:])
    if not query:
        await message.reply("NameError: You didn't specify the anime you want to search for.")
        return
    vars_ = {"search": query, "asHtml": True, "type": "ANIME"}
    if query.isdigit():
        vars_ = {"id": int(query), "asHtml": True, "type": "ANIME"}

    result = await return_json_senpai(ANIME_QUERY, vars_)
    error = result.get("errors")
    if error:
        error_sts = error[0].get("message")
        await message.reply(f"[{error_sts}]")
        return

    data = result["data"]["Media"]

    data_ = json.dumps(data)

    # Data of all fields in returned json
    # pylint: disable=possibly-unused-variable
    idm = data.get("id")
    idmal = data.get("idMal")
    romaji = data["title"]["romaji"]
    english = data["title"]["english"]
    data["title"]["native"]
    formats = data.get("format")
    status = data.get("status")
    data.get("description")
    season = data.get("season")
    episodes = data.get("episodes")
    data.get("duration")
    country = data.get("countryOfOrigin")
    c_flag = cflag.flag(country)
    source = data.get("source")
    data.get("coverImage")["extraLarge"]
    data.get("bannerImage")
    genres = data.get("genres")
    genre = genres[0]
    if len(genres) != 1:
        genre = ", ".join(genres)
    score = data.get("averageScore")
    air_on = None
    if data["nextAiringEpisode"]:
        nextAir = data["nextAiringEpisode"]["airingAt"]
        air_on = make_it_rw(nextAir)
    data.get("startDate")
    adult = data.get("isAdult")
    trailer_link = "N/A"

    if data["trailer"] and data["trailer"]["site"] == "youtube":
        trailer_link = f"[Trailer](https://youtu.be/{data['trailer']['id']})"
    html_char = ""
    for character in data["characters"]["nodes"]:
        html_ = ""
        html_ += "\n"
        html_ += f"<b>• {character['name']['full']}</b>"
        html_ += f"<em>({character['name']['native']})</em>"
        html_char += f"{html_}\n"

    open(f"data_anime.txt", "w").write(data_)
    open(f"html_char.txt", "w").write(html_char)

    studios = ""
    for studio in data["studios"]["nodes"]:
        studios += "<a href='{}'>• {}</a> ".format(studio["siteUrl"], studio["name"])
    site_url = data.get("siteUrl")

    pic = f"https://img.anili.st/media/{idm}"
    # Telegraph Post mejik
    english or romaji

    ANIME_TEMPLATE = f"""[{c_flag}]**{romaji}**
**ID:** `{idm}` | **MAL ID:** `{idmal}`
➤ **SOURCE:** `{source}`
➤ **TYPE:** `{formats}`
➤ **GENRES:** `{genre}`
➤ **SEASON:** `{season}`
➤ **EPISODES:** `{episodes}`
➤ **STATUS:** `{status}`
➤ **NEXT AIRING:** `{air_on}`
➤ **SCORE:** `{score}%` 🌟
➤ **ADULT RATED:** `{adult}`
"""
    buttons_ = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Personagens", callback_data="anim_char"),
                InlineKeyboardButton("Descrição", callback_data="anim_desc"),
            ],
            [InlineKeyboardButton("Ver no Site", url=site_url)],
        ]
    )
    await message.reply_photo(photo=pic, caption=ANIME_TEMPLATE, reply_markup=buttons_)

    @megux.on_callback_query(filters.regex(pattern=r"^anim_char$"))
    async def c_serie(client: megux, cb: CallbackQuery):
        buttons = [
            [
                InlineKeyboardButton("Voltar", callback_data="anim_back"),
            ]
        ]
        character = open("html_char.txt", "r").read()
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.id,
            caption=character,
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    @megux.on_callback_query(filters.regex(pattern=r"^anim_desc$"))
    async def c_serie(client: megux, cb: CallbackQuery):
        buttons = [
            [
                InlineKeyboardButton("Voltar", callback_data="anim_back"),
            ]
        ]
        data_r = open(f"data_anime.txt", "r").read()
        data_rd = json.loads(data_r)

        synopsis_ = data_rd.get("description")
        desc_ = f"<b> Sinopse:</b>\n\n<i>{synopsis_}</i>"
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.id,
            caption=desc_,
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    @megux.on_callback_query(filters.regex(pattern=r"^anim_back$"))
    async def c_serie(client: megux, cb: CallbackQuery):
        data_r = open(f"data_anime.txt", "r").read()
        data_rd = json.loads(data_r)

        idm_ = data_rd.get("id")
        idmal_ = data_rd.get("idMal")
        romaji_ = data_rd["title"]["romaji"]
        data_rd["title"]["native"]
        formats_ = data_rd.get("format")
        status_ = data_rd.get("status")
        season_ = data_rd.get("season")
        episodes_ = data_rd.get("episodes")
        country_ = data_rd.get("countryOfOrigin")
        c_flag_ = cflag.flag(country_)
        source_ = data_rd.get("source")
        genres_ = data_rd.get("genres")
        genre_ = genres_[0]
        if len(genres) != 1:
            ", ".join(genres)
        adult_ = data_rd.get("isAdult")
        score_ = data_rd.get("averageScore")
        air_on_ = None
        if data_rd["nextAiringEpisode"]:
            nextAir = data_rd["nextAiringEpisode"]["airingAt"]
            air_on_ = make_it_rw(nextAir)

        ANIME_TEMPLATE_ = f"""[{c_flag_}]**{romaji_}**
**ID:** `{idm_}` | **MAL ID:** `{idmal_}`
➤ <b>SOURCE:</b> `{source_}`
➤ <b>TYPE:</b> `{formats_}
➤ <b>GENRES:</b> `{genre_}`
➤ <b>SEASON:</b> `{season_}`
➤ <b>EPISODES:</b> `{episodes_}`
➤ <b>STATUS:</b> `{status_}`
➤ <b>NEXT AIRING:</b> `{air_on_}`
➤ <b>SCORE:</b> `{score_}%` 🌟
➤ <b>ADULT RATED:</b> `{adult_}`
"""
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.id,
            caption=ANIME_TEMPLATE_,
            reply_markup=buttons_,
        )
