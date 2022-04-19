import pandas_datareader as web
import datetime as dt
from requests import get
import json

def get_crypto(symbol: str):
    day = dt.date.today()
    respond = get("https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=200&sortBy=market_cap&sortType=desc&convert=USD&cryptoType=all&tagType=all&audited=false")
    symbols = json.loads(respond.text)["data"]["cryptoCurrencyList"]
    symbols = [i['symbol'] for i in symbols]
    if symbol in symbols:
        ltc = web.DataReader(f'{symbol}-USD', 'yahoo', day, day)
        return round(list(ltc['Adj Close'])[0], 2)
    else:
        return None
