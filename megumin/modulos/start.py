
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

HELP_ADMIN = """
Aqui está a ajuda para o módulo **Admin**:

**Todos usuarios:**
 • /admins - Lista todos administradores do chat

**Apenas admin:**
 • /pin - Fixa a mensagem respondida
 • /unpin - Desfixa a mensagem atualmente fixada
 • /promote < username/reply msg > - promove um usuario a administrador do chat
 • /demote < username/reply msg > - remove os privilégios de administrador do usuario
 • /title < titulo aqui >: define uma custom tag de administrador de um usuario promovido pelo WhiterKang (ainda não disponível)
 • /zombies - Procura e limpa contas excluidas no chat (ainda não disponível)
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
Olá! Me chamo WhiterKang. Sou um bot de gerenciamento de grupo modular com alguns extras divertidos! Dê uma olhada no seguinte para ter uma idéia de algumas das coisas em que posso ajudá-lo. 

Comandos básicos:
- /start: Comando Legal pra ver se eu estou Vivo ou Não:3
- /help: envia esta mensagem de ajuda
- /ping Ver o atraso para o bot retornar a mensagem.
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Admin", callback_data="admin_help_button"),
                    InlineKeyboardButton("Anilist", callback_data="anilist_help_button"),
                ],
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


    @megux.on_callback_query(filters.regex(pattern=r"^admin_help_button$"))
    async def start_back(client: megux, cb: CallbackQuery):
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=HELP_ADMIN,
            reply_markup=keyboard,
        )
