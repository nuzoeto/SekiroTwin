# reserved


from aiohttp import ClientSession
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from megumin import megux, Config

MANGA_QUERY = """
query ($search: String, $page: Int) {
  Page (perPage: 1, page: $page) {
    pageInfo {
      total
    }
    media (search: $search, type: MANGA) {
      id
      title {
        romaji
        english
        native
      }
      format
      countryOfOrigin
      source (version: 2)
      status
      description(asHtml: true)
      chapters
      isFavourite
      mediaListEntry {
        status
        score
        id
      }
      volumes
      averageScore
      siteUrl
      isAdult
    }
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


@megux.on_message(filters.command("manga", Config.TRIGGER))
async def manga_search(client: megux, message: Message):
    query = " ".join(message.text.split()[1:])
    if not query:
        await message.reply("NameError: 'query' not defined")
        return
    var = {"search": query, "asHtml": True}
    result = await return_json_senpai(MANGA_QUERY, var)
    error = result.get("errors")
    if error:
        error_sts = error[0].get("message")
        await message.reply(f"[{error_sts}]")
        return
    if len(result["data"]["Page"]["media"]) == 0:
        return [f"No results Found"]
    data = result["data"]["Page"]["media"][0]

    idm = data.get("id")
    romaji = data["title"]["romaji"]
    data["title"]["english"]
    native = data["title"]["native"]
    status = data.get("status")
    description = data.get("description")
    volumes = data.get("volumes")
    chapters = data.get("chapters")
    score = data.get("averageScore")
    site_url = data.get("siteUrl")
    format_ = data.get("format")
    data.get("countryOfOrigin")
    source = data.get("source")
    data.get("isFavourite")
    data.get("isAdult")
    name = f"""[🇯🇵]**{romaji}**
        {native}"""
    finals_ = f"{name}\n\n"
    finals_ += f"➤ **ID:** `{idm}`\n"
    finals_ += f"➤ **STATUS:** `{status}`\n"
    finals_ += f"➤ **VOLUMES:** `{volumes}`\n"
    finals_ += f"➤ **CHAPTERS:** `{chapters}`\n"
    finals_ += f"➤ **SCORE:** `{score}`\n"
    finals_ += f"➤ **FORMAT:** `{format_}`\n"
    finals_ += f"➤ **SOURCE:** `{source}`\n"
    finals_ += f"\nDescription: `{description}`\n\n"
    pic = f"https://img.anili.st/media/{idm}"
    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Ver no Site", url=site_url)]]
    )
    await client.send_photo(
        chat_id=message.chat.id, photo=pic, caption=finals_, reply_markup=buttons
    )
