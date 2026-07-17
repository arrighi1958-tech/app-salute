import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Test Diagnostico Renato", layout="centered")
st.title("🩺 Test di Lettura Dati Renato")

CSV_URL = f"https://google.com{int(time.time())}"

try:
    df = pd.read_csv(CSV_URL, header=None)
    st.success("✅ Foglio connesso con successo! Ecco cosa vede il codice:")
    st.dataframe(df.head(15)) # Mostra le prime 15 righe in formato tabella pulita
except Exception as e:
    st.error(f"❌ Errore di lettura da Google: {e}")
