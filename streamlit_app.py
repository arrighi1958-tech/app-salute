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
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 12px;
        border-left: 10px solid #cccccc;
    }
    .metric-title {
        font-size: 15px;
        font-weight: bold;
        color: #444444;
        margin-bottom: 2px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 800;
        color: #111111;
    }
    .metric-status {
        font-size: 12px;
        font-weight: 600;
        margin-top: 2px;
    }
    .section-header {
        font-size: 20px;
        font-weight: bold;
        color: #1A5276;
        margin-top: 25px;
        margin-bottom: 15px;
        border-bottom: 2px solid #1A5276;
        padding-bottom: 5px;
    }
    .clinical-box {
        background-color: #F4F6F7;
        padding: 12px;
        border-radius: 8px;
        border: 1px dashed #1A5276;
        margin-bottom: 15px;
        font-size: 13px;
        color: #2C3E50;
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

st.title("🩺 Cruscotto Salute Renato")
st.markdown('<div class="clinical-box"><strong>Quadro Clinico (68 anni):</strong> Monitoraggio bilanciamento farmaci Ipertensione, Betabloccanti (M/S), Prostata, Anticoagulante.</div>', unsafe_allow_html=True)

# Funzione per estrarre valori in modo sicuro
def ottieni_valore_riep(indice_riga, valore_default):
    try:
        if df_riep is not None:
            valore = str(df_riep.iloc[indice_riga, 1]).strip()
            if valore != "nan" and valore != "" and valore != "None":
                return valore
    except: pass
    return valore_default

# ==================== SEZIONE 1: MEDIE STORICHE E COMPLESSIVE ====================
st.markdown('<div class="section-header">📊 Medie Storiche di Controllo (Orizzonte Complessivo)</div>', unsafe_allow_html=True)

st.markdown(f'<div class="metric-card bg-giallo"><div class="metric-title">Pressione Sistolica Media (Storica)</div><div class="metric-value">{ottieni_valore_riep(10, "102")} mmHg</div><div class="metric-status">Target ottimale stabilità: < 130-140</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Pressione Diastolica Media (Storica)</div><div class="metric-value">{ottieni_valore_riep(11, "70")} mmHg</div><div class="metric-status">Target ottimale stabilità: < 80-85</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Frequenza Cardiaca Media a Riposo</div><div class="metric-value">{ottieni_valore_riep(7, "52")} bpm</div><div class="metric-status">Verifica tolleranza Betabloccante M/S</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-rosso"><div class="metric-title">Media Risvegli Notturni</div><div class="metric-value">{ottieni_valore_riep(18, "3.1")}</div><div class="metric-status">Indice nicturia / disturbi urinari da prostata</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Media Ossigenazione Notturna (SpO2)</div><div class="metric-value">{ottieni_valore_riep(9, "96.2")} %</div><div class="metric-status">Efficacia respiratoria combinata a CPAP</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-blu"><div class="metric-title">Giorni Totali Monitorati nel Report</div><div class="metric-value">{ottieni_valore_riep(3, "18")} giorni</div><div class="metric-status">Ampiezza dello storico dati attuale</div></div>', unsafe_allow_html=True)


# ==================== SEZIONE 2: I 28 PARAMETRI PUNTUALI ====================
st.markdown('<div class="section-header">📋 Elenco Completo dei 28 Parametri Analizzati</div>', unsafe_allow_html=True)

parametri = [
    (2, "Media Passi Settimanali", "bg-verde", "Attività fisica complessiva"),
    (3, "Giorni Monitorati", "bg-blu", "Giorni totali"),
    (4, "Indice Withings Composito", "bg-verde", "Stato calcolato dall'orologio"),
    (5, "Punteggio Sonno", "bg-giallo", "Qualità globale del riposo"),
    (6, "FC Media Sonno", "bg-verde", "Battiti medi notturni"),
    (7, "FC a Riposo", "bg-verde", "Battiti minimi registrati"),
    (8, "HRV Sonno", "bg-blu", "Variabilità frequenza cardiaca"),
    (9, "SpO2 Media Sonno", "bg-verde", "Saturazione ossigeno"),
    (10, "Pressione Sistolica", "bg-giallo", "Pressione massima"),
    (11, "Pressione Diastolica", "bg-verde", "Pressione minima"),
    (12, "Profondità Sonno Giudizio", "bg-blu", "Continuità del sonno"),
    (13, "Sonno REM %", "bg-blu", "Percentuale fase REM"),
    (14, "Sonno Profondo %", "bg-blu", "Percentuale fase profonda"),
    (15, "Interruzioni Notturne Brevi", "bg-rosso", "Micro-risvegli stimate"),
    (16, "HRV Primi 90 Minuti", "bg-verde", "Variabilità inizio sonno"),
    (17, "HRV Ultimi 90 Minuti", "bg-verde", "Variabilità fine sonno"),
    (18, "Risvegli Notturni", "bg-rosso", "Interruzioni prolungate complessive"),
    (19, "Efficienza del Sonno", "bg-giallo", "Percentuale tempo di sonno effettivo"),
    (20, "Temperatura del Sonno", "bg-verde", "Temperatura corporea basale"),
    (21, "Frequenza Respiratoria", "bg-verde", "Atti respiratori al minuto"),
    (22, "Qualità Respiratoria Giudizio", "bg-verde", "Regolarità del respiro"),
    (23, "FC Diurna Media", "bg-giallo", "Battiti medi da sveglio"),
    (24, "FC Diurna Minima", "bg-verde", "Battiti minimi da sveglio"),
    (25, "FC Diurna Massima", "bg-rosso", "Battiti massimi da sveglio"),
    (26, "Ore CPAP", "bg-blu", "Tempo utilizzo ventilatore"),
    (27, "Ore Sonno Profondo (Decimale)", "bg-blu", "Sonno profondo espresso in ore"),
    (28, "Ore CPAP (Decimale)", "bg-blu", "Utilizzo CPAP espresso in ore"),
    (29, "Target Attività Raggiunto", "bg-verde", "Raggiungimento obiettivo passi")
]

for riga, titolo, colore, nota in parametri:
    valore_mostrato = ottieni_valore_riep(riga, "--")
    st.markdown(f'''
        <div class="metric-card {colore}">
            <div class="metric-title">{titolo}</div>
            <div class="metric-value">{valore_mostrato}</div>
            <div class="metric-status">{nota}</div>
        </div>
    ''', unsafe_allow_html=True)


# ==================== SEZIONE 3: ANDAMENTI CRONOLOGICI ====================
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

    pulisci_e_grafica('sistole', '🩺 Trend Pressione Massima (Sistole)', '#E74C3C')
    pulisci_e_grafica('diastole', '🩺 Trend Pressione Minima (Diastole)', '#3498DB')
    pulisci_e_grafica('FC a riposo', '❤️ Trend Frequenza Cardiaca a Riposo', '#2ECC71')
    pulisci_e_grafica('frequenza respiratoria', '🫁 Frequenza Respiratoria Notturna', '#9B59B6')
    pulisci_e_grafica('SpO2 media durante il sonno', '🩸 Saturazione Ossigeno Notturna', '#F1C40F')
    pulisci_e_grafica('temperatura del sonno', '🌡️ Temperatura Basale Notturna', '#E67E22')
    pulisci_e_grafica('Ore_CPAP', '💨 Utilizzo CPAP (Ore)', '#1ABC9C')
    pulisci_e_grafica('passi', '🏃 Conteggio Passi Giornalieri', '#34495E')
