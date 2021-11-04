import ccxt 
import pandas as pd 
import time

exchange = ccxt.binanceus()
markets = exchange.load_markets()
ticker = exchange.fetch_ticker('BTC/USD')

df = pd.DataFrame(markets)
columns = df.columns
USDCrypto = []
for column in columns : 
    splitedColumn = column.split('/')
    if splitedColumn[1] == 'USD':
        print(column)
        USDCrypto.append(exchange.fetch_ticker(str(column)))
            

dfCrypto = pd.DataFrame(USDCrypto)   
dfCrypto.head(1)