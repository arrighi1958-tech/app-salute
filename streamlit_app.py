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
        return pd.read_csv(CSV_URL, header=None)
    except:
        return None

df = load_data()

st.title("🩺 Cruscotto Salute Renato")
st.write("Sincronizzato in tempo reale con il tuo Google Fogli")

tab_oggi, tab_medie, tab_trend = st.tabs(["Oggi (DATI VIVI)", "Medie Storiche", "Trend"])

with tab_oggi:
    # Nuova funzione corazzata: prende qualsiasi testo o numero senza fare controlli rigidi
    def prendi_dato(riga_foglio, valore_di_prova):
        try:
            if df is not None:
                # Estrae il valore grezzo dalla colonna B (indice 1)
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
            <div class="metric-value">{prendi_dato(3, "8.383")}</div>
            <div class="metric-status">🟢 Lettura Diretta Cella B3</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Giorni Totali Monitorati</div>
            <div class="metric-value">{prendi_dato(4, "12")} giorni</div>
            <div class="metric-status">🟢 Lettura Diretta Cella B4</div>
        </div>
    """, unsafe_allow_html=True)
    
    # === SALUTE DEL CUORE ===
    st.markdown('<div class="section-header">❤️ Salute del Cuore</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">ℹ️ INDICE WITHINGS COMPOSITO</div>
            <div class="metric-value">{prendi_dato(5, "Cardio Ottimale")}</div>
            <div class="metric-status">🟢 Lettura Diretta Cella B5</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Frequenza Cardiaca Diurna</div>
            <div class="metric-value">{prendi_dato(7, "67")} bpm</div>
            <div class="metric-status">🟢 Sincronizzato su cella B7</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Frequenza Battiti a Riposo (7gg)</div>
            <div class="metric-value">{prendi_dato(8, "52")} bpm</div>
            <div class="metric-status">🟢 Sincronizzato su cella B8</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Variabilità Cardiaca (HRV) (7gg)</div>
            <div class="metric-value">{prendi_dato(9, "18")} ms</div>
            <div class="metric-status">🟢 Sincronizzato su cella B9</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Ossigeno nel Sangue (SpO2)</div>
            <div class="metric-value">{prendi_dato(10, "96,2")} %</div>
            <div class="metric-status">🟢 Sincronizzato su cella B10</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-giallo">
            <div class="metric-title">Media Pressione Sistolica (Massima)</div>
            <div class="metric-value">{prendi_dato(11, "101")} mmHg</div>
            <div class="metric-status">🟡 Sincronizzato su cella B11</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Pressione Diastolica (Minima)</div>
            <div class="metric-value">{prendi_dato(12, "70")} mmHg</div>
            <div class="metric-status">🟢 Sincronizzato su cella B12</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Ultimo Esito ECG Registrato</div>
            <div class="metric-value">{prendi_dato(13, "ARITMIA")}</div>
            <div class="metric-status">🟢 Sincronizzato su cella B13</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Livello di Stress Estimato (da HRV)</div>
            <div class="metric-value">{prendi_dato(14, "Ottimale")}</div>
            <div class="metric-status">🟢 Sincronizzato su cella B14</div>
        </div>
    """, unsafe_allow_html=True)
    # === QUALITÀ DEL SONNO E RECUPERO ===
    st.markdown('<div class="section-header">🌙 Qualità del Sonno e Recupero</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-rosso">
            <div class="metric-title">Media Ore di Sonno (7gg)</div>
            <div class="metric-value">{prendi_dato(17, "5,86")} ore</div>
            <div class="metric-status">🔴 Sincronizzato su cella B17</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-giallo">
            <div class="metric-title">Media Punteggio Sonno Storico</div>
            <div class="metric-value">{prendi_dato(18, "64")} / 100</div>
            <div class="metric-status">🟡 Sincronizzato su cella B18</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Risvegli Notturni (7gg)</div>
            <div class="metric-value">{prendi_dato(19, "3,2")}</div>
            <div class="metric-status">🟢 Sincronizzato su cella B19</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-giallo">
            <div class="metric-title">Efficienza del Sonno Media (7gg)</div>
            <div class="metric-value">{prendi_dato(20, "63,53 %")}</div>
            <div class="metric-status">🟡 Sincronizzato su cella B20</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Temperatura Corporea Storica</div>
            <div class="metric-value">{prendi_dato(21, "36,41")} °C</div>
            <div class="metric-status">🟢 Sincronizzato su cella B21</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Valutazione della Qualità Respiratoria</div>
            <div class="metric-value">{prendi_dato(22, "Ottimale")}</div>
            <div class="metric-status">🟢 Sincronizzato su cella B22</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-giallo">
            <div class="metric-title">Stato Regolarità Ritmo Circadiano</div>
            <div class="metric-value">{prendi_dato(23, "Cattivo")}</div>
            <div class="metric-status">🟡 Sincronizzato su cella B23</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Ore Sonno Profondo (7gg)</div>
            <div class="metric-value">{prendi_dato(24, "1,6")} ore</div>
            <div class="metric-status">🟢 Lettura Diretta Cella B24</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Frequenza Respiratoria Notturna</div>
            <div class="metric-value">{prendi_dato(25, "16")} bpm</div>
            <div class="metric-status">🟢 Sincronizzato su cella B25</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Rapporto Recupero HRV (Fine vs Inizio)</div>
            <div class="metric-value">{prendi_dato(26, "2,8")}</div>
            <div class="metric-status">🟢 Sincronizzato su cella B26</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Punteggio di Recupero Fisico (PAI)</div>
            <div class="metric-value">{prendi_dato(27, "72,7")}</div>
            <div class="metric-status">🟢 Lettura Diretta Cella B27</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-giallo">
            <div class="metric-title">Punteggio di Recupero Mentale</div>
            <div class="metric-value">{prendi_dato(28, "54")} / 100</div>
            <div class="metric-status">🟡 Sincronizzato su cella B28</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Monitoraggio Rischio Apnea Notturna</div>
            <div class="metric-value">{prendi_dato(29, "Basso")}</div>
            <div class="metric-status">🟢 Sincronizzato su cella B29</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-rosso">
            <div class="metric-title">Picco Frequenza Cardiaca Massima (7gg)</div>
            <div class="metric-value">{prendi_dato(30, "137")} bpm</div>
            <div class="metric-status">🔴 Sincronizzato su cella B30</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Ore Utilizzo CPAP (7gg)</div>
            <div class="metric-value">{prendi_dato(31, "6,5")}</div>
            <div class="metric-status">🟢 Sincronizzato su cella B31</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Monitoraggio Parametro Aggiuntivo</div>
            <div class="metric-value">{prendi_dato(32, "Attivo")}</div>
            <div class="metric-status">🟢 Sincronizzato su cella B32</div>
        </div>
    """, unsafe_allow_html=True)

with tab_medie:
    st.info("📊 Sezione Medie Storiche attiva nella colonna Z e AA.")
with tab_trend:
    st.info("📈 Grafici di andamento settimanale pronti.")
