import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Pannello Clinico Renato", page_icon="🩺", layout="centered")

# CSS
st.markdown("""
    <style>
    .stApp { background-color: #F4F6F7; }
    .metric-card {
        background-color: #ffffff; padding: 14px; border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06); margin-bottom: 12px; border-left: 8px solid #3498DB;
    }
    .metric-title { font-size: 14px; font-weight: 700; color: #2C3E50 !important; }
    .metric-value { font-size: 24px; font-weight: 800; color: #111111 !important; }
    .section-header {
        font-size: 18px; font-weight: 800; color: #1A5276; margin-top: 20px;
        margin-bottom: 12px; border-bottom: 2px solid #1A5276; padding-bottom: 4px;
    }
    </style>
""", unsafe_allow_html=True)

SHEET_ID = "1sKNtsluKQKPwqA-YToNexsHa0Gu7-Nnx8pCv628qeog"

# URL CORRETTI CON GID INVERTITI (gid=0 di solito è il primo foglio principale)
URL_PANNELLO = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
URL_CRONOLOGIA = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=320500951"

@st.cache_data(ttl=2)
def carica_dati(url):
    try:
        return pd.read_csv(url, header=None)
    except Exception:
        return None

df_p = carica_dati(URL_PANNELLO)
df_c = carica_dati(URL_CRONOLOGIA)

st.title("🩺 Scheda Clinica e Monitoraggio")

# PANNELLO CLINICO
if df_p is not None:
    st.markdown('<div class="section-header">🚨 PARAMETRI CLINICI PRIORTARI</div>', unsafe_allow_html=True)
    
    # Filtriamo ed estraiamo solo le righe valide del foglio sintetico
    for idx, row in df_p.iterrows():
        if len(row) >= 2 and pd.notna(row[0]) and str(row[0]).strip() != "":
            label = str(row[0]).strip()
            valore = str(row[1]).strip() if pd.notna(row[1]) else "--"
            
            # Escludiamo intestazioni generiche
            if label.lower() not in ["date", "data", "date [data]"]:
                st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-title">{label}</div>
                        <div class="metric-value">{valore}</div>
                    </div>
                ''', unsafe_allow_html=True)

# GRAFICO DI TENDENZA CRONOLOGIA
st.markdown('<div class="section-header">📈 GRAFICI DI TENDENZA CLINICA</div>', unsafe_allow_html=True)

if df_c is not None and len(df_c) > 1:
    try:
        df_plot = df_c.copy()
        df_plot.columns = df_plot.iloc[0]
        df_plot = df_plot[1:]
        
        col_x = df_plot.columns[0]
        col_y = df_plot.columns[1]
        
        df_plot[col_x] = pd.to_datetime(df_plot[col_x], errors='coerce')
        df_plot[col_y] = pd.to_numeric(df_plot[col_y].astype(str).str.replace(',', '.'), errors='coerce')
        
        df_plot = df_plot.dropna()
        
        if not df_plot.empty:
            fig = px.line(df_plot, x=col_x, y=col_y, markers=True, title=f"Tendenza {col_y}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Formato date o valori nella cronologia da verificare per la registrazione del grafico.")
    except Exception as e:
        st.info("Grafico in attesa di sincronizzazione dati...")
else:
    st.info("Impossibile caricare la Cronologia.")
