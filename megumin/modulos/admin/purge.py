import asyncio 
from pyrogram import filters
from pyrogram.errors import MessageDeleteForbidden
from pyrogram.types import Message
from pyrogram.enums import ChatType

from megumin import megux, Config
from megumin.utils import admin_check, check_bot_rights, check_rights, get_collection, get_string  


@megux.on_message(filters.command("purge", Config.TRIGGER))
async def purge_commmand(c: megux, message: Message):
    if not await check_bot_rights(message.chat.id, "can_delete_messages"):
        return await message.reply("Não consigo excluir mensagens aqui! Verifique se eu sou um(a) administrador(a) e posso excluir mensagens de outros usuários.")
    if not await check_rights(message.chat.id, message.from_user.id, "can_delete_messages"):
        return await message.reply("Você não tem direitos suficientes para apagar mensagens")
    if not message.reply_to_message:
        return await message.reply("Responda a uma mensagem para selecionar por onde iniciar a limpeza.")
    await message.delete()
    message_ids = []
    if message.reply_to_message:
        try:
            for a_s_message_id in range(message.reply_to_message.id, message.id):
                message_ids.append(a_s_message_id)
                if len(message_ids) == 100:
                    await c.delete_messages(chat_id=message.chat.id, message_ids=message_ids)
                    count_del_etion_s += len(message_ids)
                    message_ids = []
            if len(message_ids) > 0:
                await c.delete_messages(chat_id=message.chat.id, message_ids=message_ids)
        except MessageDeleteForbidden:
            return await message.reply("Não é possível excluir todas as mensagens. As mensagens podem ser muito antigas, talvez eu não tenha direitos de exclusão ou isso pode não ser um supergrupo.")
    await message.reply("Purge completo.")


@megux.on_message(filters.command("spurge", Config.TRIGGER))
async def spurge_command(megux, message: Message):
    can_purge = await admin_check(message)
    if can_purge:
        try:
            message_reply = int(message.reply_to_message.id)
        except AttributeError:
            await message.reply(
                "Responda a uma mensagem para selecionar por onde iniciar a limpeza."
            )
            return

        while True:
            try:
                await megux.delete_messages(message.chat.id, message_reply)
                message_reply += 1
            except MessageDeleteForbidden:
                await message.reply(
                    "Não é possível excluir todas as mensagens. As mensagens podem ser muito antigas, talvez eu não tenha direitos de exclusão ou isso pode não ser um supergrupo."
                )
                return
            except Exception as exc:
                await message.reply(f"<b>ERRO:</b> {exc}")
                return
    else:
        await message.reply("Você precisa ser admin para dar purge.")
        ignore_errors=True


@megux.on_message(filters.command("cleanservice", Config.TRIGGER))
async def delservice(c: megux, m: Message):
    DATA = get_collection(f"CLEANSERVICE {m.chat.id}")
    if await check_rights(m.chat.id, m.from_user.id, "can_change_info"):
        if len(m.text.split()) > 1:
            if m.command[1] == "on":
                await DATA.drop()
                await DATA.insert_one({"status": "on"})
                await m.reply(await get_string(m.chat.id, "CLEANSERVICE_ENABLED"))
            elif m.command[1] == "off":
                await DATA.drop()
                await DATA.insert_one({"status": "off"})
                await m.reply(await get_string(m.chat.id , "CLEANSERVICE_DISABLED"))
            else:
                await m.reply(await get_string(m.chat.id, "CLEANSERVICE_ERROR"))
        else:
             if await DATA.find_one({"status": "on"}):
                 await m.reply(await get_string(m.chat.id, "CLEANSERVICE_STATUS_ON"))
             else:
                 await m.reply(await get_string(m.chat.id, "CLEANSERVICE_STATUS_ON"))
    else:
         await m.reply(await get_string(m.chat.id, "NO_CHANGEINFO_PERM"))

@megux.on_message(filters.service, group=-1)
async def delservice_action(c: megux, m: Message):
    DATA = get_collection(f"CLEANSERVICE {m.chat.id}")
    get_delservice = await DATA.find_one({"status": "on"})
    if not get_delservice:
        return

    self_member = await m.chat.get_member("me")

    if self_member.privileges and self_member.privileges.can_delete_messages:
        await m.delete()
