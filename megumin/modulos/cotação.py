import requests

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

@megux.on_message(filters.command(["cota"]))
async def pegar_cotacoes(_, message):
    requisicao = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL")

    requisicao_dic = requisicao.json()

    cotacao_dolar = requisicao_dic['USDBRL']['bid']
    dat_dolar = requisicao_dic ['USDBRL']['create_date']
    cotacao_euro = requisicao_dic['EURBRL']['bid']
    dat_euro = requisicao_dic['EURBRL']['create_date']
    cotacao_btc = requisicao_dic['BTCBRL']['bid']
    dat_btc = requisicao_dic['BTCBRL']['create_date']

    result = f'''
**Cotação das moedas:**

💵 **Dólar:** R$ ```{cotacao_dolar}```
🗓 **Data:**  ```{dat_dolar}```

💵 **Euro:** R$ ```{cotacao_euro}```
🗓 **Data:**  ```{dat_euro}```

💵 **BTC:** R$ ```{cotacao_btc}```
🗓 **Data:**  ```{dat_btc}```'''

    await message.reply_photo(photo="https://telegra.ph/file/d60e879db1cdba793a98c.jpg",
    caption=result)
    
    
