from pyrogram import filters 
from pyrogram.types import Message 

from megumin import megux, Config 
from megumin.utils.decorators import input_str 

SUDOS = Config.SUDOS_GT_OFERTAS


@megux.on_message(filters.command("s"))
async def description_gt(c: megux, m: Message):
    if not input_str(m)
        return await m.reply("Você esqueceu dos argumentos!")
    title = m.text.split(None, 1)[1]
    preco = m.text.split(None, 1)[1]
    link = m.text.split(None, 1)[1]

    resultado = f"""
{title}\n\n💥 Preço de oferta: {preco}\nFrete grátis para prime💥\n\n📦{link}\n⚠ Sujeito a alteração de preço sem prévio aviso."""

    await m.reply(resultado)
