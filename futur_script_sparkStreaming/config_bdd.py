from pymongo import MongoClient

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