import requests
import asyncio 

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

@megux.on_message(filters.command(["cota"]))
async def pegar_cotacoes(_, message):
    requisicao = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL")

    requisicao_dic = requisicao.json()

    cotacao_dolar = requisicao_dic['USDBRL']['bid']
    dat_dolar = requisicao_dic ['USDBRL']['create_date']
    var_dolar = requisicao_dic ['USDBRL']['varBid']
    cotacao_euro = requisicao_dic['EURBRL']['bid']
    dat_euro = requisicao_dic['EURBRL']['create_date']
    var_euro = requisicao_dic ['EURBRL']['varBid']
    cotacao_btc = requisicao_dic['BTCBRL']['bid']
    dat_btc = requisicao_dic['BTCBRL']['create_date']
    var_btc = requisicao_dic ['BTCBRL']['varBid']

    obting_info = await message.reply(f"""```Obtendo informações sobre as moedas...```""")
    await asyncio.sleep(0.4)
    await obting_info.delete()

    result = f'''
**Cotação das moedas:**

💵 **Dólar:** R$ ```{cotacao_dolar}```
🗓 **Data:**  ```{dat_dolar}```
📊 **Variação:** ```{var_dolar}```

💵 **Euro:** R$ ```{cotacao_euro}```
🗓 **Data:**  ```{dat_euro}```
📊 **Variação:** ```{var_euro}```

💵 **BTC:** R$ ```{cotacao_btc}```
🗓 **Data:**  ```{dat_btc}```
📊 **Variação:** ```{var_btc}```'''

    await message.reply_photo(photo="https://telegra.ph/file/d60e879db1cdba793a98c.jpg",
    caption=result)
    
    
