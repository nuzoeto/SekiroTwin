
import time

from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from megumin import megux, version
from megumin import START_TIME
from megumin.utils import time_formatter

START_PRIVADO = """
Olá! Meu nome é **WhiterKang** sou um bot útil e divertido para você :3

__Se você gostar das minhas funções me adicione a seu grupo!__
"""

@megux.on_message(filters.command("start"))
async def start_(_, message: Message):
    if message.chat.type == "private":
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="❔Ajuda", callback_data="help_menu"),
                 InlineKeyboardButton(text="📦 Código Fonte", url="https://github.com/davitudoplugins1234/Megumin")
                ],
                [
                    InlineKeyboardButton(text="Info", callback_data="infos"),
                    InlineKeyboardButton(text="Suporte", url="https://t.me/fnixsup"),
                ],
                [
                    InlineKeyboardButton(
                        text="✨ Me adicione a um grupo",
                        url=f"https://t.me/whiterkangbot?startgroup=new",
                    ),
                ],
            ]
        )
        gif = "https://telegra.ph/file/576f9c3193a1dade06bce.gif"
        msg = START_PRIVADO
        await message.reply_animation(gif, caption=msg, reply_markup=keyboard)
    else:
        return await message.reply("Oi meu nome é **WhiterKang**.")
        

    @megux.on_callback_query(filters.regex(pattern=r"^infos$"))
    async def infos(client: megux, cb: CallbackQuery):
        info_text = f"""
╔════「 Sobre  WhiterKang 」
╠ Versão : `{version.__megumin_version__}`
╠ Uptime : `{time_formatter(time.time() - START_TIME)}`
╠ Python : `{version.__python_version__}`
╠ Pyrogram : `{version.__pyro_version__}`
╚═╗
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Voltar", callback_data="start_back"),
                ]
            ]
        )
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=info_text,
            reply_markup=button,
        )

    @megux.on_callback_query(filters.regex(pattern=r"^start_back$"))
    async def start_back(client: megux, cb: CallbackQuery):
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=START_PRIVADO,
            reply_markup=keyboard,
        )

    @megux.on_callback_query(filters.regex(pattern=r"^help_menu$"))
    async def infos(client: megux, cb: CallbackQuery):
        info_text = f"""
❔Ajuda   ------   ✨ Geral

**Admin:**

/ban  Bane a um usuário.

/unban Desbane a um usuário.

/kick Chute o usuário.

/mute Silencia o usuário.

/tmute ( tempo ) Silencia o usuário por um tempo determinado m/h/d.

/purge Limpa seu grupo.


**Misc:**

/cota : Veja a cotação do Dólar, Euro, BTC

/cep : (cep) Busque um CEP

/ddd : Busque um DDD

/weather ou /clima  ( cidade ) Busque o clima para uma cidade.

/banme Se bane do grupo.

/kickme Saia do grupo.


**Android:**

/device : Busque um aparelho pelo codename.

/app : Busque um app da PlayStore. ( em breve )

**Last.fm**

/setuser : Defina seu username.

/lt ou /lastfm : Veja que musica você está scobblando.

**Anilist:**

/char ou /character Busque um Character.

/anime Busque um anime.

/manga Busque um mangá 

**Memes**

/runs Execute strings aleatórias.

/slap Bate no usuário.

/insults O bot insulta.

/bun finge que baniu o usuário.
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("↩ Voltar", callback_data="start_back"),
                ],
            ]
        )
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=info_text,
            reply_markup=button,
        )

    @megux.on_callback_query(filters.regex(pattern=r"^start_back$"))
    async def start_back(client: megux, cb: CallbackQuery):
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=START_PRIVADO,
            reply_markup=keyboard,
        )
