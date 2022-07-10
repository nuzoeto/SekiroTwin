from gpytranlate import Translator
from covid import Covid

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux, Config
from megumin.utils.decorators import input_str

cvid = Covid(source="worldometers")
tr = Translator()


@megux.on_message(filters.command("covid", Config.TRIGGER))
async def covid_command(c: megux, m: Message):
    country = input_str(m).lower()
    if not country:
        country = "world"
    if country in ["south korea", "korea"]:
        country = "s. korea"
    try:
        tr_ = await tr.translate(country, targetlang="en")
        c_case = cvid.get_status_by_country_name(tr_.text)
    except Exception:
        return await m.reply("An error have occured!, Are you sure the country name is correct?")
    active = c_case["active"]
    confirmed = c_case["confirmed"]
    country_ = c_case["country"]
    critical = c_case["critical"]
    deaths = c_case["deaths"]
    new_cases = c_case["new_cases"]
    new_deaths = c_case["new_deaths"]
    recovered = c_case["recovered"]
    total_tests = c_case["total_tests"]
    if total_tests == 0:
        total_tests = "N/A"
    else:
        total_tests = total_tests
    msg = f"""<b>Estaticas da Covid-19 para o {country_}:</b>\nCasos Confirmados: {confirmed}\nNovos Casos: {new_cases}\nCasos Ativos: {active}\nCasos Criticos: {critical}\nMortes: {deaths}\nRecuperados: {recovered}"""
    await m.reply(msg)
