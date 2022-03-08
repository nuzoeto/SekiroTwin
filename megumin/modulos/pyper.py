import html
import re
import httpx

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


from megumin import megux

def cleanhtml(raw_html):
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext


def escape_definition(definition):
    for key, value in definition.items():
        if isinstance(value, str):
            definition[key] = html.escape(cleanhtml(value))
    return definition
    
http = httpx.AsyncClient

@megux.on_message(filters.command("pypi", prefixes=["/", "!"]))
async def pypi(c: megux, m: Message):
    if len(m.command) == 1:
        return await m.reply_text("<b>Uso:</b> <code>/pypi nome_do_pacote</code> - Procura por um pacote no Python Package Index (PyPI)."
   )

    text = m.text.split(maxsplit=1)[1]
    r = await http.get(f"https://pypi.org/pypi/{text}/json", follow_redirects=True)
    if r.status_code == 200:
        json = r.json()
        pypi_info = escape_definition(json["info"])

        message = " <b>{package_name}</b> por <i>{author_name} {author_email}</i>\nPlataforma:<b>{platform}</b>\nVersão: <b>{version}</b>\nLicença: <b>{license}</b>\nResumo: <b>{summary}</b>".format(
            package_name=pypi_info["name"],
            author_name=pypi_info["author"],
            author_email=f"&lt;{pypi_info['author_email']}&gt;"
            if pypi_info["author_email"]
            else "",
            platform=pypi_info["platform"] or "Não especificado",
            version=pypi_info["version"],
            license=pypi_info["license"] or "Nenhuma",
            summary=pypi_info["summary"],
        )

        if pypi_info["home_page"] and pypi_info["home_page"] != "UNKNOWN":
            kb = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Página inicial do pacote"
                            url=pypi_info["home_page"],
                        )
                    ]
                ]
            )
        else:
            kb = None
        await m.reply_text(message, disable_web_page_preview=True, reply_markup=kb)
    else:
        await m.reply_text("Não foi possível encontrar <b>{package_name}</b> no PyPI (O código retornado foi {http_status}).".format(
                package_name=text, http_status=r.status_code
            )
        )