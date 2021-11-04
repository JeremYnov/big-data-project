#!/usr/local/bin/python3 

import ccxt 
import pandas as pd
from time import sleep 
from json import dumps 
from kafka import KafkaProducer 
 
producer = KafkaProducer( 
    bootstrap_servers='localhost:9092', 
    value_serializer=lambda x: dumps(x).encode('utf-8') 
)  

# while True : 
exchange = ccxt.binanceus()
markets = exchange.load_markets()
ticker = exchange.fetch_ticker('BTC/USD')

df = pd.DataFrame(markets)
columns = df.columns
USDCrypto = []
for column in columns : 
    splitedColumn = column.split('/')
    if splitedColumn[1] == 'USD':
        # USDCrypto.append(exchange.fetch_ticker(str(column)))
        producer.send('big-data-topic', value=exchange.fetch_ticker(str(column)))

print(type(USDCrypto))
# producer.send('big-data-topic', value=USDCrypto) 
sleep(1)