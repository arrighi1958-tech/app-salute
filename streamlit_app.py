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

# URL DI ESPORTAZIONE DIRETTA CSV (Google Sheets)
DOC_ID = "2PACX-1vTPoEryjtZvVcaBEvSkgfh7qaeYXUJEmmDcZJh6fzBMZz80v1p7M009sdIVicHuI-Lj6AmC6SdWWsDj"
URL_PANNELLO = f"https://docs.google.com/spreadsheets/d/e/{DOC_ID}/pub?gid=320500951&single=true&output=csv"
URL_CRONOLOGIA = f"https://docs.google.com/spreadsheets/d/e/{DOC_ID}/pub?gid=784819219&single=true&output=csv"

@st.cache_data(ttl=5)
def carica_csv(url):
    try:
        return pd.read_csv(url, header=None)
    except Exception as e:
        return None

df_p = carica_csv(URL_PANNELLO)
df_c = carica_csv(URL_CRONOLOGIA)

st.title("🩺 Scheda Clinica e Monitoraggio")

# SE DIAGNOSTICA CSV (Per capire subito se il link risponde)
if df_p is None:
    st.error("⚠️ Impossibile scaricare i dati da Google Sheets. Verificare la connessione o i permessi del link.")
else:
    st.markdown('<div class="section-header">🚨 PARAMETRI CLINICI E BENESSERE</div>', unsafe_allow_html=True)
    
    # Visualizza i dati riga per riga trovati nel foglio Pannello
    for idx, row in df_p.iterrows():
        label = str(row[0]) if len(row) > 0 and pd.notna(row[0]) else ""
        valore = str(row[1]) if len(row) > 1 and pd.notna(row[1]) else "--"
        
        if label and label.strip() != "":
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-title">{label}</div>
                    <div class="metric-value">{valore}</div>
                </div>
            ''', unsafe_allow_html=True)

# GRAFICO DI TENDENZA
st.markdown('<div class="section-header">📈 GRAFICI DI TENDENZA CLINICA</div>', unsafe_allow_html=True)

if df_c is not None and len(df_c) > 1:
    try:
        # Pulisce la tabella e prende le prime due colonne
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
            st.info("Dati cronologia non sufficienti per il grafico.")
    except Exception as e:
        st.info("In attesa di dati validi per il grafico.")
else:
    st.info("Impossibile caricare il foglio Cronologia.")
