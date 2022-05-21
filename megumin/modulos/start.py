
import time
import psutil
import humanize
import platform
import asyncio 

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from megumin import megux, version
from megumin import START_TIME
from megumin.utils import get_collection, time_formatter

CHAT_LOGS = -1001556292785
GROUPS = get_collection("GROUPS")
USERS = get_collection("USERS")
USERS_STARTED = get_collection("USERS_START")

START_PRIVADO = """
Olá! Meu nome é **WhiterKang** sou um bot útil e divertido para você :3

__Se você gostar das minhas funções me adicione a seu grupo!__

<b>WhiterKang's News 📬</b>: [Clique aqui](https://t.me/whiterkangnews)
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

sm = psutil.swap_memory()
uname = platform.uname() 


@megux.on_message(filters.command("start", prefixes=["/", "!"]))
async def start_(c: megux, message: Message):
    if message.chat.type == ChatType.PRIVATE:
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="❔Ajuda", callback_data="help_menu"),
                 InlineKeyboardButton(text="📦 Código Fonte", url="https://github.com/davitudoplugins1234/WhiterKang")
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
        user_id = message.from_user.id
        fname = message.from_user.first_name
        uname = message.from_user.username
        user_start = f"#NEW_USER #LOGS\n\n**User:** {fname}\n**ID:** {message.from_user.id} <a href='tg://user?id={user_id}'>**Link**</a>"
        found = await USERS_STARTED.find_one({"id_": user_id})
        if not found:
            await asyncio.gather(
                USERS_STARTED.insert_one({"id_": user_id, "user": fname}),
                c.send_log(user_start, disable_notification=False, disable_web_page_preview=True))
    else:
        return await message.reply("Oi meu nome é **WhiterKang**.")
        

    @megux.on_callback_query(filters.regex(pattern=r"^infos$"))
    async def infos(client: megux, cb: CallbackQuery):
        info_text = f"""
╔════「 Sobre  WhiterKang 」
╠ Versão : `{version.__megumin_version__}`
╠ Uptime : `{time_formatter(time.time() - START_TIME)}`
╠ System : `{client.system_version}`
╠ Cpu : `{psutil.cpu_percent(interval=1)}%`
╠ Ram : `{psutil.virtual_memory().percent}%`
╠ Disco : `{psutil.disk_usage("/").percent}%`
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
            message_id=cb.message.id,
            caption=info_text,
            reply_markup=button,
        )

    @megux.on_callback_query(filters.regex(pattern=r"^start_back$"))
    async def start_back(client: megux, cb: CallbackQuery):
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.id,
            caption=START_PRIVADO,
            reply_markup=keyboard,
        )

    @megux.on_callback_query(filters.regex(pattern=r"^help_menu$") | filters.regex("/start help_"))
    async def infos(client: megux, cb: CallbackQuery):
        info_text = f"""
Olá! Me chamo **WhiterKang**. Sou um bot de gerenciamento de grupo modular com alguns extras divertidos! Dê uma olhada no seguinte para ter uma idéia de algumas das coisas em que posso ajudá-lo. 

Comandos básicos:
- /start: Comando Legal pra ver se eu estou Vivo ou Não:3
- /help: envia esta mensagem de ajuda
- /ping Ver o atraso para o bot retornar a mensagem.
- /about Veja mais sobre os desenvolvedores. 

Todos os comandos podem ser usados com os seguintes caracteres: <code>/ !</code>
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Admin", callback_data="admin_help_button"),
                    InlineKeyboardButton("Anilist", callback_data="anilist_help_button"),
                    InlineKeyboardButton("Android", callback_data="android_help_button"),
                ],
                [
                    InlineKeyboardButton("Outros", callback_data="misc_help_button"),
                    InlineKeyboardButton("Geral", callback_data="geral_help_button"),
                    InlineKeyboardButton("LastFm", callback_data="last_help_button"),
                ],
                [
                    InlineKeyboardButton("Notas", callback_data="notes_help_button"),
                    InlineKeyboardButton("Purges", callback_data="purges_help_button"), 
                    InlineKeyboardButton("YouTube", callback_data="yt_help_button"),
                ],
                [
                    InlineKeyboardButton("Bans", callback_data="bans_help_button"),
                    InlineKeyboardButton("GitHub", callback_data="git_help_button"),
                    InlineKeyboardButton("Memes", callback_data="memes_help_button"),
                ],
                [
                    InlineKeyboardButton("Tradutor", callback_data="tr_help_button"),
                    InlineKeyboardButton("Stickers", callback_data="stickers_help_button"),
                    InlineKeyboardButton("Desativar", callback_data="disable_help_button"),
                ],
                [
                    InlineKeyboardButton("⬅ Voltar", callback_data="start_back"),
                ],
            ]
        )
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.id,
            caption=info_text,
            reply_markup=button,
        )

    @megux.on_callback_query(filters.regex(pattern=r"^start_back$"))
    async def start_back(client: megux, cb: CallbackQuery):
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.id,
            caption=START_PRIVADO,
            reply_markup=keyboard,
        )


    @megux.on_callback_query(filters.regex(pattern=r"^admin_help_button$"))
    async def infos(client: megux, cb: CallbackQuery):
        info_text = f"""
