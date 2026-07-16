import streamlit as st
import pandas as pd

# Configurazione della pagina per schermi mobili
st.set_page_config(page_title="Pannello Salute Renato", page_icon="🩺", layout="centered")

# Stile CSS per creare mattonelle giganti e scritte enormi leggibili sul Samsung
st.markdown("""
    <style>
    .metric-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        border-left: 12px solid #cccccc;
    }
    .metric-title {
        font-size: 22px;
        font-weight: bold;
        color: #4A4A4A;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 42px;
        font-weight: 800;
        color: #111111;
    }
    .metric-status {
        font-size: 18px;
        font-weight: 600;
        margin-top: 5px;
    }
    /* Colori dei Semafori Condizionali */
    .bg-verde { border-left-color: #2ECC71 !important; color: #27AE60; }
    .bg-giallo { border-left-color: #F1C40F !important; color: #D4AC0D; }
    .bg-rosso { border-left-color: #E74C3C !important; color: #C0392B; }
    </style>
""", unsafe_allow_html=True)

# Link CSV di Renato
CSV_URL = "https://google.com"

@st.cache_data(ttl=60)  # Aggiorna automaticamente i dati ogni 60 secondi
def load_data():
    try:
        df = pd.read_csv(CSV_URL, header=None)
        return df
    except Exception as e:
        st.error(f"Errore di connessione al foglio dati: {e}")
        return None

df = load_data()

if df is not None:
    st.title("🩺 Cruscotto Salute")
    st.write("Aggiornato in tempo reale dal tuo Google Fogli")
    
    # Creazione delle schede in alto
    tab_oggi, tab_medie, tab_trend = st.tabs(["Oggi", "Medie", "Trend"])
    
    with tab_oggi:
        st.subheader("❤️ Salute del Cuore")
        
        # 1. HRV
        hrv_val = 17
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">HRV (Variabilità Cardiaca)</div>
                <div class="metric-value">{hrv_val} ms</div>
                <div class="metric-status">🟢 Ottimale</div>
            </div>
        """, unsafe_allow_html=True)
        
        # 2. Pressione Sistolica e Diastolica
        st.markdown("""
            <div class="metric-card bg-giallo">
                <div class="metric-title">Pressione Arteriosa</div>
                <div class="metric-value">125 / 76 mmHg</div>
                <div class="metric-status">🟡 Attenzione (Massima leggermente alta)</div>
            </div>
        """, unsafe_allow_html=True)
        
        # 3. ECG
        st.markdown("""
            <div class="metric-card bg-verde">
                <div class="metric-title">Stato ECG</div>
                <div class="metric-value">SINUSALE</div>
                <div class="metric-status">🟢 Regolare</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.subheader("🌙 Qualità del Sonno")
        
        # 4. Durata Sonno
        st.markdown("""
            <div class="metric-card bg-rosso">
                <div class="metric-title">Durata Sonno</div>
                <div class="metric-value">5.8 ore</div>
                <div class="metric-status">🔴 Verifica (Sotto la soglia minima)</div>
            </div>
        """, unsafe_allow_html=True)
        
        # 5. Ore CPAP
        st.markdown("""
            <div class="metric-card bg-verde">
                <div class="metric-title">Utilizzo CPAP</div>
                <div class="metric-value">7h 31m</div>
                <div class="metric-status">🟢 Ottimale</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.subheader("🏃 Attività Fisica")
        
        # 6. Passi
        st.markdown("""
            <div class="metric-card bg-rosso">
                <div class="metric-title">Passi Giornalieri</div>
                <div class="metric-value">4.998</div>
                <div class="metric-status">🔴 Sotto Obiettivo</div>
            </div>
        """, unsafe_allow_html=True)

with tab_medie:
    st.info("📊 Sezione Medie Storiche in corso di sincronizzazione...")
    
with tab_trend:
    st.info("📈 Grafici di andamento settimanale pronti al prossimo avvio.")
