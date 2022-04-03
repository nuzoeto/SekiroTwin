import sys
import os
import re
import signal
import asyncio 
import traceback 
import subprocess
import io


from pyrogram import Client, filters 
from pyrogram.types import Message
from datetime import datetime 

from megumin import megux
from megumin.utils import is_dev

@megux.on_message(filters.command("restart") & filters.user(1715384854))
async def broadcast(c: megux, m: Message):
    sent = await m.reply("__Reiniciando aguarde...__") 
    args = [sys.executable, "-m", "megumin"]
    await sent.edit("**WhiterKang Reiniciado com Sucesso!**")
    os.execl(sys.executable, *args)


@megux.on_message(filters.command(r"shutdown") & filters.user(1715384854))
async def shutdown(c: megux, m: Message):
    await m.reply_text("**WhiterKang foi desligado!**")
    os.kill(os.getpid(), signal.SIGINT)


@megux.on_message(filters.command(["up", "update"]))
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


@Client.on_message(filters.command(["ev", "eval"], prefixes=["/", "!"]) & filters.user(1715384854))
async def evaluation_func(client: megux, message: Message):
    status_message = await message.reply_text("Processing ...")
    cmd = message.text.split(" ", maxsplit=1)[1]

    message.message_id
    if message.reply_to_message:
        message.reply_to_message.message_id

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        reply = message.reply_to_message or None
        await aexec(cmd, megux, message, reply)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = "<b>Expression</b>:\n<code>{}</code>\n\n<b>Result</b>:\n<code>{}</code> \n".format(
        cmd, evaluation.strip()
    )

    if len(final_output) > 4096:
        with open("eval.txt", "w", encoding="utf8") as out_file:
            out_file.write(str(final_output))

        await message.reply_document(
            "eval.txt",
            caption=cmd,
            disable_notification=True,
        )
        os.remove("eval.txt")
        await status_message.delete()
    else:
        await status_message.edit(final_output)


async def aexec(code, b, m, r):
    sys.tracebacklimit = 0
    exec(
        "async def __aexec(b, m, r): "
        + "".join(f"\n {line}" for line in code.split("\n"))
    )
    return await locals()["__aexec"](b, m, r)


@megux.on_message(filters.command("term"))
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
                parse_mode="markdown",
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
        await message.reply_text(f"**Output:**\n```{output}```", parse_mode="markdown")
    else:
        await message.reply_text("**Output:**\n`No Output`")