Aqui está a ajuda para o módulo <b>Admin</b>:

**Todos usuarios:**
 • /admins - Lista todos administradores do chat

**Apenas admin:**
 • /pin - Fixa a mensagem respondida
 • /unpin - Desfixa a mensagem atualmente fixada
 • /promote < username/reply msg > - promove um usuario a administrador do chat
 • /demote < username/reply msg > - remove os privilégios de administrador do usuario
 • /title < titulo aqui >: define uma custom tag de administrador de um usuario promovido pelo WhiterKang
 • /zombies - Procura e limpa contas excluidas no chat
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⬅ Voltar", callback_data="help_menu"),
                ]
            ]
        )
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.id,
            caption=info_text,
            reply_markup=button,
        )


    @megux.on_callback_query(filters.regex(pattern=r"^anilist_help_button$"))
    async def infos(client: megux, cb: CallbackQuery):
        info_text = f"""
Aqui está a ajuda para o módulo <b>Anilist</b>:

• /anime - Use este comando para obter informações sobre um anime específico usando nome do anime ou ID do anilist
• /char ou /character - Use este comando para obter informações sobre algum personagem
• /manga - Use este comando para obter informações sobre algum mangá
• /airing - Ainda será adicionado
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⬅ Voltar", callback_data="help_menu"),
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
Aqui está a ajuda para o módulo <b>Android</b>:

• /device ou /whatis < codename > Obtenha um dispositivo pelo codename.
• /app < nome do app > - Use para pesquisar aplicativos na Google Play Store.
• /magisk - Obtenha a última versão do magisk.
• /twrp < codename > - Busca o último TWRP disponível para um determinado codinome de dispositivo.
• /ofox < codename > - Busca a última versão do OrangeFox disponível para um determinado dispositivo ( não disponível )
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⬅ Voltar", callback_data="help_menu"),
                ]
            ]
        )
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=info_text,
            reply_markup=button,
        )


    @megux.on_callback_query(filters.regex(pattern=r"^last_help_button$"))
    async def infos(client: megux, cb: CallbackQuery):
        info_text = f"""
Aqui está a ajuda para o módulo <b>LastFm</b>:

Antes de tudo você deve estar registrado no lastfm

• /lt ou /lastfm para mostrar oque você esta ouvindo agora.
• /reg ou /setuser para definir seu usuario LastFM.
• /deluser ou /duser para remover seu nome de usuario do banco de dados.
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⬅ Voltar", callback_data="help_menu"),
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
                    InlineKeyboardButton("⬅ Voltar", callback_data="help_menu"),
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
Aqui está a ajuda para o módulo <b>Tradutor</b>:

• /tr (código de idioma) <b>Texto</b> ou mensagem respondida.
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⬅ Voltar", callback_data="help_menu"),
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

• /song [titulo] ou [link] Baixe músicas.
• /video [titulo] ou [link] Baixe videos.
• /yt <b>[Palavra]</b> Faz uma busca no YouTube vídeos com a palavra que você escreveu e retorna uma lista com vídeos.
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⬅ Voltar", callback_data="help_menu"),
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
• /muteme Muta-se.
  
Um exemplo de silenciar alguém temporariamente:
/tmute @username 2h isso silencia o usuário por 2 horas.
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⬅ Voltar", callback_data="help_menu"),
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
                    InlineKeyboardButton("⬅ Voltar", callback_data="help_menu"),
                ]
            ]
        )
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=info_text,
            reply_markup=button,
        )


    @megux.on_callback_query(filters.regex(pattern=r"^disable_help_button$"))
    async def infos(client: megux, cb: CallbackQuery):
        info_text = f"""
Aqui está a ajuda para o módulo **Desativar**:

Nem todo mundo quer todos os recursos que o bot oferece. Alguns comandos são melhores quando não utilizados para evitar spam e abuso.

Isso permite que você desative alguns comandos.

• /disableable Veja quais comandos podem ser desativados.

**Apenas administrador:**
• /enable <nome do cmd>: habilita um comando.
• /disable <nome do cmd>: Desativa um comando.
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⬅ Voltar", callback_data="help_menu"),
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
• /tr (código de idioma) <b>Texto<b> ou mensagem respondida.
• /getsticker Responda a um adesivo para eu enviar o PNG e as informações do sticker.
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⬅ Voltar", callback_data="help_menu"),
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
• /bird ou /passaro Envia a foto de um pássaro.
• /dog Envia a foto de um cachorro.
• /cat Envia a foto de um gato.
• /fox Envia a foto de uma raposa.
• /redpanda ou /rpanda Envia a foto de um panda vermelho.
• /panda Envia a foto de um panda.
• /vapor ｖａｐｏｒｗａｖｅ.
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⬅ Voltar", callback_data="help_menu"),
                ]
            ]
        )
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=info_text,
            reply_markup=button,
        )


    @megux.on_callback_query(filters.regex(pattern=r"^misc_help_button$"))
    async def infos(client: megux, cb: CallbackQuery):
        info_text = f"""
