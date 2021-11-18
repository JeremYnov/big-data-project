import ccxt
import pandas as pd
from json import dumps, loads
from pymongo import MongoClient
from time import sleep

# connexion à la bdd
client = MongoClient('mongodb://root:root@mongodb:27017')

# connexion à la database
database = client['big-data-project']

# creation des collections
collection_crypto = database['crypto']
collection_news = database['news']
collection_symbol = database['symbol']

# recuperation des collections
symbol_db = database.get_collection("symbol")
news_db = database.get_collection("news")
crypto_db = database.get_collection("crypto")

while True :
    exchange = ccxt.binanceus()
    markets = exchange.load_markets()
    ticker = exchange.fetch_ticker('BTC/USD')

    df = pd.DataFrame(markets)
    columns = df.columns
    USDCrypto = []
    for column in columns :
        splitedColumn = column.split('/')
        if splitedColumn[1] == 'USD':
            ##################################### A UTILISER POUR LE CONSUMER
            crypto = exchange.fetch_ticker(str(column)) # Variable qu'on recupere du producer
            # variable qui change si le symbol de la crypto est déjà dans la table symbol
            already = False
            # on boucle sur tous les symbols enn base et on verifie si le symbol est déjà dans la base
            for symbol in symbol_db.find({}):
                if symbol["name"] == crypto["symbol"]:
                    already = True
            # si il n'es pas dans la base on l'ajoute en base
            if not already :
                symbol_db.insert_one({"name": crypto["symbol"]})

            symbol = symbol_db.find_one({"name": crypto["symbol"]}) # recuperation du symbol crypto ex (BTC/USD)
            crypto_db.insert_one({"date_time": crypto["datetime"], "price": crypto["last"], "symbol": symbol["_id"], "high": crypto["high"], "low": crypto["low"], "average": crypto["average"]}) #INSERTION CRYPTO
            ########################################

    sleep(5)
    print("")
