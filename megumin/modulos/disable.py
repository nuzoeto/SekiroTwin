from pyrogram import filters
from pyrogram.types import Message

from megumin import megux, Config
from megumin.utils import get_collection, check_rights 
from megumin.utils.decorators import input_str 



CMDS = [
    "clima",
    "ping",
    "print",
    "ip",
    "tr",
    "vapor",
    "report",
    "ddd",
    "cep",
    "pypi",
    "slap",
    "reverse",
    "song",
    "video",
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
            return await m.reply("__Qual comando você deseja desativar?__")
        else:
            found = await DISABLED.find_one({'_cmd': query})
            if found:
                return await m.reply("__Comando já desativado!__")
            else:
                if await check_rights(chat_id, check_admin, "can_change_info"):
                    dis_cmd = await DISABLED.insert_one({'_cmd': query})
                    await m.reply(f"__Comando {query} Agora Desativado!!!__")
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
            return await m.reply("__Qual comando você deseja ativar?__")
        else:
            found = await DISABLED.find_one({'_cmd': query})
            if found:
                if await check_rights(chat_id, check_admin, "can_change_info"):
                    dis_cmd = await DISABLED.delete_one({'_cmd': query})
                    await m.reply(f"__Comando {query} Agora Ativado!!!__")
                else:
                    return await m.reply("Você não tem direitos administrativos suficientes para alterar dados do grupo!")
            else:
                return await m.reply("__Comando não desativado!__")
                

@megux.on_message(filters.command("disableable", Config.TRIGGER))
async def disableable(_, m: Message):
    chat_id = m.chat.id 
    check_admin = m.from_user.id 
    if await check_rights(chat_id, check_admin, "can_change_info"):
        DISENABLE = """
**Comandos disponíveis para ser desativados**:

- __ddd__
- __cep__
- __clima__
- __ip__
- __ping__
- __pypi__
- __print__
- __tr__
- __report__
- __reverse__
- __slap__
- __song__
- __vapor__
- __video__
"""

    await m.reply(DISENABLE)
    else:
        return await message.reply("Você precisa ser administrador.")
        
