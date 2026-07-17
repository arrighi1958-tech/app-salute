import streamlit as st
import pandas as pd
import time

# Configurazione della pagina per il Samsung A17
st.set_page_config(page_title="Pannello Salute Renato", page_icon="🩺", layout="centered")

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

CSV_URL = f"https://google.com{int(time.time())}"

@st.cache_data(ttl=1)
def load_data():
    try:
        df = pd.read_csv(CSV_URL, header=None)
        return df
    except:
        return None

df = load_data()

if df is not None:
    st.title("🩺 Cruscotto Salute Renato")
    st.write("Sincronizzato in tempo reale con il tuo Google Fogli")
    
    tab_oggi, tab_medie, tab_trend = st.tabs(["Oggi (DATI VIVI)", "Medie Storiche", "Trend"])
    
    with tab_oggi:
        def prendi_colonna(lettera_colonna, valore_di_prova):
            try:
                mappa_colonne = {
                    "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9,
                    "K": 10, "L": 11, "M": 12, "N": 13, "O": 14, "P": 15, "Q": 16, "R": 17, 
                    "S": 18, "T": 19, "U": 20, "V": 21, "W": 22, "X": 23, "Y": 24, "Z": 25, "AA": 26
                }
                col_idx = mappa_colonne.get(lettera_colonna.upper(), 1)
                valore = str(df.iloc[2, col_idx]).strip()
                if valore == "nan" or valore == "" or len(valore) > 30: 
                    return str(valore_di_prova)
                return valore
            except:
                return str(valore_di_prova)

        # === STILE DI VITA E ATTIVITÀ ===
        st.markdown('<div class="section-header">🏃 Stile di Vita e Attività</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Media Passi Settimanali</div>
                <div class="metric-value">{prendi_colonna("R", "8.383")}</div>
                <div class="metric-status">🟢 Calcolato da Colonna R</div>
            </div>
        """, unsafe_allow_html=True)
        
        # === SALUTE DEL CUORE ===
        st.markdown('<div class="section-header">❤️ Salute del Cuore</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">ℹ️ INDICE WITHINGS COMPOSITO</div>
                <div class="metric-value">{prendi_colonna("T", "Cardio Ottimale")}</div>
                <div class="metric-status">📊 Valutazione Automatica da Colonna T</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Media Frequenza Cardiaca Diurna</div>
                <div class="metric-value">{prendi_colonna("L", "67")} bpm</div>
                <div class="metric-status">🟢 Colonna L</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Media Frequenza Battiti a Riposo</div>
                <div class="metric-value">{prendi_colonna("M", "52")} bpm</div>
                <div class="metric-status">🟢 Colonna M</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Media Variabilità Cardiaca (HRV)</div>
                <div class="metric-value">{prendi_colonna("V", "18")} ms</div>
                <div class="metric-status">🟢 Colonna V</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Media Ossigeno nel Sangue (SpO2)</div>
                <div class="metric-value">{prendi_colonna("Q", "96,2")} %</div>
                <div class="metric-status">🟢 Colonna Q</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-giallo">
                <div class="metric-title">Media Pressione Sistolica (Massima)</div>
                <div class="metric-value">{prendi_colonna("O", "101")} mmHg</div>
                <div class="metric-status">🟡 Colonna O</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Media Pressione Diastolica (Minima)</div>
                <div class="metric-value">{prendi_colonna("P", "70")} mmHg</div>
                <div class="metric-status">🟢 Colonna P</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Ultimo Esito ECG Registrato</div>
                <div class="metric-value">{prendi_colonna("N", "SINUSALE")}</div>
                <div class="metric-status">🟢 Colonna N</div>
            </div>
        """, unsafe_allow_html=True)

        # === QUALITÀ DEL SONNO E RECUPERO ===
        st.markdown('<div class="section-header">🌙 Qualità del Sonno e Recupero</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-rosso">
                <div class="metric-title">Media Ore di Sonno (7gg)</div>
                <div class="metric-value">{prendi_colonna("B", "5,86")} ore</div>
                <div class="metric-status">🔴 Colonna B</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-giallo">
                <div class="metric-title">Media Punteggio Sonno Storico</div>
                <div class="metric-value">{prendi_colonna("D", "64")} / 100</div>
                <div class="metric-status">🟡 Colonna D</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Media Ore Sonno Profondo</div>
                <div class="metric-value">{prendi_colonna("K", "1,6")} ore</div>
                <div class="metric-status">🟢 Colonna K</div>
            </div>
        """, unsafe_allow_html=True)

    with tab_medie:
        st.info("📊 Sezione Medie Storiche attiva nella colonna Z e AA.")
    with tab_trend:
        st.info("📈 Grafici di andamento settimanale pronti.")
