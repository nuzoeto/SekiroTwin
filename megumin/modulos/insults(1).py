import random

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

@megux.on_message(filters.command(["insults"]))
async def printer(_, m: Message):
    insult = random.choice(INSULTS)
    await m.reply(f"__{insult}__")

INSULTS = ["Por que você é tão idiota assim?",
     "Infelizmente sua mãe não conseguiu abortar você a tempo.",
     "Acho melhor você sair da minha frente, não gosto de poluição visual.",
     "Comando não encontrado. Como seu pai.",
     "Você percebe que está fazendo algo bobo? Aparentemente não.",
     "Você pode escrever melhor que isso.",
     "A regra bot 157 da seção 9 me impede de responder a seres humanos estúpidos como você.",
     "Tão idiota que tenho ate vontade não responder.",
     "Acredite, você não é normal.",
     "Aposto que seu cérebro parece tão bom quanto novo, visto que você nunca o usa.",
     "Se eu quisesse me matar, vou elevar seu ego e pular para o seu QI.",
     "Zumbis comem cérebros ... você está seguro.",
     "Você não evoluiu dos macacos, eles evoluíram de você.",
     "Volte e fale comigo quando o seu QI exceder a sua idade.",
     "Não estou dizendo que você é estúpido, só estou dizendo que você teve azar quando se trata de pensar.",
     "Em que língua você está falando? Porque parece uma merda.",
     "A estupidez não é um crime, então você é livre para sair.",
     "Você é a prova de que a evolução CAN pode ser revertida.",
     "Eu pergunto quantos anos você tem, mas eu sei que você não pode contar tão alto.",
     "Como alguém de fora, o que você acha da raça humana?",
     "As chuvas não são tudo, no seu caso não são nada.",
     "Pessoas normais vivem e aprendem. Você apenas vive.",
     "Eu não sei o que faz você ser tão estúpido, mas realmente funciona.",
     "Continue falando, um dia você dirá algo inteligente! (Duvido, no entanto)",
     "Estou surpreso, diga algo inteligente.",
     "Seu QI é menor que o tamanho dos seus sapatos.",
     "Uau! Seus neurotransmissores não funcionam mais.",
     "Você é louco por ser burro?",
     "Todo mundo tem o direito de ser estúpido, mas o privilégio está sendo abusado.",
     "Desculpe quando te chamei de idiota. Pensei que você já sabia disso.",
     "Você deve tentar provar cianeto.",
     "Suas enzimas são projetadas para digerir veneno de rato.",
     "Você deveria tentar dormir para sempre.",
     "Pegue uma arma e atire em si mesmo.",
     "Você poderia fazer um recorde mundial pulando de um avião sem pára-quedas.",
     "Pare de falar besteiras e pule na frente de um trem-bala.",
     "Tente tomar banho com ácido clorídrico em vez de água.",
     "Tente o seguinte: se você ficar sem fôlego por uma hora, poderá salvá-lo para sempre.",
     "Fica verde! Pare de inalar oxigênio."
     "Deus estava procurando por você. Você deveria sair para encontrá-lo.",
     "Dê 100%. Agora, doe sangue.",
     "Tente pular de cem andares, mas você só pode fazê-lo uma vez.",
     "Você deve doar seu cérebro, visto que nunca o usou.",
     "Ofereça-se para mirar em um campo de tiro.",
     "Fotos na cabeça são divertidas. Pegue uma.",
     "Você deve tentar nadar com grandes tubarões brancos.",
     "Você deve se pintar de vermelho e correr em uma maratona de bolas.",
     "Você pode ficar embaixo da água pelo resto da vida sem voltar a subir.",
     "Que tal você parar de respirar como um dia? Isso será ótimo.",
     "Tente provocar um tigre enquanto ambos estão em uma gaiola.",
     "Você já tentou atirar em si mesmo a 100 metros de distância usando um canon.",
     "Você deve tentar manter o TNT na boca e ligá-lo.",
     "Tente jogar catch and launch com RDX, sua diversão.",
     "Ouvi dizer que a fotografia é venenosa, mas suponho que você não se importe em inalá-la por diversão.",
     "Deixe-se ir para o espaço esquecendo o oxigênio na Terra.",
     "Você deve tentar jogar cobra e escadas, com cobras reais e sem escadas.",
     "Dance nua em um par de cabos HT.",
     "O verdadeiro vulcão é a melhor piscina para você.",
     "Você deve tentar o banho quente em um vulcão.",
     "Tente passar um dia em uma lanchonete e será sua para sempre.",
     "Acerte o urânio com um trenó lento em sua presença. Será uma experiência que vale a pena.",
     "Você pode ser a primeira pessoa a pisar no sol. Experimente."]