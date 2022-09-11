#ported from https://github.com/ruizlenato/SmudgeLord/blob/rewrite/smudge/plugins/misc.py
from bs4 import BeautifulSoup
import httpx

from pyrogram import filters 
from pyrogram.types import Message 

from megumin import megux 
from megumin.utils import get_collection, disableable_dec, is_disabled


http = httpx.AsyncClient()


dicio_link = "https://www.dicionarioinformal.com.br/"


async def dicio_def(query):
    r = await http.get(dicio_link + query, follow_redirects=True)
    soup = BeautifulSoup(r.text, "html.parser")
    tit = soup.find_all("h3", "di-blue")
    if tit is None:
        tit = soup.find_all("h3", "di-blue-link")
    title = []
    for i in tit:
        a = i.find("a")
        if a != None:
            title.append(a.get("title"))
    if a is None:
        tit = soup.find_all("h3", "di-blue-link")
    for i in tit:
        a = i.find("a")
        if a != None:
            title.append(f'você quiz dizer: {a.get("title")}')
    ti = soup.find_all("p", "text-justify")
    tit = []
    for i in ti:
        ti = i.get_text()[17:].replace("""\n                """, "")
        tit.append(ti)
    des = soup.find_all("blockquote", "text-justify")
    des.append(" ")
    desc = []
    for i in des:
        try:
            des = (
                i.get_text()
                .replace("\n"[0], "")
                .replace("                 ", "")
                .replace("""\n                """, "")
            )
        except:
            if i == " ":
                des = ""
        desc.append(des)
    result = []
    max = 0
    for i in title:
        try:
            b = {
                "title": i.replace("\t", ""),
                "tit": tit[max].replace("\t", ""),
                "desc": desc[max].replace("\t", "").replace("                ", ""),
            }
            max += 1
            result.append(b)
        except:
            pass

    return result


@megux.on_message(filters.command("dicio"))
@disableable_dec("dicio")
async def dicio(c: megux, m: Message):
    if await is_disabled(m.chat.id, "dicio"):
        return
    txt = m.text.split(" ", 1)[1]
    if a := await dicio_def(txt):
        frase = f'<b>{a[0]["title"]}:</b>\n{a[0]["tit"]}\n\n<i>{a[0]["desc"]}</i>'
    else:
        frase = "Nenhum resultado encontrado!"
    await m.reply(frase)
