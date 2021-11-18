import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime
from time import sleep
import altair as alt


def app():
    # connexion à la bdd
    client = MongoClient('mongodb://root:root@mongodb:27017')
    # connexion à la database
    database = client['big-data-project']
    crypto_db = database.get_collection("crypto")
    symbol_db = database.get_collection("symbol")

    st.title('Prix crypto')

    # on recupere tous les symbols dans l'ordre croissant par rapport à leurs noms pour les mettres dans le selectbox
    symbols = symbol_db.find({},{'_id': 0, 'name': 1}).sort("name")
    # on met tous les symbols dans une liste pour pouvoir les afficher dans le selectbox (histoire de format)
    list_symbols = []
    for symbol in symbols:
        list_symbols.append(symbol["name"])
    
    # recupére la valeur selectionner dans le selectbox -> BTC/USD par exemple
    dropdown = st.selectbox("choisis une crypto", list_symbols)

    alt.Chart(df_chart(symbol_db, crypto_db, dropdown)).mark_bar().encode(
    x=alt.X('index:Q', axis=alt.Axis(tickCount=20, grid=False)),
    y=alt.Y('price:Q'))

    # si il y'a une valeur alors on affiche les données de la crypto en continu
    if dropdown :    
        col1, col2, col3, col4 = st.columns(4)
        symbol = symbol_db.find_one({"name": dropdown})
        crypto_symbol = crypto_db.find({"symbol": symbol["_id"]}, {"_id": 0, "symbol": 0})
        col1.metric("Prix Actuel", round(crypto_symbol[0]['price'], 2))
        col2.metric("Plus Haut 24H", round(crypto_symbol[0]['high'], 2))
        col3.metric("Plus Bas 24H", round(crypto_symbol[0]['low'], 2))   
        col4.metric("Prix Moyen", round(crypto_symbol[0]['average'], 2))   
        chart = st.line_chart(df_chart(symbol_db, crypto_db, dropdown))
        
        # met à jours le graph toutes les 5s
        while True :
            chart.add_rows(df_chart(symbol_db, crypto_db, dropdown))
            sleep(5)


def df_chart(symbol_db, crypto_db, crypto):
    """ fonction qui recupere le df pour une crypto pour l'affichage dans streamlit avec un graph
    Args:
        symbol_db (collection): collection des symbols
        crypto_db (collection): collection des stats des crypto
        crypto (str): symbol de la crypto choisis dans le selectbox sur streamlit

    Returns:
        [df]: df contenant le prix, le max, le min et la mediane pour une crypto
    """
    symbol = symbol_db.find_one({"name": crypto})
    crypto_symbol = crypto_db.find({"symbol": symbol["_id"]}, {"_id": 0, "symbol": 0})

    df = pd.DataFrame(crypto_symbol)
    df["date_time"] = df["date_time"].str.replace('T',' ').str.replace('Z','')

    df = df.rename(columns={'date_time':'index'}).set_index('index')
    return df.tail(10)

