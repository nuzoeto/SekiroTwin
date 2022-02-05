# lastfm module by @fnix

import urllib.parse
import urllib.request

import httpx
import rapidjson as json
from pyrogram import filters
from pyrogram.types import Message

from megumin import megux, Config
from megumin.utils import get_collection

BASE_LAST = "http://ws.audioscrobbler.com/2.0"
LAST_KEY = Config.LASTFM_API_KEY
USERS = get_collection("USERS")


async def _init():
    global LAST_USERS  # pylint: disable=global-statement
    lastdb = await USERS.find_one({"_id": "LAST_USERS"})
    if lastdb:
        LAST_USERS = lastdb["last_data"]


timeout = httpx.Timeout(20)
http = httpx.AsyncClient(http2=True, timeout=timeout)


@megux.on_message(filters.command(["lt", "lastfm"]))
async def last_(_, message: Message):
    user_ = message.from_user.id
    lastdb = await USERS.find_one({"_id": user_})
    if lastdb is None:
        await message.reply("__Você ainda não esta registrado, use /setuser (username).__")
        return
    user_lastfm = lastdb["last_data"]
    resp = await http.get(
        f"{BASE_LAST}?method=user.getrecenttracks&limit=3&extended=1&user={user_lastfm}&api_key={LAST_KEY}&format=json"
    )
    if not resp.status_code == 200:
        await message.reply("__Algo deu errado__")
        return
    try:
        first_track = resp.json().get("recenttracks").get("track")[0]
    except IndexError:
        await message.reply("Você não me parece ter scrobblado(escutado) nenhuma música.")
        return
    image = first_track.get("image")[3].get("#text")
    artist = first_track.get("artist").get("name")
    artist_ = urllib.parse.quote(artist)
    song = first_track.get("name")
    song_ = urllib.parse.quote(song)
    loved = int(first_track.get("loved"))
    fetch = await http.get(
        f"{BASE_LAST}?method=track.getinfo&artist={artist_}&track={song_}&user={user_lastfm}&api_key={LAST_KEY}&format=json"
    )
    info = json.loads(fetch.content)
    last_user = info["track"]
    get_scrob = int(last_user["userplaycount"]) + 1
    rep = f"**{user_lastfm} esta ouvindo:**\n\n"
    if not loved:
        rep += f"__🧑‍🎤 {artist}\n🎶 {song}__"
    else:
        rep += f"__🧑‍🎤 {artist}\n🎶 {song} ❤️__"
    if get_scrob:
        rep += f"\n\n__📊 {get_scrob} scrobbles__"
    if image:
        rep += f"<a href='{image}'>\u200c</a>"
    await message.reply(rep)


@megux.on_message(filters.command(["setuser", "reg"]))
async def last_save_user(_, message: Message):
    user_ = message.from_user.id
    text = " ".join(message.text.split()[1:])
    if not text:
        await message.reply("__Você não me informou seu username 🙃.__")
        return
    await USERS.update_one({"_id": user_}, {"$set": {"last_data": text}}, upsert=True)
    await message.reply("__Seu username foi definido com sucesso.__")


@megux.on_message(filters.command(["deluser"]))
async def last_save_user(_, message: Message):
    user_ = message.from_user.id
    await USERS.delete_one({"_id": user_})
    await message.reply("__Seu username foi removido do banco de dados.__")
