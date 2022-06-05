import base64
import time
from datetime import datetime, timedelta

from pyrogram.enums import ChatMemberStatus 
from pyrogram.types import Message

from megumin import megux, Config 

_BOT_ID = 0


def time_formatter(seconds: float) -> str:
    """tempo"""
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + "d, ") if days else "")
        + ((str(hours) + "h, ") if hours else "")
        + ((str(minutes) + "m, ") if minutes else "")
        + ((str(seconds) + "s, ") if seconds else "")
    )
    return tmp[:-2]


async def admin_check(message: Message) -> bool:
    client = message._client
    chat_id = message.chat.id
    user_id = message.from_user.id

    check_status = await client.get_chat_member(chat_id=chat_id, user_id=user_id)
    admin_strings = [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    if check_status.status not in admin_strings:
        return False
    else:
        return True


def is_admin(chat_id: int, user_id: int, check_devs: bool = False) -> bool:
    """checa admin no chat"""
    if check_devs and is_dev(user_id):
        return True
    if chat_id not in Config.ADMINS:
        return False
    return user_id in Config.ADMINS[chat_id]


def is_dev(user_id: int) -> bool:
    """retorna se é dev ou não"""
    return user_id in Config.DEV_USERS


async def is_self(user_id: int) -> bool:
    """retorna se usuario é assistente ou não"""
    global _BOT_ID  # pylint: disable=global-statement
    if not _BOT_ID:
        _BOT_ID = (await megux.get_me()).id
    return user_id == _BOT_ID


async def check_rights(chat_id: int, user_id: int, rights: str) -> bool:
    """Verifica os privilégios do usuário"""
    user = await megux.get_chat_member(chat_id, user_id)
    if user_id in Config.DEV_USERS:
        return True
    elif user.status == ChatMemberStatus.OWNER:
        return True
    elif user.status == ChatMemberStatus.ADMINISTRATOR:
        if getattr(user.privileges, rights, None):
            return True
        return False
    return False


async def check_bot_rights(chat_id: int, rights: str) -> bool:
    """checa privilegios megux"""
    global _BOT_ID  # pylint: disable=global-statement
    if not _BOT_ID:
        _BOT_ID = (await megux.get_me()).id
    bot_ = await megux.get_chat_member(chat_id, _BOT_ID)
    if bot_.status == ChatMemberStatus.ADMINISTRATOR:
        if getattr(bot_.privileges, rights, None):
            return True
        return False
    return False


async def sed_sticker(msg: Message):
    """envia sticker"""
    sticker = (await megux.get_messages("kannagifs", 19)).sticker.file_id
    await msg.reply_sticker(sticker)


def humanbytes(size: float) -> str:
    """humanize size"""
    if not size:
        return ""
    power = 1024
    t_n = 0
    power_dict = {0: " ", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        t_n += 1
    return "{:.2f} {}B".format(size, power_dict[t_n])


def encode_to_base64_string(msg: str) -> str:
    msg_bytes = msg.encode("utf-8")
    base64_bytes = base64.b64encode(msg_bytes)
    return base64_bytes.decode("utf-8")


def decode_to_base64_string(msg: str) -> str:
    msg_bytes = msg.encode("utf-8")
    base64_bytes = base64.b64decode(msg_bytes)
    return base64_bytes.decode("utf-8")


async def extract_time(msg, time_val):
    if any(time_val.endswith(unit) for unit in ("m", "h", "d")):
        unit = time_val[-1]
        time_num = time_val[:-1]  # type: str
        if not time_num.isdigit():
            await msg.reply("`Quantidade de tempo específicada é inválida.`")
            return

        if unit == "m":
            bantime = datetime.now() + timedelta(minutes=int(time_num))
        elif unit == "h":
            bantime = datetime.now() + timedelta(hours=int(time_num))
        elif unit == "d":
            bantime = datetime.now() + timedelta(days=int(time_num))  
        else:
            await msg.reply("`Existe outra unidade de tempo que você conhece ..?`")
            return
        return bantime
    else:
        await msg.reply("`Eu preciso que você informe um tempo (m, h ou d)`")
        return
