# Copyright (C) 2022 by fnixdev
#

from pyrogram import Client

import time
import os

START_TIME = time.time()

from megumin import version, Config

GP_LOGS = -1001556292785

class MeguminBot(Client):
    def __init__(self):
        kwargs = {
            'name': "megumin",
            'api_id': Config.API_ID,
            'api_hash': Config.API_HASH,
            'bot_token': Config.BOT_TOKEN,
            'in_memory': True,
            'plugins': dict(root="megumin.plugins")
        }
        super().__init__(**kwargs)

    async def start(self):
        await super().start()
        self.me = await self.get_me()
        text_ = f"#Whiter #Logs\n\n__WhiterKang está trabalhando agora.__\n\n**Versão:** `{version.__megumin_version__}`\n**System:** `{self.system_version}`\n**Python:** `{version.__python_version__}`\n**Pyrogram:** `{version.__pyro_version__}`"
        await self.send_message(chat_id=GP_LOGS, text=text_) 
        print("WhiterKang esta acordando...")

    async def stop(self):
        await super().stop()
        self.me = await self.get_me()
        text_ = f"#Whiter #sleep\n\n__WhiterKang foi dormir.__"
        await self.send_message(chat_id=GP_LOGS, text=text_)
        print("WhiterKang merreu...")

    async def send_log(self, text: str, *args, **kwargs):
        await self.send_message(
            chat_id=GP_LOGS,
            text=text,
            *args,
            **kwargs,
        )

megux = MeguminBot()
