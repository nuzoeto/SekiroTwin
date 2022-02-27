import requests
import asyncio 

from pyrogram import filters
from pyrogram.types import Message

from megumin import megux

@megux.on_message(filters.command(["cota"], prefixes=["/", "!"]))
async def pegar_cotacoes(_, message):
    requisicao = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,GBP-BRL,JPY-BRL,BTC-BRL,ETH-BRL,XRP-BRL,DOGE-BRL,ARS-BRL,AOA-BRL")

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
    cotacao_iene = requisicao_dic ['JPYBRL']['bid']
    dat_iene = requisicao_dic ['JPYBRL']['create_date']
    var_iene = requisicao_dic ['JPYBRL']['varBid']
    cotacao_doge = requisicao_dic ['DOGEBRL']['bid']
    dat_doge = requisicao_dic ['DOGEBRL']['create_date']
    var_doge = requisicao_dic ['DOGEBRL']['varBid']
    cotacao_ars = requisicao_dic ['ARSBRL']['bid']
    dat_ars = requisicao_dic ['ARSBRL']['create_date']
    var_ars = requisicao_dic ['ARSBRL']['varBid']
    cotacao_kwanza = requisicao_dic ['AOABRL']['bid']

    obting_info = await message.reply(f"""```Obtendo informações sobre as moedas...```""")
    await asyncio.sleep(0.3)
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

📊 **Variação:** ```{var_btc}```


💵 **DOGE:** R$ ```{cotacao_doge}```
🗓 **Data:** ```{dat_doge}```

📊 **Variação:** ```{var_doge}```


💵 **Iene:** R$ ```{cotacao_iene}```
🗓 **Data:** ```{dat_iene}```

📊 **Variação:** ```{var_iene}```


💵 **Peso Argentino:** R$ ```{cotacao_ars}```
🗓 **Data:** ```{dat_ars}```

📊 **Variação:** ```{var_ars}```


💵 **KWANZA** R$ ```{cotacao_kwanza}```
'''

    await message.reply_photo(photo="https://telegra.ph/file/d60e879db1cdba793a98c.jpg",
    caption=result)
    
    
