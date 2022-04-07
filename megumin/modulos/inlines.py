from pyrogram import filters
from pyrogram.errors import PeerIdInvalid, UserIdInvalid, UsernameInvalid
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)


from megumin import megux 

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
                    "Nome de usuário: {usernameformat}\nID: {useridformat}\nDC: {userdcformat}\nLink do usuário: {usermentionformat}\nÉ bot {is_bot_user}".format(
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
