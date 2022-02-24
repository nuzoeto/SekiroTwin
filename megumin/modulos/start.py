
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
Olá! Me chamo **WhiterKang**. Sou um bot de gerenciamento de grupo modular com alguns extras divertidos! Dê uma olhada no seguinte para ter uma idéia de algumas das coisas em que posso ajudá-lo. 

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
                    InlineKeyboardButton("Android", callback_data="android_help_button"),
                ],
                [
                    InlineKeyboardButton("Fun", callback_data="fun_help_button"),
                    InlineKeyboardButton("Geral", callback_data="geral_help_button"),
                    InlineKeyboardButton("LastFm", callback_data="last_help_button"),
                ],
                [
                    InlineKeyboardButton("Notas", callback_data="notes_help_button"),
                    InlineKeyboardButton("Tradutor", callback_data="tr_help_button"),
                    InlineKeyboardButton("YouTube", callback_data="yt_help_button"),
                ],
                [
                    InlineKeyboardButton("Bans", callback_data="bans_help_button"),
                    InlineKeyboardButton("GitHub", callback_data="git_help_button"),
                    InlineKeyboardButton("Memes", callback_data="memes_help_button"),
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
    async def infos(client: megux, cb: CallbackQuery):
        info_text = f"""
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
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("↩ Voltar", callback_data="help_menu"),
                ]
            ]
        )
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=info_text,
            reply_markup=button,
        )


    @megux.on_callback_query(filters.regex(pattern=r"^anilist_help_button$"))
    async def infos(client: megux, cb: CallbackQuery):
        info_text = f"""
Aqui está a ajuda para o módulo **Anilist**:

• /anime - Use este comando para obter informações sobre um anime específico usando nome do anime ou ID do anilist
• /char ou /character - Use este comando para obter informações sobre algum personagem
• /manga - Use este comando para obter informações sobre algum mangá
• /airing - Ainda será adicionado
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("↩ Voltar", callback_data="help_menu"),
                ]
            ]
        )
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=info_text,
            reply_markup=button,
        )


    @megux.on_callback_query(filters.regex(pattern=r"^android_help_button$"))
    async def infos(client: megux, cb: CallbackQuery):
        info_text = f"""
Aqui está a ajuda para o módulo **Android**:

• /app < nome do app > - Use para pesquisar aplicativos na Google Play Store
• /magisk - Obtenha a última versão do magisk
• /twrp < codename > - Busca o último TWRP disponível para um determinado codinome de dispositivo
• /ofox < codename > - Busca a última versão do OrangeFox disponível para um determinado dispositivo
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("↩ Voltar", callback_data="help_menu"),
                ]
            ]
        )
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=info_text,
            reply_markup=button,
        )


    @megux.on_callback_query(filters.regex(pattern=r"^fun_help_button$"))
    async def infos(client: megux, cb: CallbackQuery):
        await cb.answer(f"""Under development.""", show_alert=True)
    

    

    @megux.on_callback_query(filters.regex(pattern=r"^last_help_button$"))
    async def infos(client: megux, cb: CallbackQuery):
        info_text = f"""
Aqui está a ajuda para o módulo LastFm:

Antes de tudo você deve estar registrado no lastfm

• /lt ou /lastfm para mostrar oque você esta ouvindo agora.
• /reg ou /setuser para definir seu usuario LastFM.
• /deluser ou /duser para remover seu nome de usuario do banco de dados.
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("↩ Voltar", callback_data="help_menu"),
                ]
            ]
        )
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=info_text,
            reply_markup=button,
        )


    @megux.on_callback_query(filters.regex(pattern=r"^notes_help_button$"))
    async def infos(client: megux, cb: CallbackQuery):
        info_text = f"""
Under development...
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("↩ Voltar", callback_data="help_menu"),
                ]
            ]
        )
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=info_text,
            reply_markup=button,
        )


    @megux.on_callback_query(filters.regex(pattern=r"^tr_help_button$"))
    async def infos(client: megux, cb: CallbackQuery):
        info_text = f"""
