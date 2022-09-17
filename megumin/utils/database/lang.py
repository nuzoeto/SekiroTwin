import yaml
import logging
import pathlib
from megumin.utils import get_collection

CHAT_LANG = get_collection("CHAT_LANG")
STRINGS = "megumin/utils/database/string/"

language_string = {}


async def add_lang(gid: int, lang: str):
    await CHAT_LANG.update_one(
        {"chat_id": gid}, {"$set": {"lang": lang}}, upsert=True
    )


async def get_chat_lang(gid: int) -> str:
    lang = await CHAT_LANG.find_one({"chat_id": gid})
    if lang:
        return lang.get("lang")
    else:
        return "en"


async def get_string(gid: int, string) -> str:
    lang_ = await get_chat_lang(gid)
    return language_string.get(lang_).get(string)


def get_all_files():
    path = pathlib.Path(STRINGS)
    return [i.absolute() for i in path.glob("**/*")]


def load_language():
    all_files = get_all_files()
    for filepath in all_files:
        with open(filepath) as f:
            data = yaml.safe_load(f)
            language_to_load = data.get("language")
            language_string[language_to_load] = data
    logging.info("All language Loaded.")
