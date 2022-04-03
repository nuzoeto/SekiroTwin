# Copyright (C) 2022 by fnixdev
#

from pyrogram import Client

import time
import os

START_TIME = time.time()

from megumin import version

GP_LOGS = -1001556292785

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
        self.me = await self.get_me()
        text_ = f"#Whiter #Logs\n\n__WhiterKang está trabalhando agora.__\n\n**Versão:** {version.__megumin_version__}\n**System:** {self.system_version}\n**Python:** {version.__python_version__}\n**Pyrogram:** {version.__pyro_version__}"
        await self.send_mesaage(chat_id=GP_LOGS, text=text_) 
        print("WhiterKang esta acordando...")

    async def stop(self):
        await super().stop()
        print("WhiterKang merreu...")

megux = MeguBot()