Aqui está a ajuda para o módulo **Outros**:

• /id Busca o ID de um usuário ou de um grupo.
• /info ou /whois Obtem informações sobre um usuário.
• /cota Mostra a cotação do Dólar, Euro, BTC, Peso Argentino, Ruplo Russo ETC...
• /cep <b>(cep)</b>  Busque um CEP.
• /ddd <b>(ddd)</b> Busque um DDD.
• /removebg <reply/msg> Remova o fundo de uma imagem.
• /clima ou /weather <b>(cidade)</b> Busque o clima para uma cidade.
• /paste Envia texto/documento respondido para o nekobin.com.
• /telegraph ou /tg Envie uma mídia para o telegra.ph.
• /reverse Faz uma busca reversa de imagens(usando o google) basta responder uma imagem ou sticker com /reverse.
• /short <b>(url)</b> Encurta o link especificado.
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⬅ Voltar", callback_data="help_menu"),
                ]
            ]
        )
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=info_text,
            reply_markup=button,
        )


    @megux.on_callback_query(filters.regex(pattern=r"^purges_help_button$"))
    async def infos(client: megux, cb: CallbackQuery):
        info_text = f"""
Aqui está a ajuda para o módulo <b>Purges</b>:

• /purge Exclui todas as mensagens desde a marcada até a última mensagem.
• /del Exclui a mensagem que você respondeu. 
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⬅ Voltar", callback_data="help_menu"),
                ]
            ]
        )
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=info_text,
            reply_markup=button,
        )


    @megux.on_callback_query(filters.regex(pattern=r"^stickers_help_button$"))
    async def infos(client: megux, cb: CallbackQuery):
        info_text = f"""
Aqui está a ajuda para o modulo <b>Stickers</b>:

• /stickerid: responda a um adesivo para eu lhe dizer seu ID de arquivo.
• /getsticker: responda a um adesivo para fazer o upload do arquivo PNG bruto.
• /kang: responda a um sticker para adicioná-lo ao seu pacote.
    """
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⬅ Voltar", callback_data="help_menu"),
                ]
            ]
        )
        await megux.edit_message_caption(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            caption=info_text,
            reply_markup=button,
        )


@megux.on_message(filters.new_chat_members)
async def thanks_for(c: megux, m: Message):
    user = (
        f"<a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a>")
    gp_title = m.chat.title
    gp_id = m.chat.id

    text_add = f"#NEW_GROUP #LOGS\n\n**Grupo**: __{gp_title}__\n**ID:** __{gp_id}__\n**User:** __{user}__"
    if m.chat.username:
        text_add += f"**\nUsername:** @{m.chat.username}"
    if c.me.id in [x.id for x in m.new_chat_members]:
        await c.send_message(chat_id=CHAT_LOGS, text=text_add)
        await c.send_message(
            chat_id=m.chat.id,
            text=("""
__Olá pessoal obrigado por me adicionar aqui!__\n**Eu sou o WhiterKang**, Prazer em conhece-los.
"""
                  ),
            disable_notification=True,
        )
        found = await GROUPS.find_one({"id_": gp_id})
        if not found:
            await asyncio.gather(
                GROUPS.insert_one({"id_": gp_id, "title": gp_title}))    


@megux.on_message(filters.left_chat_member)
async def thanks_for(c: megux, m: Message):
    gp_title = m.chat.title
    gp_id = m.chat.id
    text_left = f"#Whiter #LEFT_GROUP #LOGS\n\n**Group**: __{gp_title}__\n**ID:** __{gp_id}__"
    if m.chat.username:
        text_left += f"**\nUsername:** @{m.chat.username}"
    if c.me.id == m.left_chat_member.id:
        found = await GROUPS.find_one({"id_": gp_id})
        if found:
            await asyncio.gather(
                GROUPS.delete_one({"id_": gp_id, "title": gp_title}),
                c.send_log(
                    text_left,
                    disable_notification=False,
                    disable_web_page_preview=True,
                )
            )
        else:
            return


@megux.on_message(filters.left_chat_member)
async def thanks_owner(c: megux, m: Message):
    gp_title = m.chat.title
    gp_id = m.chat.id
    id = 1715384854
    text_left = f"#OWNER #LEFT_GROUP #LOGS\n\n**Grupo**: __{gp_title}__\n**ID:** __{gp_id}__"
    if m.chat.username:
        text_left += f"**\nUsername:** @{m.chat.username}"
    if id == m.left_chat_member.id:
        await c.send_message(
            chat_id=m.chat.id,
            text=("""
Bem, meu mestre se foi, a festa acabou!
"""
                  ),
            disable_notification=True,
        )
        await asyncio.gather(
            c.send_log(
                text_left,
                disable_notification=False,
                disable_web_page_preview=True,
            )
        )
    else:
        return
