#Based in https://github.com/AmanoTeam/EduuRobot/blob/main/eduu/plugins/inline_search.py

import html

from pyrogram import filters
from pyrogram.errors import PeerIdInvalid, UserIdInvalid, UsernameInvalid
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from uuid import uuid4

from megumin import megux
from megumin.utils import inline_handler


@megux.on_inline_query(group=4)
async def search_inline(c: megux, q: InlineQuery):
    cmd = q.query.split(maxsplit=1)[0] if q.query else q.query

    res = inline_handler.search_cmds(cmd)
    if not res:
        return await q.answer(
            [
                InlineQueryResultArticle(
                    title="No results for {query}".format(query=command),
                    input_message_content=InputTextMessageContent(
                        "No results for {query}".format(query=command)
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
                description=result["txt_description"],
                input_message_content=InputTextMessageContent(
                    f"{html.escape(result['command'])}: {result['txt_description']}"
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="🌐 Rodar {}".format(
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
    except (PeerIdInvalid, UsernameInvalid, UserIdInvalid):
        await q.answer(
            [
                InlineQueryResultArticle(
                    title="Usuário não encontrado.",
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

inline_handler.add_cmd("info <userid>", "Get the specified user information", aliases=["info"])
