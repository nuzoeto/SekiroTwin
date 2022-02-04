# Copyright (C) 2022 by fnixdev
#

__all__ = ["Config"]

import os


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
    )
    LOG_CHANNEL_ID = set([-1001569084822])
    ADMINS = {}
    LASTFM_API_KEY = os.environ.get("LASTFM_API_KEY")
    DB_URI = os.environ.get("DATABASE_URL")
    WHITELIST_CHATS = set([])  # chat id aq
    EDIT_SLEEP_TIMEOUT = 10
    DOWN_PATH = "downloads/"
    ARQ_API_KEY = os.environ.get("ARQ_API_KEY")

# Prefixes for commands
# e.g: /command and !command
prefix = ["/", "!"]
