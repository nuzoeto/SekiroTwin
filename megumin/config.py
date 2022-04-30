# Copyright (C) 2022 by fnixdev
#

__all__ = ["Config"]

import os
from dotenv import load_dotenv

if os.path.isfile("config.env"):
    load_dotenv("config.env")

class Config:
    AUTH_CHATS = set(
        [-1001569084822, -1001252486871, -1001412694056, -1001475334171, 1715384854, -1001517679518]
    )  # chat permitidos
    if os.environ.get("AUTH_CHATS"):
        AUTH_CHATS.update(map(int, os.environ.get("AUTH_CHATS").split()))
    DEV_USERS = (  # lista de devs
        838926101,  # @fnixdev
        2138770172,  # @Luska1331
        1157759484,  # @yusukesy
        1715384854,  # @DaviTudo 
        5204291028, #TiltLesm
    )
    LOG_CHANNEL_ID = set([-1001569084822])
    ADMINS = {}
    LASTFM_API_KEY = os.environ.get("LASTFM_API_KEY")
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    REMOVE_BG_API_KEY = os.environ.get("REMOVE_BG_API_KEY")  
    DB_URI = os.environ.get("DATABASE_URL")
    TRIGGER = os.environ.get("TRIGGER", "/ !".split())
    WHITELIST_CHATS = set([])  # chat id aq
    EDIT_SLEEP_TIMEOUT = 10
    DOWN_PATH = "downloads/"
    SW_API = os.environ.get("SW_API")
    ARQ_API_KEY = os.environ.get("ARQ_API_KEY")
    CHATS_DISABLED_KANG = (
      -1001471874620
)
    BLACK_LIST = (
      5257974366,
)
    DURACION_YT = (
      3609
)


trg = Config.TRIGGER
