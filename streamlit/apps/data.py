import streamlit as st
import numpy as np
import pandas as pd
import streamlit_wordcloud as wordcloud
from pymongo import MongoClient

# from sklearn import datasets

def app():
    # connexion à la bdd
    client = MongoClient('localhost', 27017)
    # connexion à la database
    database = client['big-data-project']
    news_db = database.get_collection("news")
    symbol_db = database.get_collection("symbol")
    
    symbols = symbol_db.find({},{'_id': 0, 'name': 1}).sort("name")
    list_symbols = []
    for symbol in symbols:
        list_symbols.append(symbol["name"])

    
    st.title('Crypto-News')

    st.write("This is the `Data` page of the multi-page app.")

    st.write("The following is the DataFrame of the `iris` dataset.")

    # iris = datasets.load_iris()
    # X = pd.DataFrame(iris.data, columns = iris.feature_names)
    # Y = pd.Series(iris.target, name = 'class')
    # df = pd.concat([X,Y], axis=1)
    # df['class'] = df['class'].map({0:"setosa", 1:"versicolor", 2:"virginica"})

    # st.write(df)
    crypto_news = []
    for symbol in list_symbols:
        crypto_symbol = symbol_db.find_one({"name": symbol})
        crypto_news_count = news_db.find({"symbol": crypto_symbol["_id"]})
        
        print(crypto_symbol)
        print(crypto_news_count.count())
        crypto_news.append(dict(text=symbol, value=crypto_news_count.count(), color="#b5de2b", symbol=symbol))
        # sleep(5)
    # for name in news_db.find({"symbol": btc["_id"]}) :
    #     print(name)
    
    print(crypto_news)
    return_obj = wordcloud.visualize(crypto_news, tooltip_data_fields={
        'text':'Nom', 'value':'Mentions', 'symbol':'Symbol'
    }, per_word_coloring=False)
    # words = [
    #     dict(text="Robinhood", value=16000, color="#b5de2b", country="US", industry="Cryptocurrency"),
    #     dict(text="Personio", value=8500, color="#b5de2b", country="DE", industry="Human Resources"),
    #     dict(text="Boohoo", value=6700, color="#b5de2b", country="UK", industry="Beauty"),
    #     dict(text="Deliveroo", value=13400, color="#b5de2b", country="UK", industry="Delivery"),
    #     dict(text="SumUp", value=8300, color="#b5de2b", country="UK", industry="Credit Cards"),
    #     dict(text="CureVac", value=12400, color="#b5de2b", country="DE", industry="BioPharma"),
    #     dict(text="Deezer", value=10300, color="#b5de2b", country="FR", industry="Music Streaming"),
    #     dict(text="Eurazeo", value=31, color="#b5de2b", country="FR", industry="Asset Management"),
    #     dict(text="Drift", value=6000, color="#b5de2b", country="US", industry="Marketing Automation"),
    #     dict(text="Twitch", value=4500, color="#b5de2b", country="US", industry="Social Media"),
    #     dict(text="Plaid", value=5600, color="#b5de2b", country="US", industry="FinTech"),
    # ]
    # return_obj = wordcloud.visualize(words, tooltip_data_fields={
    #     'text':'Company', 'value':'Mentions', 'country':'Country of Origin', 'industry':'Industry'
    # }, per_word_coloring=False)
