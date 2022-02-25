import httpx
from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

weather_apikey = "8de2d8b3a93542c9a2d8b3a935a2c909"

get_coords = "https://api.weather.com/v3/location/search"
url = "https://api.weather.com/v3/aggcommon/v3-wx-observations-current"


http = httpx.AsyncClient()

headers = {
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12; M2012K11AG Build/SQ1D.211205.017)"
}


@megux.on_message(filters.command(["weather", "clima"], prefixes=["/", "!"]))
async def weather(c: megux, m: Message):
    if len(m.command) == 1:
        return await m.reply_text(
            "<b>Uso:</b> <code>/clima localização ou cidade</code> - Obtém informações sobre o clima na <i>localização ou cidade</i>."
        )

    r = await http.get(
        get_coords,
        headers=headers,
        params=dict(
            apiKey=weather_apikey,
            format="json",
            language="pt-BR",
            query=m.text.split(maxsplit=1)[1],
        ),
    )
    loc_json = r.json()
    if not loc_json.get("location"):
        await m.reply_text("Localização não encontrada.")
    else:
        pos = f"{loc_json['location']['latitude'][0]},{loc_json['location']['longitude'][0]}"
        r = await http.get(
            url,
            headers=headers,
            params=dict(
                apiKey=weather_apikey,
                format="json",
                language="pt-BR",
                geocode=pos,
                units="m",
            ),
        )
        res_json = r.json()

        obs_dict = res_json["v3-wx-observations-current"]

        res = """<b>{location}</b>:

Temperatura: <code>{temperature} °C</code>
Sensação térmica: <code>{feels_like} °C</code>
Umidade do ar: <code>{air_humidity}%</code>
Vento: <code>{wind_speed} km/h</code>

- <i>{overview}</i>""".format(
            location=loc_json["location"]["address"][0],
            temperature=obs_dict["temperature"],
            feels_like=obs_dict["temperatureFeelsLike"],
            air_humidity=obs_dict["relativeHumidity"],
            wind_speed=obs_dict["windSpeed"],
            overview=obs_dict["wxPhraseLong"],
        )

        await m.reply_text(res)
