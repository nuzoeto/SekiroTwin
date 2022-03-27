__all__ = ["get_collection"]

import asyncio

from motor.core import AgnosticClient, AgnosticCollection, AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient

from megumin import Config

print("Connecting to Database ...")

DATABASE_URL = Config.DB_URI

_MGCLIENT: AgnosticClient = AsyncIOMotorClient(DATABASE_URL)
_RUN = asyncio.get_event_loop().run_until_complete

if "megumin" in _RUN(_MGCLIENT.list_database_names()):
    print("WhiterKang Database Found :) => Now Logging to it...")
else:
    print("WhiterKang Database Not Found :( => Creating New Database...")

_DATABASE: AgnosticDatabase = _MGCLIENT["megumin"]


def get_collection(name: str) -> AgnosticCollection:
    """Create or Get Collection from your database"""
    return _DATABASE[name]


def _close_db() -> None:
    _MGCLIENT.close()
