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

# URL DEL TUO GOOGLE FOGLIO CON AGGIUNTA DI TIMESTAMP DINAMICO PER FORZARE L'AGGIORNAMENTO
BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTPoEryjtZvVcaBEvSkgfh7qaeYXUJEmmDcZJh6fzBMZz80v1p7M009sdIVicHuI-Lj6AmC6SdWWsDj/pub?gid=0&single=true&output=csv"
CSV_URL = f"{BASE_URL}&cache_bypass={int(time.time())}"

@st.cache_data(ttl=5)  # Controlla gli aggiornamenti sul foglio ogni 5 secondi
def load_data():
    try:
        return pd.read_csv(CSV_URL, header=None)
    except Exception as e:
        return None

df = load_data()

st.title("🩺 Cruscotto Salute Renato (PIPPO)")
st.write("Sincronizzato in tempo reale con il tuo Google Fogli")

if df is None:
    st.error("⚠️ Impossibile collegarsi al Foglio Google. Verifica la tua connessione o la pubblicazione del link.")

tab_oggi, tab_medie, tab_trend = st.tabs(["Oggi (DATI VIVI)", "Medie Storiche", "Trend"])

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
    
    # === SALUTE DEL CUORE ===
    st.markdown('<div class="section-header">❤️ Salute del Cuore</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">ℹ️ INDICE WITHINGS COMPOSITO</div>
            <div class="metric-value">{prendi_riga_dinamica(5, "Cardio Ottimale")}</div>
            <div class="metric-status">🟢 Dinamico su cella B5</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Frequenza Cardiaca Diurna</div>
            <div class="metric-value">{prendi_riga_dinamica(7, "67")} bpm</div>
            <div class="metric-status">🟢 Dinamico su cella B7</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Frequenza Battiti a Riposo (7gg)</div>
            <div class="metric-value">{prendi_riga_dinamica(8, "52")} bpm</div>
            <div class="metric-status">🟢 Dinamico su cella B8</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Variabilità Cardiaca (HRV) (7gg)</div>
            <div class="metric-value">{prendi_riga_dinamica(9, "18")} ms</div>
            <div class="metric-status">🟢 Dinamico su cella B9</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Ossigeno nel Sangue (SpO2)</div>
            <div class="metric-value">{prendi_riga_dinamica(10, "96,2")} %</div>
            <div class="metric-status">🟢 Dinamico su cella B10</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-giallo">
            <div class="metric-title">Media Pressione Sistolica (Massima)</div>
            <div class="metric-value">{prendi_riga_dinamica(11, "101")} mmHg</div>
            <div class="metric-status">🟡 Dinamico su cella B11</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Pressione Diastolica (Minima)</div>
            <div class="metric-value">{prendi_riga_dinamica(12, "70")} mmHg</div>
            <div class="metric-status">🟢 Dinamico su cella B12</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Ultimo Esito ECG Registrato</div>
            <div class="metric-value">{prendi_riga_dinamica(13, "ARITMIA")}</div>
            <div class="metric-status">🟢 Dinamico su cella B13</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Livello di Stress Estimato (da HRV)</div>
            <div class="metric-value">{prendi_riga_dinamica(14, "Ottimale")}</div>
            <div class="metric-status">🟢 Dinamico su cella B14</div>
        </div>
    """, unsafe_allow_html=True)

    # === QUALITÀ DEL SONNO E RECUPERO ===
    st.markdown('<div class="section-header">🌙 Qualità del Sonno e Recupero</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-rosso">
            <div class="metric-title">Media Ore di Sonno (7gg)</div>
            <div class="metric-value">{prendi_riga_dinamica(17, "5,86")} ore</div>
            <div class="metric-status">🔴 Dinamico su cella B17</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-giallo">
            <div class="metric-title">Media Punteggio Sonno Storico</div>
            <div class="metric-value">{prendi_riga_dinamica(18, "64")} / 100</div>
            <div class="metric-status">🟡 Dinamico su cella B18</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Risvegli Notturni (7gg)</div>
            <div class="metric-value">{prendi_riga_dinamica(19, "3,2")}</div>
            <div class="metric-status">🟢 Dinamico su cella B19</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-giallo">
            <div class="metric-title">Efficienza del Sonno Media (7gg)</div>
            <div class="metric-value">{prendi_riga_dinamica(20, "63,53 %")}</div>
            <div class="metric-status">🟡 Dinamico su cella B20</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Temperatura Corporea Storica</div>
            <div class="metric-value">{prendi_riga_dinamica(21, "36,41")} °C</div>
            <div class="metric-status">🟢 Dinamico su cella B21</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Valutazione della Qualità Respiratoria</div>
            <div class="metric-value">{prendi_riga_dinamica(22, "Ottimale")}</div>
            <div class="metric-status">🟢 Dinamico su cella B22</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-giallo">
            <div class="metric-title">Stato Regolarità Ritmo Circadiano</div>
            <div class="metric-value">{prendi_riga_dinamica(23, "Cattivo")}</div>
            <div class="metric-status">🟡 Dinamico su cella B23</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Ore Sonno Profondo (7gg)</div>
            <div class="metric-value">{prendi_riga_dinamica(24, "1,6")} ore</div>
            <div class="metric-status">🟢 Dinamico su cella B24</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Frequenza Respiratoria Notturna</div>
            <div class="metric-value">{prendi_riga_dinamica(25, "16")} bpm</div>
            <div class="metric-status">🟢 Dinamico su cella B25</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Rapporto Recupero HRV (Fine vs Inizio)</div>
            <div class="metric-value">{prendi_riga_dinamica(26, "2,8")}</div>
            <div class="metric-status">🟢 Dinamico su cella B26</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Punteggio di Recupero Fisico (PAI)</div>
            <div class="metric-value">{prendi_riga_dinamica(27, "72,7")}</div>
            <div class="metric-status">🟢 Dinamico su cella B27</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-giallo">
            <div class="metric-title">Punteggio di Recupero Mentale</div>
            <div class="metric-value">{prendi_riga_dinamica(28, "54")} / 100</div>
            <div class="metric-status">🟡 Dinamico su cella B28</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Monitoraggio Rischio Apnea Notturna</div>
            <div class="metric-value">{prendi_riga_dinamica(29, "Basso")}</div>
            <div class="metric-status">🟢 Dinamico su cella B29</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-rosso">
            <div class="metric-title">Picco Frequenza Cardiaca Massima (7gg)</div>
            <div class="metric-value">{prendi_riga_dinamica(30, "137")} bpm</div>
            <div class="metric-status">🔴 Dinamico su cella B30</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Ore Utilizzo CPAP (7gg)</div>
            <div class="metric-value">{prendi_riga_dinamica(31, "6,5")}</div>
            <div class="metric-status">🟢 Dinamico su cella B31</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Monitoraggio Parametro Aggiuntivo</div>
            <div class="metric-value">{prendi_riga_dinamica(32, "Attivo")}</div>
            <div class="metric-status">🟢 Dinamico su cella B32</div>
        </div>
    """, unsafe_allow_html=True)

