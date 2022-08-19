from pyrogram import filters
from pyrogram.types import Message

from megumin import megux, Config
from megumin.utils import get_collection, check_rights, get_string, DISABLEABLE_CMDS 
from megumin.utils.decorators import input_str 



CMDS = [
    "ban",
    "banme",
    "clima",
    "getsticker",
    "mute",
    "muteme",
    "tmute",
    "kang",
    "kick",
    "kickme",
    "ping",
    "print",
    "ip",
    "insults",
    "tr",
    "vapor",
    "report",
    "ddd",
    "dicio",
    "cep",
    "pypi",
    "slap",
    "short",
    "simi",
    "stickerid",
    "reverse",
    "unban",
    "unmute",
]


@megux.on_message(filters.command("disable", Config.TRIGGER))
async def disble_cmd(_, m: Message):
    DISABLED = get_collection(f"DISABLED {m.chat.id}")
    chat_id = m.chat.id 
    check_admin = m.from_user.id  
    query = input_str(m)
    if m.chat.type == "private":
        return await m.reply("Esse comando é para ser usado em grupos.")
    else:
        if not query in CMDS:
            return await m.reply(await get_string(m.chat.id, "NO_DISABLE_COMMAND"))
        else:
            found = await DISABLED.find_one({'_cmd': query})
            if found:
                return await m.reply(await get_string(m.chat.id, "ALREADY_DISABLED_COMMAND"))
            else:
                if await check_rights(chat_id, check_admin, "can_change_info"):
                    dis_cmd = await DISABLED.insert_one({'_cmd': query})
                    await m.reply((await get_string(m.chat.id, "COMMAND_NOW_DISABLED")).format(query))
                else:
                    return await m.reply("Você não tem direitos administrativos suficientes para alterar dados do grupo!")
        

@megux.on_message(filters.command("enable", Config.TRIGGER))
async def enable_cmd(_, m: Message):
    DISABLED = get_collection(f"DISABLED {m.chat.id}")
    chat_id = m.chat.id
    check_admin = m.from_user.id  
    query = input_str(m)
    if m.chat.type == "private":
        return await m.reply("Esse comando é para ser usado em grupos.")
    else:
        if not query in CMDS:
            return await m.reply(await get_string(m.chat.id, "NO_ENABLE_COMMAND")) 
        else:
            found = await DISABLED.find_one({'_cmd': query})
            if found:
                if await check_rights(chat_id, check_admin, "can_change_info"):
                    dis_cmd = await DISABLED.delete_one({'_cmd': query})
                    await m.reply((await get_string(m.chat.id, "COMMAND_NOW_ENABLED")).format(query))
                else:
                    return await m.reply("Você não tem direitos administrativos suficientes para alterar dados do grupo!")
            else:
                return await m.reply(await get_string(m.chat.id, "NO_DISABLED_COMMAND"))
                

@megux.on_message(filters.command("disableable", Config.TRIGGER))
async def disableable(_, m: Message):
    text = "<b>Comandos Disponiveis para ser desativados</b>:
    for command in sorted(DISABLABLE_CMDS):
        text += f"* <code>/{command}</code>\n"
    await message.reply(text)

