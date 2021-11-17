import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime
from time import sleep 
from bson.code import Code


def app():
    # connexion à la bdd
    client = MongoClient('localhost', 27017)
    # connexion à la database
    database = client['big-data-project']
    news_db = database.get_collection("news")
    symbol_db = database.get_collection("symbol")

    for n in news_db.find():
        print(n)

    # map = Code("function () {"
    # "    emit(this.symbol, 1);"
    # "}")

    # reduce = Code("function (key, values) {"
    #     "  var total = 0;"
    #     "  for (var i = 0; i < values.length; i++) {"
    #     "    total += values[i];"
    #     "  }"
    #     "  return total;"
    #     "}")
    
    # result_count = news_db.map_reduce(map, reduce, "count")
    # result_n_count = format_df(result_count, symbol_db)


    # map = Code("function () {"
    # "    emit(this.symbol, this.vote_positif);"
    # "}")
    
    # result_like = news_db.map_reduce(map, reduce, "positif")
    # result_n_like = format_df(result_like, symbol_db)

    # map = Code("function () {"
    # "    emit(this.symbol, this.vote_negatif);"
    # "}")
    
    # result_dislike = news_db.map_reduce(map, reduce, "negatif")
    # result_n_dislike = format_df(result_dislike, symbol_db)

    # # on transforme la liste en df, on rename la colonne value par le bon nom et on met en index le nom
    # df_count = pd.DataFrame(result_n_count).rename(columns={'value':'count'}).set_index('_id')
    # df_count["count"] = df_count["count"].astype(int)
    # df_like= pd.DataFrame(result_n_like).rename(columns={'value':'like'}).set_index('_id')
    # df_like["like"] = df_like["like"].astype(int)
    # df_dislike = pd.DataFrame(result_n_dislike).rename(columns={'value':'dislike'}).set_index('_id')
    # df_dislike["dislike"] = df_dislike["dislike"].astype(int)

    # df = df_count.join(df_like["like"]).join(df_dislike["dislike"]).sort_values(by='count', ascending=False)
    while True :
        table = st.dataframe(df_news(news_db, symbol_db))
        sleep(60)
        table.empty()
    

def df_news(news_db, symbol_db):
    """genere le df pour les stats sur les news"""
    map = Code("function () {"
    "    emit(this.symbol, 1);"
    "}")

    reduce = Code("function (key, values) {"
        "  var total = 0;"
        "  for (var i = 0; i < values.length; i++) {"
        "    total += values[i];"
        "  }"
        "  return total;"
        "}")
    
    result_count = news_db.map_reduce(map, reduce, "count")
    result_n_count = format_df(result_count, symbol_db)


    map = Code("function () {"
    "    emit(this.symbol, this.vote_positif);"
    "}")
    
    result_like = news_db.map_reduce(map, reduce, "positif")
    result_n_like = format_df(result_like, symbol_db)

    map = Code("function () {"
    "    emit(this.symbol, this.vote_negatif);"
    "}")
    
    result_dislike = news_db.map_reduce(map, reduce, "negatif")
    result_n_dislike = format_df(result_dislike, symbol_db)

    # on transforme la liste en df, on rename la colonne value par le bon nom et on met en index le nom
    df_count = pd.DataFrame(result_n_count).rename(columns={'value':'count'}).set_index('_id')
    df_count["count"] = df_count["count"].astype(int)
    df_like= pd.DataFrame(result_n_like).rename(columns={'value':'like'}).set_index('_id')
    df_like["like"] = df_like["like"].astype(int)
    df_dislike = pd.DataFrame(result_n_dislike).rename(columns={'value':'dislike'}).set_index('_id')
    df_dislike["dislike"] = df_dislike["dislike"].astype(int)

    df = df_count.join(df_like["like"]).join(df_dislike["dislike"]).sort_values(by='count', ascending=False)
    return df


def format_df(result, symbol_db) :
    """ formate avec en index le nom du symbol associer au count,like,dislike"""
    result_n = []
    for r in result.find():
        name = symbol_db.find_one({"_id": r["_id"]})
        result_n.append({"_id": name["name"], "value": r["value"]})  

    return result_n


    