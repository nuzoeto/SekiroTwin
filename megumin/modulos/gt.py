from pyrogram import filters 
from pyrogram.types import Message 

from megumin import megux, Config 
from megumin.utils.decorators import input_str 

SUDOS = Config.SUDOS_GT_OFERTAS


@megux.on_message(filters.command("s" Config.TRIGGER) & filters.user(SUDOS)
async def description_gt(c: megux, m: Message):
    title = input_str(m)
    preco = input_str(m)
    link = input_str(m)

    resultado = f"""
{title}\n\n💥 Preço de oferta: {preco}\nFrete grátis para prime💥\n\n📦{link}\n⚠ Sujeito a alteração de preço sem prévio aviso."""
"""

    await m.reply(resultado)
