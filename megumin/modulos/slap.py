
import random

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

@megux.on_message(filters.command(["slap"], prefixes=["/", "!"]))
async def printer(_, m: Message):
    DISABLED = get_collection(f"DISABLED {m.chat.id}")
    query = "slap"  
    off = await DISABLED.find_one({"_cmd": query})
    if off:
        return
    if m.reply_to_message:
        try:
            user1 = (
                f"<a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a>"
            )
        except:
            user1 = m.chat.title
        try:
            user2 = f"<a href='tg://user?id={m.reply_to_message.from_user.id}'>{m.reply_to_message.from_user.first_name}</a>"
        except:
            user2 = m.chat.title
        temp = random.choice(TEMPLATE)
        item = random.choice(ITENS)
        hit = random.choice(HIT)
        throw = random.choice(THROW)

        reply = temp.format(user1=user1, user2=user2, item=item, hits=hit, throws=throw)

        await m.reply(reply)
    else:
        await m.reply("Bruuuh")

TEMPLATE = [
    "__{user1} {hits} {user2} com um {item}.__",
    "__{user1} {hits} {user2} no rosto com um {item}.__",
    "__{user1} {hits} {user2} um pouco com um {item}.__",
    "__{user1} {throws} {item} no {user2}.__",
    "__{user1} {throws} {item} na cara do(a) {user2}.__",
    "__{user1} joga um {item} na cabeça do(a) {user2}.__",
    "__{user1} pensa em bater no(a) {user2} com {item}.__",
    "__{user1} derruba {user2} e repetidamente o {hits} com {item}.__",
    "__{user1} pega {item} e {hits} no(a) {user2}.__",
    "__{user1} amarra {user2} em uma cadeira e {throws} {item}.__",
    "__{user1} deu um empurrão amigável no(a) {user2} para que ele aprenda a nadar na lava__",
  ]

ITENS = [
      "frigideira de ferro fundido",
    "truta grande",
    "taco de beisebol",
    "bastão de cricket",
    "bengala de madeira",
    "unha",
    "penis de borracha",
    "pá",
    "ventilador",
    "um Nokia 3310",
    "torradeira",
    "Laptop da positivo",
    "televisão",
    "caminhão de cinco toneladas",
    "piroca",
    "livro",
    "laptop",
    "televisão antiga",
    "chifre do administrador",
    "um vibrador gigante",
    "galinha de borracha",
    "morcego cravado",
    "extintor de incêndio",
    "litro de 51",
    "pedaço de terra",
    "colméia",
    "pedaço de carne podre",
    "Urso",
    "a mãe do admin",
    "HB20",
    "fiat palio 2006 vermelho 2 portas",
    "gol quadrado 1986",
    "palio 12 marcha",
    "scania jacaré",
    "água",
    "caixa da água",
    "caixa d' agua",
    "transformador de poste",
    "magnetrom de microondas",
    "microondas samsung 1970",
    "laptop apple 1",
    "TV BOX",
    "fire tv stick",
    "iberê thenório",
    "vaca",
    "boi",
    "porco",
    "tijolo",
    "galinha",
    "fnm 180",
    "smartwatch iwo 13",
    "smartwatch DZ09",
    "DZ09",
    "bola",
    "monitor CRT",
    "chiqueiro",
    "Mercedes-Benz 608D",
    "picina 200L cheia",
    "megafone",
    "bomba",
    "rojão de vara",
    "bloco de cimento",
    "exynos fervente",
    "gelo",
    "xiomi redmi note 9",
    "moto e6i",
    "xiaomi redmi note 9", 
    "moldem da zyxel",
    "moldem da vivo",
    "fogão antigo",
    "lava louças",
    "volkswagen fusca 1986",
    "laptop da dell",
    "bola de basquete",
    "dinamite acesa",
    "LG K9",
    "pc fervente",
    "panela queimando",
    "botijão de gás",
    "scammer",
    "HV CURSOS",
    "Xbox 360 com luz vemelha",
    "dvd do sherek 3",
    "roteador da vivo",
    "roteador da zyxel",
    "mesa de 15kg"
  ]

THROW = [
  "joga",
  "lança",
  "arremessa",
  ]

HIT = [
    "golpeia",
    "bate",
    "golpeia",
    "esmurra",
    "ataca",
  ]
