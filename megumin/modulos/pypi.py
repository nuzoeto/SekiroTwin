import httpx
import os
import re
import shutil
import tempfile

from pyrogram import filters
from pyrogram.types import Message


from megumin import megux


@megux.on_message(filters.command("pypi", prefixes=["/", "!"]))
async def pypi(c: megux, m: Message):
    text = m.matches[0]["search"]
    r = await http.get(f"https://pypi.org/pypi/{text}/json")
    if r.status_code == 200:
        json = r.json()
        pypi_info = escape_definition(json["info"])
        message = (
            "<b>%s</b> Por <i>%s %s</i>\n"
            "Plataforma: <b>%s</b>\n"
            "Versão: <b>%s</b>\n"
            "Licença: <b>%s</b>\n"
            "Resumo: <b>%s</b>\n"
            % (
                pypi_info["name"],
                pypi_info["author"],
                f"&lt;{pypi_info['author_email']}&gt;"
                if pypi_info["author_email"]
                else "",
                pypi_info["platform"] or "Não especificado",
                pypi_info["version"],
                pypi_info["license"] or "Nenhuma",
                pypi_info["summary"],
            )
        )
        keyboard = None
        if pypi_info["home_page"] and pypi_info["home_page"] != "UNKNOWN":
            keyboard = c.ikb(
                [[("Página inicial do pacote", pypi_info["home_page"], "url")]]
            )
        await m.reply_text(
            message,
            disable_web_page_preview=True,
            reply_markup=keyboard,
        )
    else:
        await m.reply_text(
            f"Não consegui encontrar <b>{text}</b> no PyPi (<b>Error:</b> <code>{r.status_code}</code>)",
            disable_web_page_preview=True,
        )
    return
