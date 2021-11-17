import streamlit as st
from multiapp import MultiApp
from apps import home, data, model, compare_crypto

app = MultiApp()

st.markdown("""
# Big-Data Crypto
""")


app.add_app("Prix Crypto", home.app)
app.add_app("Data", data.app)
app.add_app("Model", model.app)
app.add_app("Comparaison crypto", compare_crypto.app)

app.run()
