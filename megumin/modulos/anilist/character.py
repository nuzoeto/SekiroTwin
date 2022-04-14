import json

from aiohttp import ClientSession
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from megumin import megux

CHARACTER_QUERY = """
query ($search: String, $asHtml: Boolean) {
  Character (search: $search) {
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
    media (page: 1, perPage: 25) {
      nodes {
        id
        idMal
        title {
          romaji
          english
          native
        }
        type
        siteUrl
        coverImage {
          extraLarge
        }
        bannerImage
        averageScore
        description (asHtml: $asHtml)
      }
    }
  }
}
"""

LS_INFO_QUERY = """
query ($id: Int) {
	Character (id: $id) {
    image {
      large
    }
    media (page: 1, perPage: 25) {
      nodes {
        title {
          romaji
          english
        }
        type
      }
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


@megux.on_message(filters.command(["char", "character"], prefixes=["/", "!"]))
async def char_search(client: megux, message: Message):
    query = " ".join(message.text.split()[1:])
    if not query:
        await message.reply("NameError: 'query' not defined")
        return
    var = {"search": query, "asHtml": True}
    result = await return_json_senpai(CHARACTER_QUERY, var)
    error = result.get("errors")
    if error:
        error_sts = error[0].get("message")
        await message.reply(f"[{error_sts}]")
        return

    data = result["data"]["Character"]

    data_ = json.dumps(data)
    open("data.txt", "w").write(data_)

    # Character Data
    id_ = data["id"]
    name = data["name"]["full"]
    native = data["name"]["native"]
    img = data["image"]["large"]
    site_url = data["siteUrl"]
    data["description"]
    featured = data["media"]["nodes"]

    sp = 0
    cntnt = ""
    for cf in featured:
        out = "\n"
        title = cf["title"]["english"] or cf["title"]["romaji"]
        out += f"<h3>{title}</h3>"
        out += f"<em>[🇯🇵] {cf['title']['native']}</em>"
        out += "\n"
        cntnt += out
        sp += 1
        out = ""
        if sp > 5:
            break
    html_cntnt = ""
    if cntnt:
        html_cntnt += "<h2>Top Featured Anime :</h2>"
        html_cntnt += cntnt
        html_cntnt += "\n\n"

    open("html.txt", "w").write(html_cntnt)

    cap_text = f"""
[🇯🇵] <i>{native}</i>
(<tt>{name}</tt>)

<b>ID:</b> {id_}
"""
    buttons_ = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Series", callback_data="char_serie"),
                InlineKeyboardButton("Descrição", callback_data="char_desc"),
            ],
            [InlineKeyboardButton("Ver no Site", url=site_url)],
        ]
    )
    await message.reply_photo(
        photo=img, caption=cap_text, parse_mode="html", reply_markup=buttons_
    )

    @megux.on_callback_query(filters.regex(pattern=r"^char_serie$"))
    async def c_serie(client: megux, cb: CallbackQuery):
        buttons = [
            [
                InlineKeyboardButton("Voltar", callback_data="char_back"),
            ]
        ]
        html_r = open("html.txt", "r").read()
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=f"<i>{html_r}</i>",
            parse_mode="html",
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    @megux.on_callback_query(filters.regex(pattern=r"^char_desc$"))
    async def c_serie(client: megux, cb: CallbackQuery):
        buttons = [
            [
                InlineKeyboardButton("Voltar", callback_data="char_back"),
            ]
        ]
        data_r = open("data.txt", "r").read()
        data_rd = json.loads(data_r)

        description_ = data_rd["description"]
        desc_ = f"<b>Sobre o Personagem:</b>\n\n<i>{description_}</i>"
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=desc_,
            parse_mode="html",
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    @megux.on_callback_query(filters.regex(pattern=r"^char_back$"))
    async def c_serie(client: megux, cb: CallbackQuery):
        data_r = open("data.txt", "r").read()
        data_rd = json.loads(data_r)

        _id_ = data_rd["id"]
        name_ = data_rd["name"]["full"]
        native_ = data_rd["name"]["native"]
        cap_text_ = f"""
[🇯🇵] <i>{native_}</i>
(<tt>{name_}</tt>)

<b>ID:</b> {_id_}
"""
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=cap_text_,
            parse_mode="html",
            reply_markup=buttons_,
        )