with tab_medie:
    st.markdown('<div class="section-header">📊 Le Tue Medie Storiche Complessive</div>', unsafe_allow_html=True)
    st.write("Valori medi calcolati analizzando l'intero storico dei tuoi giorni registrati.")

    if df is not None:
        try:
            media_passi = int(pd.to_numeric(df.iloc[1:, 23], errors='coerce').mean())
            media_sonno = int(pd.to_numeric(df.iloc[1:, 1], errors='coerce').mean())
            media_sistole = int(pd.to_numeric(df.iloc[1:, 19], errors='coerce').mean())
            media_diastole = int(pd.to_numeric(df.iloc[1:, 20], errors='coerce').mean())
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                    <div class="metric-card bg-verde">
                        <div class="metric-title">Media Passi Storica</div>
                        <div class="metric-value">{media_passi:,}</div>
                        <div class="metric-status">🏃 Passi medi al giorno</div>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class="metric-card bg-giallo">
                        <div class="metric-title">Media Pressione Massima</div>
                        <div class="metric-value">{media_sistole} mmHg</div>
                        <div class="metric-status">🩺 Sistolica media</div>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                    <div class="metric-card bg-verde">
                        <div class="metric-title">Media Punteggio Sonno</div>
                        <div class="metric-value">{media_sonno} / 100</div>
                        <div class="metric-status">🌙 Qualità del riposo media</div>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class="metric-card bg-verde">
                        <div class="metric-title">Media Pressione Minima</div>
                        <div class="metric-value">{media_diastole} mmHg</div>
                        <div class="metric-status">🩺 Diastolica media</div>
                    </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.warning("Nota: Verifica i dati sul foglio.")

with tab_trend:
    st.markdown('<div class="section-header">📈 Trend e Andamento Temporale</div>', unsafe_allow_html=True)
    
    if df is not None:
        try:
            df_trend = pd.DataFrame({
                'Data': df.iloc[1:, 0].astype(str),
                'Passi': pd.to_numeric(df.iloc[1:, 23], errors='coerce'),
                'Punteggio Sonno': pd.to_numeric(df.iloc[1:, 1], errors='coerce'),
                'Sistole (Massima)': pd.to_numeric(df.iloc[1:, 19], errors='coerce'),
                'Diastole (Minima)': pd.to_numeric(df.iloc[1:, 20], errors='coerce')
            }).dropna()
            
            st.subheader("🏃 Andamento Passi Giornalieri")
            st.line_chart(df_trend, x='Data', y='Passi', color="#2ECC71")
            
            st.subheader("🌙 Evoluzione Qualità del Sonno")
            st.line_chart(df_trend, x='Data', y='Punteggio Sonno', color="#1A5276")
            
            st.subheader("🩺 Andamento Pressione Arteriosa")
            st.line_chart(df_trend, x='Data', y=['Sistole (Massima)', 'Diastole (Minima)'], color=["#E74C3C", "#F1C40F"])
            
        except Exception as e:
            st.error(f"Errore nella generazione dei grafici: {e}")
