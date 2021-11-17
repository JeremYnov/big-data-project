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

    st.title('Comparaison entre plusieurs crypto')

    # on recupere tous les symbols dans l'ordre croissant par rapport à leurs noms pour les mettres dans le selectbox
    symbols = symbol_db.find({},{'_id': 0, 'name': 1}).sort("name")
    # on met tous les symbols dans une liste pour pouvoir les afficher dans le selectbox (histoire de format)
    list_symbols = []
    for symbol in symbols:
        list_symbols.append(symbol["name"])
    
    # recupére la valeur selectionner dans le selectbox -> BTC/USD par exemple
    dropdown = st.multiselect("choisis une crypto", list_symbols)

    # si il y'a une valeur alors on affiche les données des différentes crypto en continu
    if len(dropdown):
        # # on boucle sur dropdwon qui contient les noms des crypto 
        # for key,crypto in enumerate(dropdown):
        #     # on recupere la crypto à l'aide du symbol
        #     symbol = symbol_db.find_one({"name": crypto})
        #     crypto_symbol = crypto_db.find({"symbol": symbol["_id"]}, {"_id": 0, "symbol": 0,"low": 0, "high": 0, "average": 0, "date_time": 0})
        #     # si on est au premier tour de boucle, on laisse dans le df date_time, mais sinon on l'enleve car toutes les crypto on le meme datetime
        #     if key ==  0:
        #         crypto_symbol = crypto_db.find({"symbol": symbol["_id"]}, {"_id": 0, "symbol": 0,"low": 0, "high": 0, "average": 0})
            
        #     # transformation de crypto_symbol en df
        #     df = pd.DataFrame(crypto_symbol)
        #     # on renomme la colonne price en nom de la crypto pour differencier les differentes crypto dans ce df
        #     df = df.rename(columns={"price": symbol["name"]})

        #     if key == 0:
        #         # on renomme la colonne price en nom de la crypto pour differencier les differentes crypto dans ce df
        #         df = df.rename(columns={"date_time": "date_time", "price": symbol["name"]})
        #         # on reformate la date pour qu'elle soit plus jolie
        #         df["date_time"] = df["date_time"].str.replace('T',' ').str.replace('Z','')
            
        #         df_final = df
            
        #     else :
        #         # on concat le df_final avec le df en cours
        #         df_final = pd.concat([df_final, df.reindex(df_final.index)], axis=1)
            
            

        # df = df_final.rename(columns={'date_time':'index'}).set_index('index')
        chart = st.line_chart(df_chart(symbol_db, crypto_db, dropdown))
        
        # met à jours le graph toutes les 5s
        while True :
            chart.add_rows(df_chart(symbol_db, crypto_db, dropdown))
            sleep(5)




def df_chart(symbol_db, crypto_db, dropdown):
    """ fonction qui recupere le df pour une crypto pour l'affichage dans streamlit avec un graph
    Args:
        symbol_db (collection): collection des symbols
        crypto_db (collection): collection des stats des crypto
        crypto (str): symbol des crypto choisis dans le multiselect sur streamlit

    Returns:
        [df]: df contenant le prix, le max, le min et la mediane pour une crypto
    """
    # on boucle sur dropdwon qui contient les noms des crypto 
    for key,crypto in enumerate(dropdown):
        # on recupere la crypto à l'aide du symbol
        symbol = symbol_db.find_one({"name": crypto})
        crypto_symbol = crypto_db.find({"symbol": symbol["_id"]}, {"_id": 0, "symbol": 0,"low": 0, "high": 0, "average": 0, "date_time": 0})
        # si on est au premier tour de boucle, on laisse dans le df date_time, mais sinon on l'enleve car toutes les crypto on le meme datetime
        if key ==  0:
            crypto_symbol = crypto_db.find({"symbol": symbol["_id"]}, {"_id": 0, "symbol": 0,"low": 0, "high": 0, "average": 0})
        
        # transformation de crypto_symbol en df
        df = pd.DataFrame(crypto_symbol)
        # on renomme la colonne price en nom de la crypto pour differencier les differentes crypto dans ce df
        df = df.rename(columns={"price": symbol["name"]})

        if key == 0:
            # on renomme la colonne price en nom de la crypto pour differencier les differentes crypto dans ce df
            df = df.rename(columns={"date_time": "date_time", "price": symbol["name"]})
            # on reformate la date pour qu'elle soit plus jolie
            df["date_time"] = df["date_time"].str.replace('T',' ').str.replace('Z','')
        
            df_final = df
        
        else :
            # on concat le df_final avec le df en cours
            df_final = pd.concat([df_final, df.reindex(df_final.index)], axis=1)
        
        

    df = df_final.rename(columns={'date_time':'index'}).set_index('index')
    return df