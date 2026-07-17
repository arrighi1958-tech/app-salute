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

# Link del tuo Google Fogli pubblicato come CSV
CSV_URL = "https://google.com"

@st.cache_data(ttl=5)
def load_data():
    try:
        url_dinamico = f"{CSV_URL}&cache_bust={int(time.time())}"
        df = pd.read_csv(url_dinamico, header=None)
        return df
    except Exception as e:
        st.sidebar.error(f"Errore di connessione: {e}")
        return None

df = load_data()

st.title("🩺 Cruscotto Salute Renato")
st.write("Sincronizzato in tempo reale con il tuo Google Fogli")

if df is None:
    st.error("⚠️ Attenzione: L'applicazione non riesce a scaricare i dati online dal link di Google Fogli. Controlla che il file sia ancora pubblicato in formato CSV.")

tab_oggi, tab_medie, tab_trend = st.tabs(["Oggi (DATI VIVI)", "Medie Storiche", "Trend"])

with tab_oggi:
    def prendi_dato(riga_foglio, valore_di_prova):
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
            <div class="metric-value">{prendi_dato(3, "8.383")}</div>
            <div class="metric-status">🟢 Obiettivo Raggiunto (Ottimo)</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Giorni Totali Monitorati</div>
            <div class="metric-value">{prendi_dato(4, "12")} giorni</div>
            <div class="metric-status">🟢 Storico Attivo</div>
        </div>
    """, unsafe_allow_html=True)
    
    # === SALUTE DEL CUORE ===
    st.markdown('<div class="section-header">❤️ Salute del Cuore</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Frequenza Cardiaca Diurna</div>
            <div class="metric-value">{prendi_dato(7, "67")} bpm</div>
            <div class="metric-status">🟢 Regolare (ok)</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Frequenza Battiti a Riposo (7gg)</div>
            <div class="metric-value">{prendi_dato(8, "52")} bpm</div>
            <div class="metric-status">🟢 Eccellente Recupero (OK)</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Variabilità Cardiaca (HRV) (7gg)</div>
            <div class="metric-value">{prendi_dato(9, "18")} ms</div>
            <div class="metric-status">🟢 Bilanciato (ok)</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Ossigeno nel Sangue (SpO2)</div>
            <div class="metric-value">{prendi_dato(10, "96,2")} %</div>
            <div class="metric-status">🟢 Ottimale</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-giallo">
            <div class="metric-title">Media Pressione Sistolica (Massima)</div>
            <div class="metric-value">{prendi_dato(11, "101")} mmHg</div>
            <div class="metric-status">🟡 Attenzione (Leggermente Bassa)</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Pressione Diastolica (Minima)</div>
            <div class="metric-value">{prendi_dato(12, "70")} mmHg</div>
            <div class="metric-status">🟢 Ottimale</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Ultimo Esito ECG Registrato</div>
            <div class="metric-value">{prendi_dato(13, "ARITMIA")}</div>
            <div class="metric-status">🟢 Registrato</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Livello di Stress Stimato (da HRV)</div>
            <div class="metric-value">{prendi_dato(14, "Ottimale")}</div>
            <div class="metric-status">🟢 Stato di Riposo Ottimo</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-card bg-rosso">
            <div class="metric-title">Picco Frequenza Cardiaca Massima (7gg)</div>
            <div class="metric-value">{prendi_dato(30, "137")} bpm</div>
            <div class="metric-status">🔴 Monitorare Sforzo</div>
        </div>
    """, unsafe_allow_html=True)
    # === QUALITÀ DEL SONNO E RECUPERO ===
    st.markdown('<div class="section-header">🌙 Qualità del Sonno e Recupero</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-rosso">
            <div class="metric-title">Media Ore di Sonno (7gg)</div>
            <div class="metric-value">{prendi_dato(17, "5,86")} ore</div>
            <div class="metric-status">🔴 Carenza Sonno (Sotto 6 ore)</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Ore Sonno Profondo (7gg)</div>
            <div class="metric-value">{prendi_dato(24, "6,4")} ore</div>
            <div class="metric-status">🟢 Buona quota profonda</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-giallo">
            <div class="metric-title">Media Punteggio Sonno Storico</div>
            <div class="metric-value">{prendi_dato(18, "64")} / 100</div>
            <div class="metric-status">🟡 Moderato</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Risvegli Notturni (7gg)</div>
            <div class="metric-value">{prendi_dato(19, "3,2")}</div>
            <div class="metric-status">🟢 Nella Norma</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-giallo">
            <div class="metric-title">Efficienza del Sonno Media (7gg)</div>
            <div class="metric-value">{prendi_dato(20, "63,53 %")}</div>
            <div class="metric-status">🟡 Monitorare Continuità</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Temperatura Corporea Storica</div>
            <div class="metric-value">{prendi_dato(21, "36,41")} °C</div>
            <div class="metric-status">🟢 Regolare</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Valutazione della Qualità Respiratoria</div>
            <div class="metric-value">{prendi_dato(22, "Ottimale")}</div>
            <div class="metric-status">🟢 Assenza di Disturbi</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Frequenza Respiratoria Media Notturna</div>
            <div class="metric-value">{prendi_dato(25, "16")} apm</div>
            <div class="metric-status">🟢 Regolare</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-giallo">
            <div class="metric-title">Stato Regolarità Ritmo Circadiano</div>
            <div class="metric-value">{prendi_dato(23, "Cattivo")}</div>
            <div class="metric-status">🟡 Da Regolarizzare</div>
        </div>
    """, unsafe_allow_html=True)

    # === MONITORAGGIO TERAPEUTICO E RECUPERO AVANZATO ===
    st.markdown('<div class="section-header">🩺 Monitoraggio Avanzato e Recupero</div>', unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Ore Utilizzo CPAP (7gg)</div>
            <div class="metric-value">{prendi_dato(31, "6,4")} ore</div>
            <div class="metric-status">🟢 Aderenza Terapia Ottima</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Monitoraggio Rischio Apnea Notturna</div>
            <div class="metric-value">{prendi_dato(29, "Basso / Assente")}</div>
            <div class="metric-status">🟢 Sotto Controllo</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Punteggio di Recupero Fisico</div>
            <div class="metric-value">{prendi_dato(27, "121,7")}</div>
            <div class="metric-status">🟢 Ottimo Livello</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-card bg-rosso">
            <div class="metric-title">Punteggio di Recupero Mentale</div>
            <div class="metric-value">{prendi_dato(28, "52")}</div>
            <div class="metric-status">🔴 Stanchezza Accumulata</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Rapporto Recupero HRV (Inizio/Fine Notte)</div>
            <div class="metric-value">{prendi_dato(26, "2,4")}</div>
            <div class="metric-status">🟢 Buon Andamento Vagale</div>
        </div>
    """, unsafe_allow_html=True)

with tab_medie:
    st.subheader("Analisi delle Medie Storiche")
    st.info("In questa sezione verranno inseriti i calcoli aggregati sul lungo periodo.")

with tab_trend:
    st.subheader("Grafici e Trend temporali")
    st.info("In questa sezione potrai visualizzare l'andamento grafico dei tuoi parametri medici.")
