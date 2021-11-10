from config_bdd import symbol_db, news_db, crypto_db

from time import sleep
from json import dumps
import requests


API_KEY = '4cb209d86481440649b653af92741b370037dbde'
url = "https://cryptopanic.com/api/v1/posts/?auth_token={}".format(API_KEY)

while True :
    try:
        page = requests.get(url)
        data = page.json()
        news = data['results']
        # on balaye la liste news qui contient les news pour garder seulement les news qui ont un "code" crypto
        for new in news :
            # si currency existe dans la news, c'est à dire si il y'a un code
            if "currencies" in new:
                for code in new['currencies']:
                    # si le symbol crypto est dans notre table symbol
                    if symbol_db.find_one({"name": f"{code['code']}/USD" }):
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
                        "count" : 1
                        }
                        # si la news n'est pas bdd alors on l'ajoute (on ne veut pas de doublon!!!)
                        if not news_db.find_one(dict_news) :
                            news_db.insert_one(dict_news)
            print("cool")

    except:
        print('error')
    sleep(10)

# SI UN CODE N'EST PAS DANS NOS SYMBOL DANS LES NEWS LE PASSER
for a in news_db.find({}):
    print(a)