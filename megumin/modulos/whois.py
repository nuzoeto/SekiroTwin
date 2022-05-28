from datetime import datetime
import httpx

from pyrogram import filters
from pyrogram.enums import UserStatus
from pyrogram.errors import BadRequest
from pyrogram.types import User, Message

from megumin import megux, Config
from megumin.utils.decorators import input_str 

http = httpx.AsyncClient()

infotext = (
    "**Who is [{full_name}](tg://user?id={user_id})**\n"
    " 🕵️‍♂️ **User ID**: `{user_id}`\n"
    " 🗣 **Primeiro Nome**: `{first_name}`\n"
    " 🗣 **Ultimo Nome**: `{last_name}`\n"
    " 🤖 **É Bot**: __{is_bot}__\n"
    " 👤 **Username**: __@{username}__\n"
    " 👁 **Visto por Ultimo**: __{last_online}__\n"
    " 📝 **Bio**: {bio}\n"
    " 🛇 **É Restrito**: `{is_scam}`\n"
    " ✅ **É Verificado**: `{is_verified}`\n"
    " 🇧🇷 **Idioma**: `{language}`"
)


def LastOnline(user: User):
    if user.is_bot:
        return "bot"
    elif user.status == UserStatus.RECENTLY:
        return "Recentemente"
    elif user.status == UserStatus.LAST_WEEK:
        return "Na última semana"
    elif user.status == UserStatus.LAST_MONTH:
        return "No último mês"
    elif user.status == UserStatus.LONG_AGO:
        return "Há muito tempo :("
    elif user.status == UserStatus.ONLINE:
        return "Online"
    elif user.status == UserStatus.OFFLINE:
        return datetime.fromtimestamp(user.status.date).strftime(
            "%a, %d %b %Y, %H:%M:%S"
        )


SW_API = Config.SW_API

def FullName(user: User):
    return user.first_name + " " + user.last_name if user.last_name else user.first_name


@megux.on_message(filters.command(["whois", "info"], prefixes=["/", "!"]))
async def whois(client, message):
    cmd = " ".join(message.text.split()[1:])
    try:
        if cmd:
            user = await client.get_users(cmd)
        elif message.reply_to_message:
            user = message.reply_to_message.from_user
        elif not message.reply_to_message and not cmd:
            user = message.from_user
    except BadRequest as e:
        return await message.reply_text(f"<b>Error!</b>\n<code>{e}</code>")
    except IndexError:
        return await message.reply_text("Isso não me parece ser um usuário!")

    bio = (await client.get_chat(chat_id=user.id)).bio
    
    if user.photo:
        async for photo in client.get_chat_photos(user.id, limit=1):
            await message.reply_photo(
                photo=photo.file_id,
                caption=infotext.format(
                    full_name=FullName(user),
                    user_id=user.id,
                    user_dc=user.dc_id,
                    first_name=user.first_name,
                    last_name=user.last_name if user.last_name else "None",
                    username=user.username if user.username else "None",
                    last_online=LastOnline(user),
                    bio=bio if bio else "`No bio set up.`",
                    is_scam=user.is_scam,
                    is_verified=user.is_verified,
                    is_bot=user.is_bot,
                    language=user.language_code,
                ),
                disable_notification=True,
           )
    else:
        await message.reply_text(
            infotext.format(
                full_name=FullName(user),
                user_id=user.id,
                user_dc=user.dc_id,
                first_name=user.first_name,
                last_name=user.last_name if user.last_name else "None",
                username=user.username if user.username else "None",
                last_online=LastOnline(user),
                bio=bio if bio else "`No bio set up.`",
                is_scam=user.is_scam,
                is_verified=user.is_verified,
                is_bot=user.is_bot,
                language=user.language_code,
            ),
            disable_web_page_preview=True,
        )


@megux.on_message(filters.command("spamwatch"))
async def spam_watch(_, m: Message):
    if not m.reply_to_message: 
        user = m.from_user
    else:
        user = m.reply_to_message.from_user
    r = await http.get(f"https://api.spamwat.ch/banlist/{int(user.id)}", headers={"Authorization": f"Bearer {SW_API}"})

    if r.status_code == 200: 
        text = ""
        ban = r.json()
        text += "\n\nEste usuário está banido no @SpamWatch!" 
        text += f"\nMotivo: <code>{ban['reason']}</code>"
        await m.reply(text)
    else:
        return await m.reply(f"{user.mention()} Está livre como um passaro!")
