from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from megumin import megux

HELP_TEXT = """
Olá! Me chamo <b>WhiterKang</b>. Sou um bot de gerenciamento de grupo modular com alguns extras divertidos! Dê uma olhada no seguinte para ter uma idéia de algumas das coisas em que posso ajudá-lo. 

Comandos básicos:
- /start: Comando Legal pra ver se eu estou Vivo ou Não:3
- /help: envia esta mensagem de ajuda
- /ping Ver o atraso para o bot retornar a mensagem.
- /about Veja mais sobre os desenvolvedores. 

Todos os comandos podem ser usados com os seguintes caracteres: / !
"""

ABOUT_TEXT = """
__Um Weeb Bot feito com carinho ❤️__.
"""


@megux.on_message(filters.command("about", prefixes=["/", "!"]))
async def info(client, message):
    buttons = [
        [
            InlineKeyboardButton("Criadores", url="https://t.me/whiterbotnews/16"),
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


@megux.on_message(filters.command("help", prefixes=["/", "!"]) & filters.private)
async def help(client, message):
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Admin", callback_data="help_admin"),
                InlineKeyboardButton("Anilist", callback_data="help_ani"),
                InlineKeyboardButton("Android", callback_data="help_andr"),
            ],
            [
                InlineKeyboardButton("Outros", callback_data="help_misc"),
                InlineKeyboardButton("Geral", callback_data="help_geral"),
                InlineKeyboardButton("Lastfm", callback_data="help_last"),
            ],
            [
                InlineKeyboardButton("Notas", callback_data="help_notes"),
                InlineKeyboardButton("Purges", callback_data="help_purges"),
                InlineKeyboardButton("Youtube", callback_data="help_yt"),
            ],
            [
                InlineKeyboardButton("Bans", callback_data="help_bans"),
                InlineKeyboardButton("GitHub", callback_data="help_git"),
                InlineKeyboardButton("Memes", callback_data="help_memes"),
            ],
            [
                InlineKeyboardButton("Tradutor", callback_data="help_tr"),
                InlineKeyboardButton("Stickers", callback_data="help_stickers"),
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


@megux.on_callback_query(filters.regex(pattern=r"^help_memes$"))
async def help_diversao(client: megux, cb: CallbackQuery):
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("↩ Voltar", callback_data="help_back")]]
    )
    await cb.edit_message_text(text=H_MEMES, reply_markup=button)


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
async def help_youtube(client: megux, cb: CallbackQuery):
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("↩ Voltar", callback_data="help_back")]]
    )
    await cb.edit_message_text(text=H_YOUTUBE, reply_markup=button)


@megux.on_callback_query(filters.regex(pattern=r"^help_geral$"))
async def help_gen(client: megux, cb: CallbackQuery):
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("↩ Voltar", callback_data="help_back")]]
    )
    await cb.edit_message_text(text=H_GERAL, reply_markup=button)


@megux.on_callback_query(filters.regex(pattern=r"^help_bans$"))
async def help_restricions(client: megux, cb: CallbackQuery):
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("↩ Voltar", callback_data="help_back")]]
    )
    await cb.edit_message_text(text=H_BANS, reply_markup=button)


@megux.on_callback_query(filters.regex(pattern=r"^help_git$"))
async def help_github(client: megux, cb: CallbackQuery):
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("↩ Voltar", callback_data="help_back")]]
    )
    await cb.edit_message_text(text=H_GIT, reply_markup=button)



@megux.on_callback_query(filters.regex(pattern=r"^help_notes$"))
async def help_notes_(client: megux, cb: CallbackQuery):
    await cb.answer(f"""Under development.""", show_alert=True)



@megux.on_callback_query(filters.regex(pattern=r"^help_misc$"))
async def help_github(client: megux, cb: CallbackQuery):
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("↩ Voltar", callback_data="help_back")]]
    )
    await cb.edit_message_text(text=H_MISC, reply_markup=button)



@megux.on_callback_query(filters.regex(pattern=r"^help_tr$"))
async def help_github(client: megux, cb: CallbackQuery):
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("↩ Voltar", callback_data="help_back")]]
    )
    await cb.edit_message_text(text=H_TRANSLATOR, reply_markup=button)



@megux.on_callback_query(filters.regex(pattern=r"^help_purges$"))
async def help_github(client: megux, cb: CallbackQuery):
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("↩ Voltar", callback_data="help_back")]]
    )
    await cb.edit_message_text(text=H_PURGES, reply_markup=button)


H_ANILIST = """
Aqui está a ajuda para o módulo **Anilist**:

• /anime - Use este comando para obter informações sobre um anime específico usando nome do anime ou ID do anilist
• /char ou /character - Use este comando para obter informações sobre algum personagem
• /manga - Use este comando para obter informações sobre algum mangá
• /airing - Ainda será adicionado
"""

H_ANDR = """
Aqui está a ajuda para o módulo **Android**:

• /app < nome do app > - Use para pesquisar aplicativos na Google Play Store
• /magisk - Obtenha a última versão do magisk
• /twrp < codename > - Busca o último TWRP disponível para um determinado codinome de dispositivo
• /ofox < codename > - Busca a última versão do OrangeFox disponível para um determinado dispositivo ( não disponível )
"""

