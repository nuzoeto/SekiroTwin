# Copyright (C) 2022 by fnixdev
#

from pyrogram import Client

import time
import os

START_TIME = time.time()

class MeguBot(Client):
    def __init__(self):
        kwargs = {
            'api_id': os.environ.get("API_ID"),
            'api_hash': os.environ.get("API_HASH"),
            'session_name': ":memory:",
            'bot_token': os.environ.get("BOT_TOKEN"),
            'plugins': dict(root="megumin/modulos")
        }
        super().__init__(**kwargs)

    async def start(self):
        await super().start()
        print("Megumin esta acordando...")

    async def stop(self):
        await super().stop()
        print("Megumin merreu...")

megux = MeguBot()
