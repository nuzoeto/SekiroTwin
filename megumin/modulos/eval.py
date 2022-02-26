import sys
import os
import re
import io
import traceback

from pyrogram import Client, filters
from pyrogram.types import Message

from megumin import megux


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
