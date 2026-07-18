import streamlit as st
import pandas as pd
import time
import plotly.express as px

# CONFIGURAZIONE GENERALE
st.set_page_config(page_title="Pannello Salute Renato", page_icon="🩺", layout="wide")

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
        font-size: 18px;
        font-weight: bold;
        color: #333333;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 34px;
        font-weight: 800;
        color: #111111;
    }
    .metric-status {
        font-size: 14px;
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
    .bg-blu { border-left-color: #3498DB !important; color: #2980B9; }
    </style>
""", unsafe_allow_html=True)

# URL DEI DUE FOGLI GOOGLE
URL_RIEPILOGO = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTPoEryjtZvVcaBEvSkgfh7qaeYXUJEmmDcZJh6fzBMZz80v1p7M009sdIVicHuI-Lj6AmC6SdWWsDj/pub?gid=0&single=true&output=csv"
URL_CRONOLOGIA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTPoEryjtZvVcaBEvSkgfh7qaeYXUJEmmDcZJh6fzBMZz80v1p7M009sdIVicHuI-Lj6AmC6SdWWsDj/pub?gid=320500951&single=true&output=csv"

# Bypass della cache
timestamp = int(time.time())
CSV_RIEPILOGO = f"{URL_RIEPILOGO}&cache_bypass={timestamp}"
CSV_CRONOLOGIA = f"{URL_CRONOLOGIA}&cache_bypass={timestamp}"

@st.cache_data(ttl=5)
def load_riepilogo():
    try: return pd.read_csv(CSV_RIEPILOGO, header=None)
    except: return None

@st.cache_data(ttl=5)
def load_cronologia():
    try:
        # Carichiamo usando la prima riga come intestazione (nomi colonne)
        df_cron = pd.read_csv(CSV_CRONOLOGIA)
        # Pulizia della data
        df_cron.iloc[:, 0] = pd.to_datetime(df_cron.iloc[:, 0], errors='coerce')
        df_cron = df_cron.dropna(subset=[df_cron.columns[0]])
        df_cron = df_cron.sort_values(by=df_cron.columns[0])
        return df_cron
    except:
        return None

df_riep = load_riepilogo()
df_cron = load_cronologia()

st.title("🩺 Cruscotto Medico Avanzato - Renato")
st.write("Analisi integrata Withings ScanWatch 2 e Storico Clinico")

if df_riep is None or df_cron is None:
    st.error("⚠️ Errore nel caricamento dei dati da uno dei fogli. Verifica la pubblicazione sul web.")

# Funzione per estrarre valori dal foglio riepilogo
def ottieni_valore_riep(indice_riga, valore_default):
    try:
        if df_riep is not None:
            valore = str(df_riep.iloc[indice_riga, 1]).strip()
            if valore != "nan" and valore != "" and valore != "None":
                return valore
    except: pass
    return valore_default

tab_oggi, tab_storico, tab_grafici = st.tabs(["📋 Valori Odierni e Medie", "📊 Quadro Clinico Completo", "📈 Grafici di Tendenza"])

with tab_oggi:
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-header">🏃 Attività e Stile di Vita</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Media Passi Settimanali</div><div class="metric-value">{ottieni_valore_riep(2, "5.657")}</div><div class="metric-status">Livello movimento attivo</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card bg-blu"><div class="metric-title">Giorni Monitorati</div><div class="metric-value">{ottieni_valore_riep(3, "18")} giorni</div><div class="metric-status">Storico totale registrato</div></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="section-header">❤️ Stato Cardiovascolare</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Stato Withings Composito</div><div class="metric-value">{ottieni_valore_riep(4, "Cardio Ottimale")}</div><div class="metric-status">Valutazione complessiva orologio</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Frequenza Cardiaca Diurna</div><div class="metric-value">{ottieni_valore_riep(6, "67")} bpm</div><div class="metric-status">Frequenza media da sveglio</div></div>', unsafe_allow_html=True)

with tab_storico:
    st.markdown('<div class="section-header">🩺 Indicatori per il Medico Curante / Specialista</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('### 🩸 Area Ipertensione e Farmaci')
        st.markdown(f'<div class="metric-card bg-giallo"><div class="metric-title">Pressione Sistolica Media</div><div class="metric-value">{ottieni_valore_riep(10, "101")} mmHg</div><div class="metric-status">Target ottimale a riposo: < 130-140</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Pressione Diastolica Media</div><div class="metric-value">{ottieni_valore_riep(11, "70")} mmHg</div><div class="metric-status">Target ottimale a riposo: < 80-85</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Frequenza Cardiaca a Riposo</div><div class="metric-value">{ottieni_valore_riep(7, "52")} bpm</div><div class="metric-status">Stabilità da effetto Betabloccante</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Variabilità Cardiaca (HRV)</div><div class="metric-value">{ottieni_valore_riep(8, "18")} ms</div><div class="metric-status">Equilibrio del sistema nervoso autonomo</div></div>', unsafe_allow_html=True)

    with col2:
        st.markdown('### 🌙 Area Sonno, Prostata e Respiro')
        st.markdown(f'<div class="metric-card bg-rosso"><div class="metric-title">Risvegli Notturni Medi</div><div class="metric-value">{ottieni_valore_riep(18, "3.2")}</div><div class="metric-status">Frequenza nicturia / disturbi della prostata</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card bg-giallo"><div class="metric-title">Efficienza del Sonno</div><div class="metric-value">{ottieni_valore_riep(19, "63.53 %")}</div><div class="metric-status">Continuità e qualità del riposo</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Saturazione Ossigeno (SpO2)</div><div class="metric-value">{ottieni_valore_riep(9, "96.2")} %</div><div class="metric-status">Ossigenazione media notturna</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Temperatura del Sonno</div><div class="metric-value">{ottieni_valore_riep(20, "36.41")} °C</div><div class="metric-status">Stabilità termica basale</div></div>', unsafe_allow_html=True)

with tab_grafici:
    st.markdown('<div class="section-header">📈 Trend Temporali (Dati Cronologici ScanWatch)</div>', unsafe_allow_html=True)
    
    if df_cron is not None:
        # Pulizia colonne per grafici (conversione in numerico dei dati utili)
        data_col = df_cron.columns[0]
        
        def pulisci_e_grafica(nome_colonna, titolo_grafico, colore_linea):
            if nome_colonna in df_cron.columns:
                df_cron[nome_colonna] = pd.to_numeric(df_cron[nome_colonna].astype(str).str.replace(',', '.'), errors='coerce')
                df_valido = df_cron.dropna(subset=[nome_colonna])
                if not df_valido.empty:
                    fig = px.line(df_valido, x=data_col, y=nome_colonna, title=titolo_grafico,
                                  labels={data_col: 'Data', nome_colonna: 'Valore'},
                                  markers=True, color_discrete_sequence=[colore_linea])
                    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(f"Dati non sufficienti per mostrare il grafico di: {nome_colonna}")
            else:
                st.warning(f"Colonna '{nome_colonna}' non trovata nel foglio.")

        # Grafici affiancati o in sequenza
        pulisci_e_grafica('sistole', '🩺 Andamento Pressione Massima (Sistole)', '#E74C3C')
        pulisci_e_grafica('diastole', '🩺 Andamento Pressione Minima (Diastole)', '#3498DB')
        pulisci_e_grafica('FC a riposo', '❤️ Andamento Frequenza Cardiaca a Riposo', '#2ECC71')
        pulisci_e_grafica('frequenza respiratoria', '🫁 Frequenza Respiratoria Notturna (BRPM)', '#9B59B6')
        pulisci_e_grafica('SpO2 media durante il sonno', '🩸 Saturazione Ossigeno Notturna (SpO2)', '#F1C40F')
        pulisci_e_grafica('temperatura del sonno', '🌡️ Variazione Temperatura Basale Notturna', '#E67E22')
        pulisci_e_grafica('Ore_CPAP', '💨 Utilizzo CPAP (Ore)', '#1ABC9C')
        pulisci_e_grafica('passi', '🏃 Conteggio Passi Giornalieri', '#34495E')
    else:
        st.info("Caricamento del trend cronologico in corso...")
