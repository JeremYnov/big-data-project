from pymongo import MongoClient

import ccxt 
import pandas as pd
from time import sleep 
from json import dumps, loads

# connexion à la bdd
client = MongoClient('localhost', 27017)

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
# on recupere tous les symboles
all_symbol = symbol_db.find({})
# on transforme le type "cursor" en dict qu'on stockera dans ce dict, pour ne pas avoir de doublon dans les symboles
all_symbol_dict = {}
# on ajoute au dict chaque name de crypto que contient la base pour eviter les doublons
for symbol in all_symbol :
    name = {"name": symbol["name"]}
    all_symbol_dict.update(name)
    
# for name in all_symbol.distinct('name') :
#     print(name)

# for name in crypto_db.find() :
#     print(name)

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
            symbol_db.update(all_symbol_dict, {"name": crypto["symbol"]}, upsert = True) # INSERE LES SYMBOLS SANS DOUBLON
            symbol = symbol_db.find_one({"name": crypto["symbol"]}) # recuperation du symbol crypto ex (BTC/USD)
            crypto_db.insert_one({"timestamp": crypto["timestamp"], "price": crypto["last"], "symbol": symbol["_id"]}) #INSERTION CRYPTO
            ########################################
            
            
    sleep(5)

# RECUPERATION DONNE D'UNE CRYPTO
# btc = symbol_db.find_one({"name": "ETH/USD"})
# print(btc)
# for name in crypto_db.find({"symbol" : btc["_id"]}) :
#     print(name)