Under development...
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("↩ Voltar", callback_data="help_menu"),
                ]
            ]
        )
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=info_text,
            reply_markup=button,
        )


    @megux.on_callback_query(filters.regex(pattern=r"^yt_help_button$"))
    async def infos(client: megux, cb: CallbackQuery):
        info_text = f"""
Aqui está a ajuda para o módulo **YouTube**:

• /song Baixe músicas
• /video Baixe videos
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("↩ Voltar", callback_data="help_menu"),
                ]
            ]
        )
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=info_text,
            reply_markup=button,
        )


    @megux.on_callback_query(filters.regex(pattern=r"^bans_help_button$"))
    async def infos(client: megux, cb: CallbackQuery):
        info_text = f"""
Aqui está a ajuda para o módulo **Bans**:

• /ban Bane um usuário no chat.
• /banme Bane-se.
• /unban Desbane a um usuário.
• /mute Silencia um usuário no chat.
• /tmute (tempo) Silencia temporariamente um usuário no chat.
• /unmute Desmuta um usuário no chat.
• /kick Chuta um usuário do chat.
• /kickme Saia do grupo.
  
Um exemplo de silenciar alguém temporariamente:
/tmute @username 2h isso silencia o usuário por 2 horas.
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("↩ Voltar", callback_data="help_menu"),
                ]
            ]
        )
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=info_text,
            reply_markup=button,
        )


    @megux.on_callback_query(filters.regex(pattern=r"^git_help_button$"))
    async def infos(client: megux, cb: CallbackQuery):
        info_text = f"""
Aqui está a ajuda para o módulo **GitHub**:

• /github Retorna informações sobre um usuário ou organização do GitHub.
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("↩ Voltar", callback_data="help_menu"),
                ]
            ]
        )
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=info_text,
            reply_markup=button,
        )


    @megux.on_callback_query(filters.regex(pattern=r"^geral_help_button$"))
    async def infos(client: megux, cb: CallbackQuery):
        info_text = f"""
✨ Geral

**Admin:**

• /ban  Bane a um usuário.

• /unban Desbane a um usuário.

• /kick Chute o usuário.

• /mute Silencia o usuário.

• /tmute ( tempo ) Silencia o usuário por um tempo determinado m/h/d.

• /purge Limpa seu grupo.


**Misc:**

• /cota : Veja a cotação do Dólar, Euro, BTC

• /cep : (cep) Busque um CEP

• /ddd : Busque um DDD

• /clima ou /weather  ( cidade ) Busque o clima para uma cidade.

• /kickme Saia do grupo.

**Android:**

• /device : Busque um aparelho pelo codename.

• /app : Busque um app da PlayStore. ( em breve )

**Lastfm:**

• /setuser : Defina seu username.

• /lt ou /lastfm : Veja que musica você está scobblando.

•/deluser ou /duser Apague seu username lastfm do meu banco de dados.

**Anilist:**

• /char ou /character Busque um Character.

• /anime Busque um anime.

• /manga Busque um mangá 

**Memes:**

• /runs Execute strings aleatórias.

• /slap Bate no usuário.

• /insults O bot insulta.

• /bun finge que baniu o usuário.

**GitHub:**

• /github Retorna informações sobre um usuário ou organização do GitHub.
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("↩ Voltar", callback_data="help_menu"),
                ]
            ]
        )
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=info_text,
            reply_markup=button,
        )


    @megux.on_callback_query(filters.regex(pattern=r"^memes_help_button$"))
    async def infos(client: megux, cb: CallbackQuery):
        info_text = f"""
Aqui está a ajuda para o módulo **Memes**:

• /slap Dá um tapa no usuário.
• /insults Insulta alguém com um insulto aleatório de minhas strings.
• /runs Responde uma sequência aleatória de minhas strings.
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("↩ Voltar", callback_data="help_menu"),
                ]
            ]
        )
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=info_text,
            reply_markup=button,
        )
