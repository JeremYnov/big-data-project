import os
from dotenv import load_dotenv
from pymongo import MongoClient
from kafka import KafkaConsumer

load_dotenv()

consumer = KafkaConsumer('crypto_news', bootstrap_servers=[os.getenv('KAFKA_BOOTSTRAP_SERVER')])

# connexion à la bdd
client = MongoClient('mongodb://root:root@mongodb:27017')

# connexion à la database
database = client['big-data-project']

# creation des collections
collection_news = database['news']
collection_symbol = database['symbol']

# recuperation des collections
symbol_db = database.get_collection("symbol")
news_db = database.get_collection("news")

# on balaye la liste news qui contient les news pour garder seulement les news qui ont un "code" crypto
for new in consumer:
    # si currency existe dans la news, c'est à dire si il y'a un code
    if "currencies" in new:
        for code in new['currencies']:
          # si le symbol crypto est dans notre table symbol
          if symbol_db.find_one({"name": f"{code['code']}/USD"}):
            # on recupere le symbol en question
            symbol = symbol_db.find_one({"name": f"{code['code']}/USD"})
            # dict qui contient toutes les infos interessantes de la news
            dict_news = {
                "published_at": new["published_at"],
                "symbol": symbol["_id"],
                "vote_positif": new["votes"]["positive"],
                "vote_negatif": new["votes"]["negative"],
                "like": new["votes"]["liked"],
                "disliked": new["votes"]["negative"],
                "count": 1
            }
            # si la news n'est pas bdd alors on l'ajoute (on ne veut pas de doublon!!!)
            if not news_db.find_one(dict_news):
              news_db.insert_one(dict_news)