H_LAST = """
Aqui está a ajuda para o módulo **LastFm**:

Antes de tudo você deve estar registrado no lastfm

• /lt ou /lastfm para mostrar oque você esta ouvindo agora
• /reg ou /setuser para definir seu usuario LastFM
• /deluser para remover seu nome de usuario do banco de dados
"""

H_ADM = """
Aqui está a ajuda para o módulo **Admin**:

Todos usuarios:
 • /admins - Lista todos administradores do chat

Apenas admin:
 • /pin - Fixa a mensagem respondida
 • /unpin - Desfixa a mensagem atualmente fixada
 • /promote < username/reply msg > - promove um usuario a administrador do chat
 • /demote < username/reply msg > - remove os privilégios de administrador do usuario
 • /title < titulo aqui >: define uma custom tag de administrador de um usuario promovido pelo WhiterKang (ainda não disponível)
 • /zombies - Procura e limpa contas excluidas no chat
"""


@megux.on_callback_query(filters.regex(pattern=r"^help_misc$"))
async def help_admin(client: megux, cb: CallbackQuery):
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("↩ Voltar", callback_data="help_back")]]
    )
    await cb.edit_message_text(text=H_MISC, reply_markup=button)



@megux.on_callback_query(filters.regex(pattern=r"^help_stickers$"))
async def help_github(client: megux, cb: CallbackQuery):
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("↩ Voltar", callback_data="help_back")]]
    )
    await cb.edit_message_text(text=H_STICKERS, reply_markup=button)


H_YOUTUBE = """
Aqui está a ajuda para o módulo **YouTube**:

• /song Baixe músicas
• /video Baixe videos
"""


H_GERAL = """
✨ Geral

• /ban  Bane a um usuário.
• /unban Desbane a um usuário.
• /kick Chute o usuário.
• /mute Silencia o usuário.
• /purge Limpa seu grupo.
• /del Deleta a mensagem que você respondeu.
• /zombies Bane contas excluídas do grupo 
• /cota : Veja a cotação do Dólar, Euro, BTC
• /cep : (cep) Busque um CEP
• /ddd : Busque um DDD
• /clima ou /weather  ( cidade ) Busque o clima para uma cidade.
• /device : Busque um aparelho pelo codename.
• /app : Busque um app da PlayStore. 
• /setuser : Defina seu username.
• /lt : Veja que musica você está scobblando.
• /deluser : Apague seu username lastfm do meu banco de dados.
• /github Retorna informações sobre um usuário ou organização do GitHub.
• /tr (código de idioma) Texto ou mensagem respondida.
• /getsticker Responda a um adesivo para eu enviar o PNG e as informações do sticker.
"""


H_BANS = """
Aqui está a ajuda para o módulo Bans:

• /ban Bane um usuário no chat.
• /banme Bane-se.
• /unban Desbane a um usuário.
• /mute Silencia um usuário no chat.
• /tmute (tempo) Silencia temporariamente um usuário no chat.
• /unmute Desmuta um usuário no chat.
• /kick Chuta um usuário do chat.
• /kickme Saia do grupo.
• /muteme Muta-se.
  
Um exemplo de silenciar alguém temporariamente:
/tmute @username 2h isso silencia o usuário por 2 horas.
"""


H_GIT = """
Aqui está a ajuda para o módulo **GitHub**:

• /github Retorna informações sobre um usuário ou organização do GitHub.
"""


H_MEMES = """
Aqui está a ajuda para o módulo **Memes**:

• /slap Dá um tapa no usuário.
• /insults Insulta alguém com um insulto aleatório de minhas strings.
• /runs Responde uma sequência aleatória de minhas strings.
• /bird ou /passaro Envia a foto de um pássaro.
• /dog Envia a foto de um cachorro.
• /cat Envia a foto de um gato.
• /fox Envia a foto de uma raposa.
• /redpanda ou /rpanda Envia a foto de um panda vermelho.
• /panda Envia a foto de um panda.
• /vapor ｖａｐｏｒｗａｖｅ.
"""

H_MISC = """
Aqui está a ajuda para o módulo **Outros**:

• /id Busca o ID de um usuário ou de um grupo.
• /info ou /whois Obtem informações sobre um usuário.
• /cota Mostra a cotação do Dólar, Euro, BTC, Peso Argentino, Ruplo Russo ETC...
• /cep (cep)  Busque um CEP.
• /ddd (ddd) Busque um DDD.
• /removebg  Remova o fundo de uma imagem.
• /clima ou /weather (cidade) Busque o clima para uma cidade.
• /paste Envia texto/documento respondido para o nekobin.com.
• /telegraph ou /tg Envie uma mídia para o telegra.ph.
• /reverse Faz uma busca reversa de imagens(usando o google) basta responder uma imagem ou sticker com /reverse.
• /short (url) Encurta o link especificado.
"""

H_PURGES = """
Aqui está a ajuda para o módulo **Purges**:

• /purge Exclui todas as mensagens desde a marcada até a última mensagem.
• /del Exclui a mensagem que você respondeu.
"""

H_TRANSLATOR = """
Aqui está a ajuda para o módulo **Tradutor**:

• /tr (código de idioma) Texto ou mensagem respondida.
"""


H_STICKERS = """
Aqui está a ajuda para o modulo Stickers:

• /stickerid: responda a um adesivo para eu lhe dizer seu ID de arquivo.
• /getsticker: responda a um adesivo para fazer o upload do arquivo PNG bruto.
• /kang: responda a um sticker para adicioná-lo ao seu pacote.
"""
