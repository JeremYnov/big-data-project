import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime
from time import sleep 


def app():
    

    # connexion à la bdd
    client = MongoClient('localhost', 27017)
    # connexion à la database
    database = client['big-data-project']
    crypto_db = database.get_collection("crypto")
    symbol_db = database.get_collection("symbol")

    st.title('Prix crypto')

    symbols = symbol_db.find({},{'_id': 0, 'name': 1}).sort("name")
    list_symbols = []
    for symbol in symbols:
        list_symbols.append(symbol["name"])
    
    dropdown = st.multiselect("choisis une crypto", list_symbols)

    if len(dropdown):
        for crypto in dropdown :
            
            symbol = symbol_db.find_one({"name": crypto})
            crypto_symbol = crypto_db.find({"symbol": symbol["_id"]}, {"_id": 0, "symbol": 0})
                
            df = pd.DataFrame(crypto_symbol)
            df["date_time"] = df["date_time"].str.replace('T',' ').str.replace('Z','')

            df = df.rename(columns={'date_time':'index'}).set_index('index')

        chart = st.line_chart(df)

    if len(dropdown):
        while True :
            for crypto in dropdown :
                
                symbol = symbol_db.find_one({"name": crypto})
                crypto_symbol = crypto_db.find({"symbol": symbol["_id"]}, {"_id": 0, "symbol": 0})
                    
                df = pd.DataFrame(crypto_symbol)
                df["date_time"] = df["date_time"].str.replace('T',' ').str.replace('Z','')

                df = df.rename(columns={'date_time':'index'}).set_index('index')

            chart.add_rows(df)
            sleep(5)

