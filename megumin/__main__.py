# Copyright (C) 2022 by fnixdev
#

from .bot import megux
from pyrogram import idle
import asyncio
from .utils.database.lang import load_language


async def main():
    await megux.start()
    await idle()
    await megux.stop()
    

if __name__ == "__main__" :
    asyncio.get_event_loop().run_until_complete(main())
