import streamlit as st
import pandas as pd
import time
import plotly.express as px

# CONFIGURAZIONE GENERALE (Ottimizzata per cellulare)
st.set_page_config(page_title="Pannello Salute Renato", page_icon="🩺", layout="centered")

# STILI CSS PERSONALIZZATI
st.markdown("""
    <style>
    .metric-card {
        background-color: #ffffff;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 12px;
        border-left: 10px solid #cccccc;
    }
    .metric-title {
        font-size: 16px;
        font-weight: bold;
        color: #444444;
        margin-bottom: 2px;
    }
    .metric-value {
        font-size: 30px;
        font-weight: 800;
        color: #111111;
    }
    .metric-status {
        font-size: 13px;
        font-weight: 600;
        margin-top: 2px;
    }
    .section-header {
        font-size: 22px;
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
        df_cron = pd.read_csv(CSV_CRONOLOGIA)
        df_cron.iloc[:, 0] = pd.to_datetime(df_cron.iloc[:, 0], errors='coerce')
        df_cron = df_cron.dropna(subset=[df_cron.columns[0]])
        df_cron = df_cron.sort_values(by=df_cron.columns[0])
        return df_cron
    except: return None

df_riep = load_riepilogo()
df_cron = load_cronologia()

st.title("🩺 Cruscotto Salute Renato (PIPPO)")
st.write("Vista unica continua ottimizzata per cellulare")

# Controllo separato e meno invasivo
if df_riep is None:
    st.warning("⚠️ Impossibile aggiornare i dati in tempo reale. Mostro i dati memorizzati.")

# Funzione per estrarre valori dal foglio riepilogo
def ottieni_valore_riep(indice_riga, valore_default):
    try:
        if df_riep is not None:
            valore = str(df_riep.iloc[indice_riga, 1]).strip()
            if valore != "nan" and valore != "" and valore != "None":
                return valore
    except: pass
    return valore_default

# ==================== 1. VISTA GENERALE E MEDIE INDICI ====================
st.markdown('<div class="section-header">📋 Riepilogo Attività e Stato Generale</div>', unsafe_allow_html=True)

st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Media Passi Settimanali</div><div class="metric-value">{ottieni_valore_riep(2, "5.657")}</div><div class="metric-status">Livello di attività</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-blu"><div class="metric-title">Giorni Totali Monitorati</div><div class="metric-value">{ottieni_valore_riep(3, "18")} giorni</div><div class="metric-status">Conteggio complessivo</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">ℹ️ INDICE WITHINGS COMPOSITO</div><div class="metric-value">{ottieni_valore_riep(4, "Cardio Ottimale")}</div><div class="metric-status">Stato di salute generale</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Media Frequenza Cardiaca Diurna</div><div class="metric-value">{ottieni_valore_riep(6, "67")} bpm</div><div class="metric-status">Durante le ore di veglia</div></div>', unsafe_allow_html=True)

# ==================== 2. IL QUADRO CLINICO DETTAGLIATO ====================
st.markdown('<div class="section-header">🩸 Area Monitoraggio Farmaci (Ipertensione e Betabloccanti)</div>', unsafe_allow_html=True)

st.markdown(f'<div class="metric-card bg-giallo"><div class="metric-title">Pressione Sistolica Media</div><div class="metric-value">{ottieni_valore_riep(10, "102")} mmHg</div><div class="metric-status">Media Storica Massima (Target < 130-140)</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Pressione Diastolica Media</div><div class="metric-value">{ottieni_valore_riep(11, "70")} mmHg</div><div class="metric-status">Media Storica Minima (Target < 80-85)</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Media Frequenza Battiti a Riposo</div><div class="metric-value">{ottieni_valore_riep(7, "52")} bpm</div><div class="metric-status">Effetto Betabloccante stabile</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Media Variabilità Cardiaca (HRV)</div><div class="metric-value">{ottieni_valore_riep(8, "18")} ms</div><div class="metric-status">Recupero e stress cardiaco</div></div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">🌙 Area Sonno, Prostata e Respiro</div>', unsafe_allow_html=True)

st.markdown(f'<div class="metric-card bg-rosso"><div class="metric-title">Risvegli Notturni Medi</div><div class="metric-value">{ottieni_valore_riep(18, "3.1")}</div><div class="metric-status">Indicatore disturbi (es. Prostata/Nicturia)</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-giallo"><div class="metric-title">Efficienza del Sonno</div><div class="metric-value">{ottieni_valore_riep(19, "63.67 %")}</div><div class="metric-status">Qualità del sonno continuo</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Media Ossigeno nel Sangue (SpO2)</div><div class="metric-value">{ottieni_valore_riep(9, "96.2")} %</div><div class="metric-status">Saturazione ossigeno notturna</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Temperatura del Sonno</div><div class="metric-value">{ottieni_valore_riep(20, "36.4")} °C</div><div class="metric-status">Media basale notturna</div></div>', unsafe_allow_html=True)


# ==================== 3. GRAFICI CRONOLOGICI CONTINUI ====================
st.markdown('<div class="section-header">📈 Grafici di Tendenza Temporale</div>', unsafe_allow_html=True)

if df_cron is not None:
    data_col = df_cron.columns[0]
    
    def pulisci_e_grafica(nome_colonna, titolo_grafico, colore_linea):
        if nome_colonna in df_cron.columns:
            df_cron[nome_colonna] = pd.to_numeric(df_cron[nome_colonna].astype(str).str.replace(',', '.'), errors='coerce')
            df_valido = df_cron.dropna(subset=[nome_colonna])
            if not df_valido.empty:
                fig = px.line(df_valido, x=data_col, y=nome_colonna, title=titolo_grafico,
                              labels={data_col: 'Data', nome_colonna: 'Valore'},
                              markers=True, color_discrete_sequence=[colore_linea])
                fig.update_layout(height=280, margin=dict(l=10, r=10, t=40, b=10))
                st.plotly_chart(fig, use_container_width=True)

    # Elenco sequenziale dei grafici per lo scorrimento
    pulisci_e_grafica('sistole', '🩺 Trend Pressione Massima (Sistole)', '#E74C3C')
    pulisci_e_grafica('diastole', '🩺 Trend Pressione Minima (Diastole)', '#3498DB')
    pulisci_e_grafica('FC a riposo', '❤️ Trend Frequenza Cardiaca a Riposo', '#2ECC71')
    pulisci_e_grafica('frequenza respiratoria', '🫁 Frequenza Respiratoria Notturna', '#9B59B6')
    pulisci_e_grafica('SpO2 media durante il sonno', '🩸 Saturazione Ossigeno Notturna', '#F1C40F')
    pulisci_e_grafica('temperatura del sonno', '🌡️ Temperatura Basale Notturna', '#E67E22')
    pulisci_e_grafica('Ore_CPAP', '💨 Utilizzo CPAP (Ore)', '#1ABC9C')
    pulisci_e_grafica('passi', '🏃 Conteggio Passi Giornalieri', '#34495E')
else:
    st.info("ℹ️ I grafici storici saranno visibili non appena il foglio cronologico avrà completato il caricamento.")
