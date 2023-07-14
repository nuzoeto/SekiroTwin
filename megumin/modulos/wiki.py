##BubbalooTeam contribute from WhiterKang


##module by DAVI

import wikipedia
import re

from pyrogram import filters
from pyrogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    Message,
)
from pyrogram.errors import BadRequest

from typing import Union

from megumin import megux, Config
from megumin.utils import tld 


@megux.on_message(filters.command("wiki", Config.TRIGGER))
@megux.on_inline_query(filters.regex(r"^wiki"))
async def wiki(c: megux, m: Union[InlineQuery, Message]):
    query = m.text if isinstance(m, Message) else m.query
    chat_id = m.chat.id if isinstance(m, Message) else m.from_user.id
    if len(query.split(maxsplit=1)) == 1:
        try:
            if isinstance(m, Message):
                return await m.reply_text("Você não especificou o que deseja buscar. Por favor especifique o que deseja buscar.")
            return await m.answer(
                [
                    InlineQueryResultArticle(
                        title="wiki <query>",
                        input_message_content=InputTextMessageContent(
                            message_text="Você não especificou o que deseja buscar. Por favor digite o que deseja pesquisar no wiki Inline",
                        ),
                    )
                ],
                cache_time=0,
            )
        except BadRequest:
            return
    kueri = re.split(pattern="wiki", string=query)
    try:
        wikipedia.set_lang(await tld(chat_id, "language"))
        keyboard = [[InlineKeyboardButton(text=await tld(chat_id, "MOREINFO_BNT"), url=wikipedia.page(kueri).url)]]
        if isinstance(m, Message):
            await m.reply((await tld(chat_id, "WIKI_RESULT")).format(wikipedia.summary(kueri, sentences=2)), reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            res = (await tld(chat_id, "WIKI_RESULT")).format(wikipedia.summary(kueri, sentences=2))
            await m.answer(
                [
                    InlineQueryResultArticle(
                        title=(wikipedia.summary(kueri, sentences=2)),
                        description=("Resultados para '{search}'").format(
                           search=kueri
                        ),
                        reply_markup=InlineKeyboardMarkup(keyboard),
                        input_message_content=InputTextMessageContent(
                            message_text=res
                        ),
                    )
                ],
                cache_time=0,
            )
    except wikipedia.PageError as e:
        if isinstance(m, Message):
            return await m.reply("error: {}".format(e))
        return await m.answer(
                [
                    InlineQueryResultArticle(
                        title="error: {}".format(e),
                        input_message_content=InputTextMessageContent(
                            message_text="error: {}".format(e),
                        ),
                    )
                ],
                cache_time=0,
            )
    except BadRequest as et:
        if isinstance(m, Message):
            return await m.reply("error: {}".format(et))
        return await m.answer(
                [
                    InlineQueryResultArticle(
                        title="error: {}".format(et),
                        input_message_content=InputTextMessageContent(
                            message_text="error: {}".format(et),
                        ),
                    )
                ],
                cache_time=0,
            )
    except wikipedia.exceptions.DesambiguationError as eet:
        if isinstance(m, Message):
            return await m.reply("⚠ Error\nHá muitas coisas! Expresse melhor para achar o resultado!\nPossíveis resultados da consulta:\n{}".format(eet))
        return await m.answer(
                [
                    InlineQueryResultArticle(
                        title="Multiplos resultados".format(e),
                        input_message_content=InputTextMessageContent(
                            message_text="⚠ Error\nHá muitas coisas! Expresse melhor para achar o resultado!\nPossíveis resultados da consulta:\n{}".format(eet),
                        ),
                    )
                ],
                cache_time=0,
            )
