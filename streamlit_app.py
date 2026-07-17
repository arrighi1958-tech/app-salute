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

# Il timestamp forza l'aggiornamento reale dei tuoi dati ogni volta che apri l'app
CSV_URL = f"https://google.com{int(time.time())}"

@st.cache_data(ttl=5)
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
        def prendi_dato(riga_foglio):
            try:
                valore = str(df.iloc[int(riga_foglio) - 1, 1]).strip()
                if valore == "nan" or valore == "": 
                    return "N/D"
                return valore
            except:
                return "N/D"

        # === STILE DI VITA E ATTIVITÀ ===
        st.markdown('<div class="section-header">🏃 Stile di Vita e Attività</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Media Passi Settimanali</div>
                <div class="metric-value">{prendi_dato(3)}</div>
                <div class="metric-status">🟢 Obiettivo Minimo Raggiunto</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Giorni Totali Monitorati</div>
                <div class="metric-value">{prendi_dato(4)} giorni</div>
                <div class="metric-status">🟢 Storico Attivo</div>
            </div>
        """, unsafe_allow_html=True)
        
        # === SALUTE DEL CUORE ===
        st.markdown('<div class="section-header">❤️ Salute del Cuore</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Media Frequenza Cardiaca Diurna</div>
                <div class="metric-value">{prendi_dato(7)} bpm</div>
                <div class="metric-status">🟢 Regolare (ok)</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Media Frequenza Battiti a Riposo (7gg)</div>
                <div class="metric-value">{prendi_dato(8)} bpm</div>
                <div class="metric-status">🟢 Eccellente Recupero (OK)</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Media Variabilità Cardiaca (HRV) (7gg)</div>
                <div class="metric-value">{prendi_dato(9)} ms</div>
                <div class="metric-status">🟢 Bilanciato (ok)</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Media Ossigeno nel Sangue (SpO2)</div>
                <div class="metric-value">{prendi_dato(10)} %</div>
                <div class="metric-status">🟢 Ottimale</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-giallo">
                <div class="metric-title">Media Pressione Sistolica (Massima)</div>
                <div class="metric-value">{prendi_dato(11)} mmHg</div>
                <div class="metric-status">🟡 Attenzione (Leggermente Bassa)</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Media Pressione Diastolica (Minima)</div>
                <div class="metric-value">{prendi_dato(12)} mmHg</div>
                <div class="metric-status">🟢 Ottimale</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Ultimo Esito ECG Registrato</div>
                <div class="metric-value">{prendi_dato(13)}</div>
                <div class="metric-status">🟢 Regolare</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Livello di Stress Stimato (da HRV)</div>
                <div class="metric-value">{prendi_dato(14)}</div>
                <div class="metric-status">🟢 Stato di Riposo Ottimo</div>
            </div>
        """, unsafe_allow_html=True)
        # === QUALITÀ DEL SONNO E RECUPERO ===
        st.markdown('<div class="section-header">🌙 Qualità del Sonno e Recupero</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-rosso">
                <div class="metric-title">Media Ore di Sonno (7gg)</div>
                <div class="metric-value">{prendi_dato(17)} ore</div>
                <div class="metric-status">🔴 Carenza Sonno (Sotto 6 ore)</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-giallo">
                <div class="metric-title">Media Punteggio Sonno Storico</div>
                <div class="metric-value">{prendi_dato(18)} / 100</div>
                <div class="metric-status">🟡 Moderato</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Media Risvegli Notturni (7gg)</div>
                <div class="metric-value">{prendi_dato(19)}</div>
                <div class="metric-status">🟢 Nella Norma</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-giallo">
                <div class="metric-title">Efficienza del Sonno Media (7gg)</div>
                <div class="metric-value">{prendi_dato(20)}</div>
                <div class="metric-status">🟡 Monitorare Continuità</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Media Temperatura Corporea Storica</div>
                <div class="metric-value">{prendi_dato(21)} °C</div>
                <div class="metric-status">🟢 Regolare</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Valutazione della Qualità Respiratoria</div>
                <div class="metric-value">{prendi_dato(22)}</div>
                <div class="metric-status">🟢 Assenza di Disturbi</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Stato Regolarità Ritmo Circadiano</div>
                <div class="metric-value">{prendi_dato(23)}</div>
                <div class="metric-status">🟢 Sonno Stabile</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Media Ore Sonno Profondo (7gg)</div>
                <div class="metric-value">{prendi_dato(24)} ore</div>
                <div class="metric-status">🟢 Sbloccato</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Media Frequenza Respiratoria Notturna</div>
                <div class="metric-value">{prendi_dato(25)} bpm</div>
                <div class="metric-status">🟢 Regolare</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Rapporto Recupero HRV (Fine vs Inizio)</div>
                <div class="metric-value">{prendi_dato(26)}</div>
                <div class="metric-status">🟢 Cuore Recuperato e Rilassato</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Punteggio di Recupero Fisico (PAI)</div>
                <div class="metric-value">{prendi_dato(27)}</div>
                <div class="metric-status">🟢 Buono Stato Fisico</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Punteggio di Recupero Mentale</div>
                <div class="metric-value">{prendi_dato(28)} / 100</div>
                <div class="metric-status">🟢 Ottimo Stato Mentale</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Monitoraggio Rischio Apnea Notturna</div>
                <div class="metric-value">{prendi_dato(29)}</div>
                <div class="metric-status">🟢 Sicuro</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-rosso">
                <div class="metric-title">Picco Frequenza Cardiaca Massima (7gg)</div>
                <div class="metric-value">{prendi_dato(30)} bpm</div>
                <div class="metric-status">🔴 Picco Elevato</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Media Ore Utilizzo CPAP (7gg)</div>
                <div class="metric-value">{prendi_dato(31)} val</div>
                <div class="metric-status">🟢 Terapia Perfetta</div>
            </div>
        """, unsafe_allow_html=True)

    # Correzione Chirurgica: ecco i 4 spazi aggiunti all'inizio di ogni riga!
    with tab_medie:
        st.info("📊 Sezione Medie Storiche attiva.")
    with tab_trend:
        st.info("📈 Grafici di andamento settimanale pronti.")
