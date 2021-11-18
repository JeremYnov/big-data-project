import ccxt, calendar
import pandas as pd
from time import sleep
from json import dumps
from kafka import KafkaProducer
from datetime import datetime

producer = KafkaProducer(
  bootstrap_servers='kafka:29092',
  value_serializer=lambda x: dumps(x).encode('utf-8')
)

binance = ccxt.binanceus()

while True:
  try:
    tickers = binance.fetch_tickers()

    for ticker in tickers.values():
      producer.send('crypto_raw', ticker)
  except:
    print('ooops')

  sleep(20)

# df = pd.DataFrame(ohlcv, columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
# df['Time'] = [datetime.fromtimestamp(float(time)/1000) for time in df['Time']]
# df.set_index('Time', inplace=True)

# print(df)

# df = pd.DataFrame(markets)
# columns = df.columns
# USDCrypto = []
# for column in columns :
#   splitedColumn = column.split('/')
#   if splitedColumn[1] == 'USD':
#     # USDCrypto.append(exchange.fetch_ticker(str(column)))
#     producer.send('big-data-topic', value=exchange.fetch_ticker(str(column)))

# print(type(USDCrypto))
# producer.send('crypto_raw', value=USDCrypto)
# sleep(1)
