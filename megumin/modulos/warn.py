import os
import asyncio 

from pyrogram import filters 
from pyrogram.types import (CallbackQuery, 
InlineKeyboardButton, 
InlineKeyboardMarkup,
Message, 
)


from megumin import megux 
from megumin.utils import get_collection


@megux.on_message(filters.command(["warm"], prefixes=["/", "!"]))
async def warm_(_, message):
    ids = (message.reply_to_message.from_user.id)
    WARMS = get_collection(f"WARM {ids}")
    name_user = (message.reply_to_message.from_user.mention())
    await asyncio.gather(WARMS.insert_one({"id_": ids, "title": name_user}))
    G = await WARMS.estimated_document_count()
    keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Remover Advertencia",
              callback_data="remove_warm_")]
            ]
        )
    await message.reply(f"Usuario {name_user} tem {G}/3 Advertências tenha cuidado!\nReason: <code>Xingando o bot</code>", reply_markup=(keyboard))
    
          


