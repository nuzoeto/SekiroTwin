from pyrogram import filters 
from pyrogram.types import Message 

from megumin import megux, Config 
from megumin.utils.decorators import input_str 

SUDOS = Config.SUDOS_GT_OFERTAS


@megux.on_message(filters.command("s"))
async def description_gt(c: megux, m: Message):
    if not input_str(m):
        return await m.reply("Você esqueceu dos argumentos!")
    str_args = m.text.split()
    title = str_args[1]
    preco = str_args[2]
    link = str_args[3]

    resultado = f"""
{title}\n\n💥 Preço de oferta: {preco}\nFrete grátis para prime💥\n\n📦{link}\n⚠ Sujeito a alteração de preço sem prévio aviso."""

    await m.reply(resultado)
