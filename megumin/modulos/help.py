from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from megumin import megux

HELP_TEXT = """
Aqui estão todos os meu plugins, para saber mais sobre os plugins, **basta clicar no nome deles.**

Comandos Básicos:
Use /ping para verificar o atraso para o WhiterKang retornar a mensagem.
Use /start para iniciar o WhiterKang em um grupo ou privado
Use /help para os comandos disponíveis sobre o WhiterKang 
Use /about para saber sobre os desenvolvedores e mais
"""

ABOUT_TEXT = """
__Um Weeb Bot feito com carinho ❤️__.
"""


@megux.on_message(filters.command("about"))
async def info(client, message):
    buttons = [
        [
            InlineKeyboardButton("Criadores", url="https://t.me/megubotup/13"),
            InlineKeyboardButton("Suporte", url="https://t.me/fnixsup"),
        ]
    ]
    gif = "https://telegra.ph/file/e2621f9fa3e294c6291e5.gif"
    await megux.send_animation(
        chat_id=message.chat.id,
        animation=gif,
        caption=ABOUT_TEXT,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@megux.on_message(filters.command("help") & filters.private)
async def help(client, message):
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


@megux.on_callback_query(filters.regex(pattern=r"^help_yt$"))
async def help_andro(client: megux, cb: CallbackQuery):
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("↩ Voltar", callback_data="help_back")]]
    )
    await cb.edit_message_text(text=H_YOUTUBE, reply_markup=button)


@megux.on_callback_query(filters.regex(pattern=r"^help_geral$"))
async def help_andro(client: megux, cb: CallbackQuery):
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("↩ Voltar", callback_data="help_back")]]
    )
    await cb.edit_message_text(text=H_GERAL, reply_markup=button)


@megux.on_callback_query(filters.regex(pattern=r"^help_fun$"))
async def help_ani_(client: megux, cb: CallbackQuery):
    await cb.answer(f"""Under development.""", show_alert=True)


@megux.on_callback_query(filters.regex(pattern=r"^help_tr$"))
async def help_ani_(client: megux, cb: CallbackQuery):
    await cb.answer(f"""Under development.""", show_alert=True)


@megux.on_callback_query(filters.regex(pattern=r"^help_notes$"))
async def help_ani_(client: megux, cb: CallbackQuery):
    await cb.answer(f"""Under development.""", show_alert=True)


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
 • /title < titulo aqui >: define uma custom tag de administrador de um usuario promovido pelo WhiterKang (ainda não disponível)
 • /zombies - Procura e limpa contas excluidas no chat (ainda não disponível)
"""


H_YOUTUBE = """

• /song Baixe músicas
• /video Baixe videos
"""


H_GERAL = """
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

**Lastfm**

• /setuser : Defina seu username.

• /lt ou /lastfm : Veja que musica você está scobblando.

•/deluser ou /duser Apague seu username lastfm do meu banco de dados.

**Anilist:**

• /char ou /character Busque um Character.

• /anime Busque um anime.

• /manga Busque um mangá 

**Memes**

• /runs Execute strings aleatórias.

• /slap Bate no usuário.

• /insults O bot insulta.

• /bun finge que baniu o usuário.
"""
