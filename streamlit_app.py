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

# URL DEL TUO GOOGLE FOGLIO (RIEPILOGO)
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

tab_oggi, tab_medie = st.tabs(["Oggi (DATI VIVI)", "📊 Medie Storiche Complete"])

# Funzione sicura per estrarre il valore dalla colonna 1 (B)
def ottieni_valore(indice_riga, valore_default):
    try:
        if df is not None:
            valore = str(df.iloc[indice_riga, 1]).strip()
            if valore != "nan" and valore != "" and valore != "None":
                return valore
    except:
        pass
    return valore_default

with tab_oggi:
    # === STILE DI VITA E ATTIVITÀ ===
    st.markdown('<div class="section-header">🏃 Stile di Vita e Attività</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Passi Settimanali</div>
            <div class="metric-value">{ottieni_valore(2, "5.657")}</div>
            <div class="metric-status">🟢 Preso in tempo reale dal foglio</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Giorni Totali Monitorati</div>
            <div class="metric-value">{ottieni_valore(3, "18")} giorni</div>
            <div class="metric-status">🟢 Conteggio complessivo dal foglio</div>
        </div>
    """, unsafe_allow_html=True)
    
    # === SALUTE DEL CUORE ===
    st.markdown('<div class="section-header">❤️ Salute del Cuore</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">ℹ️ INDICE WITHINGS COMPOSITO</div>
            <div class="metric-value">{ottieni_valore(4, "Cardio Ottimale")}</div>
            <div class="metric-status">🟢 Stato di salute generale</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Frequenza Cardiaca Diurna</div>
            <div class="metric-value">{ottieni_valore(6, "67")} bpm</div>
            <div class="metric-status">🟢 Durante le ore di veglia</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Frequenza Battiti a Riposo (7gg)</div>
            <div class="metric-value">{ottieni_valore(7, "52")} bpm</div>
            <div class="metric-status">🟢 Battito cardiaco a riposo</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Variabilità Cardiaca (HRV) (7gg)</div>
            <div class="metric-value">{ottieni_valore(8, "18")} ms</div>
            <div class="metric-status">🟢 Indicatore del sistema nervoso autonomo</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Ossigeno nel Sangue (SpO2)</div>
            <div class="metric-value">{ottieni_valore(9, "96,2")} %</div>
            <div class="metric-status">🟢 Saturazione media rilevata</div>
        </div>
    """, unsafe_allow_html=True)

with tab_medie:
    st.markdown('<div class="section-header">📊 Quadro Generale delle Medie Storiche</div>', unsafe_allow_html=True)
    st.write("Tutti i parametri aggregati estratti dal tuo storico per il monitoraggio clinico a lungo termine:")
    
    # Sezione 1: Parametri Cardiovascolari (Priorità per Ipertensione e Betabloccanti)
    st.markdown('### 🩺 Monitoraggio Cardio-Vascolare')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="metric-card bg-giallo">
                <div class="metric-title">Pressione Sistolica Media</div>
                <div class="metric-value">{ottieni_valore(10, "101")} mmHg</div>
                <div class="metric-status">Media Storica Massima (Target < 130-140)</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Battito Medio a Riposo</div>
                <div class="metric-value">{ottieni_valore(7, "52")} bpm</div>
                <div class="metric-status">Effetto Betabloccante (Target stabile 50-60)</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Pressione Diastolica Media</div>
                <div class="metric-value">{ottieni_valore(11, "70")} mmHg</div>
                <div class="metric-status">Media Storica Minima (Target < 80-85)</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Variabilità Cardiaca (HRV)</div>
                <div class="metric-value">{ottieni_valore(8, "18")} ms</div>
                <div class="metric-status">Livello di recupero e stress cardiaco</div>
            </div>
        """, unsafe_allow_html=True)

    # Sezione 2: Parametri Riposo e Attività (Priorità per Sonno/Prostata e Circolazione)
    st.markdown('### 🌙 Sonno, Prostata e Attività Fisica')
    col3, col4 = st.columns(2)
    with col3:
        st.markdown(f"""
            <div class="metric-card bg-rosso">
                <div class="metric-title">Risvegli Notturni Medi</div>
                <div class="metric-value">{ottieni_valore(18, "3,2")}</div>
                <div class="metric-status">Indicatore disturbi (es. Prostata/Nicturia)</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Passi Storici Medi</div>
                <div class="metric-value">{ottieni_valore(2, "5.657")}</div>
                <div class="metric-status">Attività motoria (Ottimo per fluidificanti)</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
            <div class="metric-card bg-giallo">
                <div class="metric-title">Efficienza del Sonno</div>
                <div class="metric-value">{ottieni_valore(19, "63,53 %")}</div>
                <div class="metric-status">Qualità reale del tempo passato a letto</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Temperatura Corporea</div>
                <div class="metric-value">{ottieni_valore(20, "36,41")} °C</div>
                <div class="metric-status">Media basale notturna</div>
            </div>
        """, unsafe_allow_html=True)
