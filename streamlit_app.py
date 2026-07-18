import streamlit as st
import pandas as pd
import time

# CONFIGURAZIONE GENERALE
st.set_page_config(page_title="Pannello Salute Renato", page_icon="🩺", layout="centered")

# STILI CSS PERSONALIZZATI
st.markdown("""
    <style>
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.06);
        margin-bottom: 15px;
        border-left: 12px solid #cccccc;
    }
    .metric-title {
        font-size: 20px;
        font-weight: bold;
        color: #333333;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 38px;
        font-weight: 800;
        color: #111111;
    }
    .metric-status {
        font-size: 16px;
        font-weight: 600;
        margin-top: 4px;
    }
    .section-header {
        font-size: 24px;
        font-weight: bold;
        color: #1A5276;
        margin-top: 25px;
        margin-bottom: 15px;
        border-bottom: 2px solid #1A5276;
        padding-bottom: 5px;
    }
    .bg-verde { border-left-color: #2ECC71 !important; color: #27AE60; }
    .bg-giallo { border-left-color: #F1C40F !important; color: #D4AC0D; }
    .bg-rosso { border-left-color: #E74C3C !important; color: #C0392B; }
    </style>
""", unsafe_allow_html=True)

# URL DEL TUO GOOGLE FOGLIO
BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTPoEryjtZvVcaBEvSkgfh7qaeYXUJEmmDcZJh6fzBMZz80v1p7M009sdIVicHuI-Lj6AmC6SdWWsDj/pub?gid=0&single=true&output=csv"
CSV_URL = f"{BASE_URL}&cache_bypass={int(time.time())}"

@st.cache_data(ttl=5)
def load_data():
    try:
        return pd.read_csv(CSV_URL, header=None)
    except Exception as e:
        return None

df = load_data()

st.title("🩺 Cruscotto Salute Renato (PIPPO)")
st.write("Sincronizzato in tempo reale con il tuo Google Fogli")

if df is None:
    st.error("⚠️ Impossibile collegarsi al Foglio Google.")

tab_oggi, tab_diagnostica = st.tabs(["Oggi (DATI VIVI)", "🔍 Controlla Dati Importati"])

with tab_oggi:
    def prendi_riga_dinamica(riga_foglio, valore_di_prova):
        try:
            if df is not None:
                valore = str(df.iloc[int(riga_foglio) - 1, 1]).strip()
                if valore != "nan" and valore != "":
                    return valore
            return str(valore_di_prova)
        except:
            return str(valore_di_prova)

    # === STILE DI VITA E ATTIVITÀ ===
    st.markdown('<div class="section-header">🏃 Stile di Vita e Attività</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Passi Settimanali</div>
            <div class="metric-value">{prendi_riga_dinamica(3, "8.383")}</div>
            <div class="metric-status">🟢 Dinamico su cella B3</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Giorni Totali Monitorati</div>
            <div class="metric-value">{prendi_riga_dinamica(4, "12")} giorni</div>
            <div class="metric-status">🟢 Dinamico su cella B4</div>
        </div>
    """, unsafe_allow_html=True)

with tab_diagnostica:
    st.markdown('<div class="section-header">🔍 Esploratore delle colonne caricate</div>', unsafe_allow_html=True)
    st.write("Ecco esattamente cosa sta leggendo Python dal tuo link in questo momento:")
    
    if df is not None:
        # Mostra le prime righe del foglio caricato per capire la sua struttura
        st.dataframe(df.head(10))
        st.write(f"Dimensioni del foglio letto: **{df.shape[0]} righe** e **{df.shape[1]} colonne**.")
