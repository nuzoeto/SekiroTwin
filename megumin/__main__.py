# Copyright (C) 2022 by fnixdev
#
import logging

from .bot import megux
from pyrogram import idle
from logging.handlers import RotatingFileHandler
import asyncio
from .utils.database.lang import load_language

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s - %(levelname)s] - %(name)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    handlers=[
                        RotatingFileHandler(
                            "WhiterKang.log", maxBytes=20480, backupCount=10),
                        logging.StreamHandler()
                    ])

logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pyrogram.parser.html").setLevel(logging.ERROR)
logging.getLogger("pyrogram.session.session").setLevel(logging.ERROR)


async def main():
    load_language()
    await megux.start()
    await idle()
    await megux.stop()
    

if __name__ == "__main__" :
      asyncio.get_event_loop().run_until_complete(main())
