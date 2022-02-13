from datetime import datetime

from pyrogram import filters
from pyrogram.errors import BadRequest
from pyrogram.types import User

from megumin import megux

infotext = (
    "**Who is [{full_name}](tg://user?id={user_id})**\n"
    " 🕵️‍♂️ User ID: `{user_id}`\n"
    " 🗣 Primeiro Nome: **{first_name}**\n"
    " 🗣 Ultimo Nome: **{last_name}**\n"
    " 👤 Username: __@{username}__\n"
    " 👁 Visto por Ultimo: `{last_online}`\n"
    " 📝 Bio: {bio}"
)


def LastOnline(user: User):
    if user.is_bot:
        return ""
    elif user.status == "recently":
        return "Recentemente"
    elif user.status == "within_week":
        return "última semana"
    elif user.status == "within_month":
        return "último mês"
    elif user.status == "long_time_ago":
        return "há muito tempo :("
    elif user.status == "online":
        return "Online"
    elif user.status == "offline":
        return datetime.fromtimestamp(user.status.date).strftime(
            "%a, %d %b %Y, %H:%M:%S"
        )


def FullName(user: User):
    return user.first_name + " " + user.last_name if user.last_name else user.first_name


@megux.on_message(filters.command("whois", "info"))
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
        photos = await client.get_profile_photos(user.id)
        await message.reply_photo(
            photo=photos[0].file_id,
            caption=infotext.format(
                full_name=FullName(user),
                user_id=user.id,
                user_dc=user.dc_id,
                first_name=user.first_name,
                last_name=user.last_name if user.last_name else "None",
                username=user.username if user.username else "None",
                last_online=LastOnline(user),
                bio=bio if bio else "`Não tem.`",
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
            ),
            disable_web_page_preview=True,
        )
