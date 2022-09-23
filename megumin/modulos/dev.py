import sys
import os
import re
import time
import signal
import asyncio 
import traceback 
import subprocess
import io


from pyrogram import Client, filters
from pyrogram.enums import ParseMode  
from pyrogram.errors import UserIsBlocked
from pyrogram.types import Message
from datetime import datetime 

from megumin import megux, Config
from megumin.utils import is_dev, get_collection, http
from megumin.utils.decorators import input_str



USERS = get_collection("USERS_START")
GROUPS = get_collection("GROUPS")


@megux.on_message(filters.command(["broadcast", "bc"], Config.TRIGGER))
async def broadcasting_(_, message: Message):
    user_id = message.from_user.id
    if not is_dev(user_id):
        return
    if not input_str(message):
        return await message.reply("__I need text to broadcasting.__")
    query = message.text.split(None, 1)[1]
    msg = await message.reply("__Broadcasting ...__")
    web_preview = False
    sucess_br = 0
    no_sucess = 0
    total_user = await USERS.estimated_document_count()
    ulist = USERS.find()
    if query.startswith("-d"):
        web_preview = True
        query_ = query.strip("-d")
    else:
        query_ = query
    async for users in ulist:
        try:
            await megux.send_message(chat_id= users["id_"], text=query_, disable_web_page_preview=web_preview)
            sucess_br += 1
        except UserIsBlocked:
            no_sucess += 1
        except Exception:
            no_sucess += 1
    total_groups = await GROUPS.estimated_document_count()
    sucess_br_gp = 0
    no_sucess_gp = 0
    gplist = GROUPS.find()
    async for groups in gplist:
        try:
            await megux.send_message(chat_id= groups["id_"], text=query_, disable_web_page_preview=web_preview)
            sucess_br_gp += 1
        except Exception:
            no_sucess_gp += 1
    await asyncio.sleep(3)
    await msg.edit(f"""
╭─❑ 「 **Anúncio Completo** 」 ❑──
│- __Total de Usuários:__ `{total_user}`
│- __Total de Grupos:__ `{total_groups}`
│- __Usuarios com sucesso:__ `{sucess_br}`
│- __Usuarios Falhados :__ `{no_sucess}`
│- __Grupos com sucesso:__ `{sucess_br_gp}`
│- __Grupos Falhados:__ `{no_sucess_gp}`
╰❑
    """)



@megux.on_message(filters.command("restart", prefixes=["/", "!"]) & filters.user(1715384854))
async def broadcast(c: megux, m: Message):
    sent = await m.reply("__Reiniciando aguarde...__") 
    args = [sys.executable, "-m", "megumin"]
    await sent.edit("**WhiterKang Reiniciado com Sucesso!**")
    os.execl(sys.executable, *args)


@megux.on_message(filters.command(r"shutdown", prefixes=["/", "!"]) & filters.user(1715384854))
async def shutdown(c: megux, m: Message):
    await m.reply_text("**WhiterKang foi desligado!**")
    os.kill(os.getpid(), signal.SIGINT)


@megux.on_message(filters.command(["up", "update"], prefixes=["/", "!"]))
async def restart_(_, message: Message):
    user_id = message.from_user.id
    if not is_dev(user_id):
        return
    process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    kek = await message.reply(f"`{output}`")
    await asyncio.sleep(3)
    await kek.edit("`Reiniciando...`")
    await asyncio.sleep(2)
    await kek.edit("**WhiterKang foi Reiniciado com Sucesso!**")
    os.execv(sys.executable, [sys.executable, "-m", "megumin"])


@Client.on_message(filters.command(["ev", "eval"], prefixes=["/", "!"]))
async def eval_(client: megux, message: Message):
    user_id = message.from_user.id
    if not is_dev(user_id):
        return
    status_message = await message.reply_text("__Processing ...__")
    cmd = message.text[len(message.text.split()[0]) + 1:]
    reply_to_ = message
    if message.reply_to_message:
        reply_to_ = message.reply_to_message
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = "<b>Expression</b>: "
    final_output += f"<code>{cmd}</code>\n\n"
    final_output += "<b>Result</b>:\n"
    final_output += f"<code>{evaluation.strip()}</code> \n"
    if len(final_output) > 4096:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.txt"
            await reply_to_.reply_document(
                document=out_file, caption=cmd[:1000], disable_notification=True
            )
    else:
        await reply_to_.reply_text(final_output)
    await status_message.delete()


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@megux.on_message(filters.command(["term", "sh"], prefixes=["/", "!"]))
async def terminal(client: megux, message: Message):
    user_id = message.from_user.id
    if not is_dev(user_id):
        return
    if len(message.text.split()) == 1:
        await message.reply_text("Usage: `/term echo owo`")
        return
    args = message.text.split(None, 1)
    teks = args[1]
    if "\n" in teks:
        code = teks.split("\n")
        output = ""
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
            except Exception as err:
                print(err)
                await message.reply_text(
                    """
**Error:**
```{}```
""".format(
                        err
                    ),
                    parse_mode="markdown",
                )
            output += "**{}**\n".format(code)
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", teks)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type, value=exc_obj, tb=exc_tb
            )
            await message.reply_text(
                """**Error:**\n```{}```""".format("".join(errors)),
                parse_mode=ParseMode.MARKDOWN,
            )
            return
        output = process.stdout.read()[:-1].decode("utf-8")
    if str(output) == "\n":
        output = None
    if output:
        if len(output) > 4096:
            filename = "output.txt"
            with open(filename, "w+") as file:
                file.write(output)
            await client.send_document(
                message.chat.id,
                filename,
                reply_to_message_id=message.message_id,
                caption="`Output file`",
            )
            os.remove(filename)
            return
        await message.reply_text(f"**Output:**\n```{output}```", parse_mode=ParseMode.MARKDOWN)
    else:
        await message.reply_text("**Output:**\n`No Output`")
    return await locals()["__aexec"](client, message)


@megux.on_message(filters.command("logs", Config.TRIGGER))
async def logs_bot(c: megux, m: Message):
    await m.reply("<i>Verificando o logs...</i>")
    
    logs = await http.get(f"{Config.heroku_app.get_log(lines=1200)}")["url"]
    await c.send_document(chat_id=m.chat.id, document=logs)
    await m.delete()
