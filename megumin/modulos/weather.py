import httpx
from pyrogram import filters
from pyrogram.types import ( 
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Message,
)
from typing import Union


from megumin import megux, Config
from megumin.utils import get_collection, get_string, weather_apikey, http


get_coords = "https://api.weather.com/v3/location/search"
url = "https://api.weather.com/v3/aggcommon/v3-wx-observations-current"


headers = {
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; M2012K11AG Build/SQ1D.211205.017)"
}

status_emojis = {
    0: "⛈",
    1: "⛈",
    2: "⛈",
    3: "⛈",
    4: "⛈",
    5: "🌨",
    6: "🌨",
    7: "🌨",
    8: "🌨",
    9: "🌨",
    10: "🌨",
    11: "🌧",
    12: "🌧",
    13: "🌨",
    14: "🌨",
    15: "🌨",
    16: "🌨",
    17: "⛈",
    18: "🌧",
    19: "🌫",
    20: "🌫",
    21: "🌫",
    22: "🌫",
    23: "🌬",
    24: "🌬",
    25: "🌨",
    26: "☁️",
    27: "🌥",
    28: "🌥",
    29: "⛅️",
    30: "⛅️",
    31: "🌙",
    32: "☀️",
    33: "🌤",
    34: "🌤",
    35: "⛈",
    36: "🔥",
    37: "🌩",
    38: "🌩",
    39: "🌧",
    40: "🌧",
    41: "❄️",
    42: "❄️",
    43: "❄️",
    44: "n/a",
    45: "🌧",
    46: "🌨",
    47: "🌩",
}


def get_status_emoji(status_code: int) -> str:
    return status_emojis.get(status_code, "n/a")


@megux.on_message(filters.command(["weather", "clima"], prefixes=["/", "!"]))
@megux.on_inline_query(filters.regex(r"^(clima|weather)"))
async def weather(c: megux, m: Union[InlineQuery, Message]):
    text = m.text if isinstance(m, Message) else m.query
    DISABLED = get_collection(f"DISABLED {m.chat.id}")
    query = "clima"
    off = await DISABLED.find_one({"_cmd": query})
    if off:
        return
    if len(text.split(maxsplit=1)) == 1:
        if isinstance(m, Message):
            return await m.reply_text(await get_string(m.chat.id, "WEATHER_NO_ARGS"))
        return await m.answer(
            [
                InlineQueryResultArticle(
                    title="Local não especificado",
                    input_message_content=InputTextMessageContent(
                        message_text=await get_string(m.chat.id, "WEATHER_NO_ARGS"),
                    ),
                )
            ],
            cache_time=0,
        )
    r = await http.get(
        get_coords,
        headers=headers,
        params=dict(
            apiKey=weather_apikey,
            format="json",
            language=await get_string(m.chat.id, "WEATHER_LANGUAGE"),
            query=m.text.split(maxsplit=1)[1],
        ),
    )
    loc_json = r.json()
    if not loc_json.get("location"):
        if isinstance(m, Message):
            return await m.reply_text(await get_string(m.chat.id, "WEATHER_LOCATION_NOT_FOUND"))

        return await m.answer(
            [
                InlineQueryResultArticle(
                    title=await get_string(m.chat.id, "WEATHER_LOCATION_NOT_FOUND"),
                    input_message_content=InputTextMessageContent(
                        message_text=await get_string(m.chat.id, "WEATHER_LOCATION_NOT_FOUND"),
                    ),
                )
            ],
            cache_time=0,
        )
    else:
        pos = f"{loc_json['location']['latitude'][0]},{loc_json['location']['longitude'][0]}"
        r = await http.get(
            url,
            headers=headers,
            params=dict(
                apiKey=weather_apikey,
                format="json",
                language=await get_string(m.chat.id, "WEATHER_LANGUAGE"),
                geocode=pos,
                units=await get_string(m.chat.id, "WEATHER_UNIT"),
            ),
        )
        res_json = r.json()

        obs_dict = res_json["v3-wx-observations-current"]

        res = (await get_string(m.chat.id, "WEATHER_DETAILS")).format(
            location=loc_json["location"]["address"][0],
            temperature=obs_dict["temperature"],
            feels_like=obs_dict["temperatureFeelsLike"],
            air_humidity=obs_dict["relativeHumidity"],
            wind_speed=obs_dict["windSpeed"],
            overview=f"{get_status_emoji(obs_dict['iconCode'])} {obs_dict['wxPhraseLong']}",
        )

        if isinstance(m, Message):
            await m.reply_text(res)
        else:
            await m.answer(
                [
                    InlineQueryResultArticle(
                        title=loc_json["location"]["address"][0],
                        description=await get_string(m.chat.id, "WEATHER_DETAILS").format(
                            temperature=obs_dict["temperature"],
                            feels_like=obs_dict["temperatureFeelsLike"],
                            air_humidity=obs_dict["relativeHumidity"],
                            wind_speed=obs_dict["windSpeed"],
                            overview=f"{get_status_emoji(obs_dict['iconCode'])} {obs_dict['wxPhraseLong']}",
                        ),
                        input_message_content=InputTextMessageContent(
                            message_text=res,
                        ),
                    )
                ],
                cache_time=0,
            )
