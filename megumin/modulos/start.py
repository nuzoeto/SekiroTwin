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

HELP_TEXT = """
Oi? Precisa de ajuda sobre como me usar? Clique nos meguxões abaixo para saber mais sobre os comandos


@megux.on_message(filters.command("start"))
async def start_(_, message: Message):
    if message.chat.type == "private":
        keyboard = InlineKeyboardMarkup(
            [
                [   InlineKeyboardButton(text="❔ Ajuda", callback_data="help_menu"),
                    InlineKeyboardButton(text=" 📦 Código Fonte", url="https://github.com/davitudoplugins1234/Megumin")
                ],
                [
                    InlineKeyboardButton(text="Info", callback_data="infos"),
                    InlineKeyboardButton(text="Suporte", url="https://t.me/fnixsup"),
                ],
                [
                    InlineKeyboardButton(
                        text="✨ Me adicione a um grupo",
                        url=f"https://t.me/meguxtestbot?startgroup=new",
                    ),
                ],
            ]
        )
        gif = "https://telegra.ph/file/a003598d771e24f4abb13.gif"
        msg = START_PRIVADO
        await message.reply_animation(gif, caption=msg, reply_markup=keyboard)
    else:
        return

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

@megux.on_callback_query(filters.regex(pattern=r"^help_back$"))
    async def help_back_(client: megux, cb: CallbackQuery):
        await cb.edit_message_text(text=HELP_TEXT, reply_markup=button)
        button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Admin", callback_data="help_admin"),
                InlineKeyboardButton("Anilist", callback_data="help_ani"),
                InlineKeyboardButton("Android", callback_data="help_andr"),
            ],
            [
                InlineKeyboardButton("Fun", callback_data="help_fun"),
                InlineKeyboardButton("Geral", callback_data="help_geral"),
                InlineKeyboardButton("Lastfm", callback_data="help_last"),
            ],
            [
                InlineKeyboardButton("Notas", callback_data="help_notes"),
                InlineKeyboardButton("Tradutor", callback_data="help_tr"),
                InlineKeyboardButton("Youtube", callback_data="help_yt"),
            ],
        ]
    )
    await megux.send_message(
        chat_id=message.chat.id, text=HELP_TEXT, reply_markup=button
    )

    @megux.on_callback_query(filters.regex(pattern=r"^help_back$"))
    async def help_back_(client: megux, cb: CallbackQuery):
        await cb.edit_message_text(text=HELP_TEXT, reply_markup=button)


@megux.on_callback_query(filters.regex(pattern=r"^help_admin$"))
async def help_admin(client: megux, cb: CallbackQuery):
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("↩ Voltar", callback_data="help_back")]]
    )
    await cb.edit_message_text(text=H_ADM, reply_markup=button)


@megux.on_callback_query(filters.regex(pattern=r"^help_ani$"))
async def help_ani_(client: megux, cb: CallbackQuery):
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("↩ Voltar", callback_data="help_back")]]
    )
    await cb.edit_message_text(text=H_ANILIST, reply_markup=button)


@megux.on_callback_query(filters.regex(pattern=r"^help_andr$"))
async def help_andro(client: megux, cb: CallbackQuery):
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("↩ Voltar", callback_data="help_back")]]
    )
    await cb.edit_message_text(text=H_ANDR, reply_markup=button)


@megux.on_callback_query(filters.regex(pattern=r"^help_last$"))
async def help_lt_(client: megux, cb: CallbackQuery):
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Criar uma conta LasFM", url="https://www.last.fm/join"
                )
            ],
            [InlineKeyboardButton("↩ Voltar", callback_data="help_back")],
        ]
    )
    await cb.edit_message_text(text=H_LAST, reply_markup=button)


H_ANILIST = """
Abaixo está a lista de comandos anilist básicos para informações sobre animes, personagens, mangás, etc.
• /anime - Use este comando para obter informações sobre um anime específico usando nome do anime ou ID do anilist
• /char ou /character - Use este comando para obter informações sobre algum personagem
• /manga - Use este comando para obter informações sobre algum mangá
• /airing - Ainda será adicionado
"""

H_ANDR = """
Aqui estão alguns comandos úteis para Android.
Comandos disponíveis:
• /app < nome do app > - Use para pesquisar aplicativos na Google Play Store
• /magisk - Obtenha a última versão do magisk
• /twrp < codename > - Busca o último TWRP disponível para um determinado codinome de dispositivo
• /ofox < codename > - Busca a última versão do OrangeFox disponível para um determinado dispositivo
"""

H_LAST = """
A LastFM usa o seu histórico musical para recomendar novas músicas e eventos. Também mostra oque você esta ouvindo ou as músicas que voce ja ouviu.
Antes de tudo você deve estar registrado no lastfm
• /lt ou /lastfm para mostrar oque você esta ouvindo agora
• /reg ou /setuser para definir seu usuario LastFM
• /deluser para remover seu nome de usuario do banco de dados
"""

H_ADM = """
Aqui estão alguns comandos de admin do chat
**Todos usuarios:**
 • /admins - Lista todos administradores do chat
**Apenas admin:**
 • /pin - Fixa a mensagem respondida
 • /unpin - Desfixa a mensagem atualmente fixada
 • /promote < username/reply msg > - promove um usuario a administrador do chat
 • /demote < username/reply msg > - remove os privilégios de administrador do usuario
 • /title < titulo aqui >: define uma custom tag de administrador de um usuario promovido pelo megux (ainda não disponível)
 • /zombies - Procura e limpa contas excluidas no chat (ainda não disponível)
"""
