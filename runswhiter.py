import random

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

@megux.on_message(filters.command(["runs"]))
async def printer(_, m: Message):
    runs = random.choice(MEMES)
    await m.reply(f"__{runs}__")

MEMES = ["Aonde você pensa que está indo?"
     "Hein? O quê? Eles foram embora?",
     "ZZZZzz ... Hein? O quê? Ah, só eles de novo!",
     "Volte aqui!",
     "Não tão rápido...",
     "Olhe para a parede!",
     "Não me deixe sozinho com eles !!",
     "Corra, ou você morre.",
     "Piadas sobre você, eu estou em todo lugar",
     "Você está prestes a se arrepender ...",
     "Você também pode tentar /kickme, eu ouvi dizer que é divertido.",
     "Vá incomodar alguém, ninguém se importa aqui.",
     "Você pode correr, mas não pode se esconder.",
     "É tudo o que você tem?"
     "Estou atrás de você...",
     "Você tem companhia!",
     "Podemos fazer isso da maneira mais fácil ou mais difícil.",
     "Você não entende, não é?",
     "Sim, é melhor correr!",
     "Por favor, lembre-me o quanto eu me importo?",
     "Eu correria mais rápido se fosse você.",
     "Esse é definitivamente o bot que estamos procurando.",
     "Que as probabilidades estejam sempre a seu favor.",
     "Últimas palavras conhecidas.",
     "E eles desapareceram para sempre, para nunca mais vê-los.",
     "'Oh, olhe para mim! Eu sou tão legal e posso fugir de um bot!' - esta pessoa",
     "Sim, sim, basta tocar /kick já.",
     "Aqui, pegue este anel e vá até Mordor enquanto estiver nele.",
     "Diz a lenda, eles continuam correndo ...",
     "Ao contrário de Harry Potter, seus pais não podem protegê-lo de mim.","O medo leva à raiva. A raiva leva ao ódio. O ódio leva ao sofrimento. Se você continuar correndo com medo, pode",
     "seja o próximo Vader.",
     "Vários cálculos depois, decidi que meu interesse em suas travessuras é exatamente 0.",
     "Diz a lenda, eles continuam correndo.",
     "Mantenha, você não tem certeza de que queremos aqui de qualquer maneira.",
     "Você é um mágico- Oh. Espere. Você não é Harry, continue andando.",
     "Não há corredores nos corredores!",
     "Até a vista, bebe.",
     "Quem deixou os cachorros?",
     "É divertido, porque ninguém se importa.",
     "Ah, que desperdício. Gostei disso.","Francamente, minha querida, eu não dou a mínima.",
     "Meu smoothie traz todos os caras para o parquinho ... Então corra mais rápido!",
     "Você não pode ABRIR a verdade!",
     "Há muito tempo, em uma galáxia distante ... Alguém teria se importado com isso. Não mais.",
     "Ei, olhe para eles! Eles estão fugindo do inevitável martelo de bannillo ... fofo.",
     "Eles atiraram primeiro. Então eu fiz.",
     "O que você está concorrendo, um coelho branco?",
     "Como o médico diria ... CORRA!"
     ]