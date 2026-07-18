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
st.write("Vista panoramica totale ottimizzata per scorrimento verticale")

# Funzione per estrarre valori in modo sicuro
def ottieni_valore_riep(indice_riga, valore_default):
    try:
        if df_riep is not None:
            valore = str(df_riep.iloc[indice_riga, 1]).strip()
            if valore != "nan" and valore != "" and valore != "None":
                return valore
    except: pass
    return valore_default

# ==================== SEZIONE 1: VISTA MEDICA DI SINTESI ====================
st.markdown('<div class="section-header">🩺 Indicatori Principali per il Medico</div>', unsafe_allow_html=True)

st.markdown(f'<div class="metric-card bg-giallo"><div class="metric-title">Pressione Sistolica Media</div><div class="metric-value">{ottieni_valore_riep(10, "102")} mmHg</div><div class="metric-status">Target ottimale a riposo: < 130-140</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Pressione Diastolica Media</div><div class="metric-value">{ottieni_valore_riep(11, "70")} mmHg</div><div class="metric-status">Target ottimale a riposo: < 80-85</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Frequenza Cardiaca a Riposo</div><div class="metric-value">{ottieni_valore_riep(7, "52")} bpm</div><div class="metric-status">Stabilità da effetto Betabloccante</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-rosso"><div class="metric-title">Risvegli Notturni Medi</div><div class="metric-value">{ottieni_valore_riep(18, "3.1")}</div><div class="metric-status">Frequenza nicturia / disturbi della prostata</div></div>', unsafe_allow_html=True)

# ==================== SEZIONE 2: TUTTI I 28 PARAMETRI IN SEQUENZA ====================
st.markdown('<div class="section-header">📊 Elenco Completo dei parametri monitorati</div>', unsafe_allow_html=True)

# Mappa dinamica basata sulle righe del tuo file excel
parametri = [
    (2, "Media Passi Settimanali", "bg-verde", "Passi medi registrati"),
    (3, "Giorni Monitorati", "bg-blu", "Giorni totali storici"),
    (4, "Indice Withings Composito", "bg-verde", "Valutazione automatica orologio"),
    (5, "Punteggio Qualità del Sonno", "bg-giallo", "Valutazione riposo"),
    (6, "FC Media Durante il Sonno", "bg-verde", "Frequenza cardiaca notturna"),
    (7, "FC a Riposo", "bg-verde", "Minimo battiti registrato"),
    (8, "HRV Durante il Sonno", "bg-blu", "Variabilità della frequenza cardiaca"),
    (9, "SpO2 Media Durante il Sonno", "bg-verde", "Saturazione ossigeno"),
    (10, "Pressione Sistolica (Massima)", "bg-giallo", "Valore medio registrato"),
    (11, "Pressione Diastolica (Minima)", "bg-verde", "Valore medio registrato"),
    (12, "Profondità del Sonno Giudizio", "bg-blu", "Giudizio continuità riposo"),
    (13, "Profondità Sonno REM", "bg-blu", "Fase REM del sonno"),
    (14, "Profondità del Sonno", "bg-blu", "Sonno profondo complessivo"),
    (15, "Interruzioni Notturne", "bg-rosso", "Numero microrisvegli"),
    (16, "Variabilità FC Media (Primi 90 min)", "bg-verde", "Finestra iniziale sonno"),
    (17, "Variabilità FC Media (Ultimi 90 min)", "bg-verde", "Finestra finale sonno"),
    (18, "Risvegli Notturni", "bg-rosso", "Interruzioni stimate"),
    (19, "Efficienza del Sonno", "bg-giallo", "Percentuale tempo di riposo reale"),
    (20, "Temperatura del Sonno", "bg-verde", "Stabilità termica corporea"),
    (21, "Frequenza Respiratoria", "bg-verde", "Attività polmonare (BRPM)"),
    (22, "Valutazione Qualità Respiratoria", "bg-verde", "Regolarità del respiro notturno"),
    (23, "FC Tempo Medio Sveglio", "bg-giallo", "Battiti medi diurni"),
    (24, "FC Tempo Medio Sveglio Minima", "bg-verde", "Battiti minimi diurni"),
    (25, "FC Tempo Medio Sveglio Massima", "bg-rosso", "Battiti massimi diurni"),
    (26, "Ore CPAP", "bg-blu", "Tempo di utilizzo della ventilazione"),
    (27, "Sonno Profondo Decimale", "bg-blu", "Ore di sonno profondo"),
    (28, "CPAP Decimale", "bg-blu", "Ore CPAP in formato decimale"),
    (29, "Raggiungimento Obiettivi Attività", "bg-verde", "Target passi quotidiani")
]

# Ciclo automatico per stampare tutti i blocchi richiesti
for riga, titolo, colore, nota in parametri:
    valore_mostrato = ottieni_valore_riep(riga, "Dato non presente")
    st.markdown(f'''
        <div class="metric-card {colore}">
            <div class="metric-title">{titolo}</div>
            <div class="metric-value">{valore_mostrato}</div>
            <div class="metric-status">{nota}</div>
        </div>
    ''', unsafe_allow_html=True)

# ==================== SEZIONE 3: I GRAFICI CRONOLOGICI ====================
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
