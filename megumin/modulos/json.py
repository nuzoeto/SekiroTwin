import html
import io
import json

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux 


@megux.on_message(filters.command("json", prefixes=["/", "!"]))
async def jsondump(c: megux, m: Message):
    params = m.text.split()
    # Remove the command and -f flag from list.
    params.pop(0)
    if "-f" in params:
        params.remove("-f")

    # Strip all things like _client and bound methods from Message.
    obj = json.loads(str(m))

    for param in params:
        param = int(param) if param.lstrip("-").isdecimal() else param
        try:
            obj = obj[param]
        except (IndexError, KeyError) as e:
            return await m.reply_text(f"{e.__class__.__name__}: {e}")
        # There is nothing to get anymore.
        if obj is None:
            break

    obj = json.dumps(obj, indent=4, ensure_ascii=False)

    send_as_file = len(obj) > 3000 or "-f" in params

    if send_as_file:
        bio = io.BytesIO(obj.encode())
        bio.name = f"dump-{m.chat.id}.json"
        await m.reply_document(bio)
    else:
        await m.reply_text(f"{html.escape(obj)}")
