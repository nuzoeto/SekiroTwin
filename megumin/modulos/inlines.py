#Based in https://github.com/AmanoTeam/EduuRobot/blob/main/eduu/plugins/inline_search.py

import html

from pyrogram import filters
from pyrogram.errors import PeerIdInvalid, UserIdInvalid, UsernameInvalid, BadRequest
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from uuid import uuid4

from megumin import megux
from megumin.utils import inline_handler, GoogleImagesAPI, PixabayImagesAPI


info_thumb_url = "https://telegra.ph/file/0bf64eb57a779f7bf18c2.png"
picgo_thumb_url = "https://telegra.ph/file/ab4cc383d35bf14fa3e88.png"


@megux.on_inline_query(group=4)
async def search_inline(c: megux, q: InlineQuery):
    cmd = q.query.split(maxsplit=1)[0] if q.query else q.query

    res = inline_handler.search_cmds(cmd)
    if not res:
        return await q.answer(
            [
                InlineQueryResultArticle(
                    title="No results for {query}".format(query=cmd),
                    input_message_content=InputTextMessageContent(
                        "No results for {query}".format(query=cmd)
                    ),
                )
            ],
            cache_time=0,
        )
    articles = []
    for result in res:
        stripped_command = result["command"].split()[0]
        articles.append(
            InlineQueryResultArticle(
                id=uuid4(),
                title=result["command"],
                thumb_url=result["url_thumb"],
                description=result["txt_description"],
                input_message_content=InputTextMessageContent(
                    f"{html.escape(result['command'])}: {result['txt_description']}"
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="🌐 Run '{query}'".format(
                                    query=stripped_command
                                ),
                                switch_inline_query_current_chat=stripped_command,
                            )
                        ]
                    ]
                ),
            )
        )
    await q.answer(articles, cache_time=0)



@megux.on_inline_query(filters.regex(r"^info"))
async def info_inline(c: megux, q: InlineQuery):
    try:
        if q.query == "info":
            user = q.from_user
        elif q.query.lower().split(None, 1)[1]:
            txt = q.query.lower().split(None, 1)[1]
            user = await c.get_users(txt)
    except (PeerIdInvalid, UsernameInvalid, UserIdInvalid, BadRequest, IndexError):
        await q.answer(
            [
                InlineQueryResultArticle(
                    title="Usuário não encontrado.",
                    thumb_url=info_thumb_url,
                    input_message_content=InputTextMessageContent(
                        "Usuário não encontrado."
                    ),
                )
            ]
        )
    await q.answer(
        [
            InlineQueryResultArticle(
                title="Clique aqui para obter informações do usuário.",
                thumb_url=info_thumb_url,
                input_message_content=InputTextMessageContent(
                    "Nome de usuário: {usernameformat}\nID: {useridformat}\nDC: {userdcformat}\nLink do usuário: {usermentionformat}\nÉ bot: {is_bot_user}".format(
                        usernameformat=user.username,
                        useridformat=user.id,
                        userdcformat=user.dc_id,
                        usermentionformat=user.mention(),
                        is_bot_user=user.is_bot,
                    ),
                ),
            )
        ]
    )


@megux.on_inline_query(filters.regex(r"^picgo"))
async def picgo(c: megux, q: InlineQuery):
    gimg = GoogleImagesAPI()
    try:
        query = q.query.split(maxsplit=1)[1]
        user_id = q.from_user.id
        res = gimg.results_photo(query, user_id)
    except Exception:
        return
    await q.answer(
        results=res,
        cache_time=1,
    )

@megux.on_inline_query(filters.regex(r"^images"))
async def images(c: megux, q: InlineQuery):
    pixabay = PixabayImagesAPI()
    try:
        query = q.query.split(maxsplit=1)[1]
        user_id = q.from_user.id
        res = pixabay.pixabay_results_photo(query, 50)
        if res == []:
            return await q.answer(
                [
                    InlineQueryResultArticle(
                        title="No images for {query}".format(query=cmd),
                        input_message_content=InputTextMessageContent(
                            "No images for {query}".format(query=cmd)
                        ),
                    )
                ],
                cache_time=0,
            )
    except Exception:
        return
    await q.answer(
        results=res,
        cache_time=1,
    )

inline_handler.add_cmd("info <username>", "Get the specified user information", info_thumb_url, aliases=["info"])
inline_handler.add_cmd("picgo <query>", "Gets Images from Google (at low resolution 144p).", picgo_thumb_url, aliases=["picgo"])
