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
    
    /* Stile speciale per il Punteggio in cima */
    .punteggio-card {
        background-color: #fcfcfc;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        text-align: center;
        border: 3px solid #cccccc;
    }
    .punteggio-title {
        font-size: 18px;
        font-weight: bold;
        color: #333333;
    }
    .punteggio-value {
        font-size: 42px;
        font-weight: 900;
    }
    .border-verde { border-color: #2ECC71 !important; color: #27AE60; }
    .border-giallo { border-color: #F1C40F !important; color: #D4AC0D; }
    .border-rosso { border-color: #E74C3C !important; color: #C0392B; }
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
st.markdown('<div class="clinical-box"><strong>Quadro Clinico (68 anni):</strong> Monitoraggio bilanciamento farmaci Ipertensione, Betabloccanti (M/S), Prostata, Anticoagulante permanente. Soglia minima FC impostata per controllo Bradicardia.</div>', unsafe_allow_html=True)

# Funzione per estrarre valori in modo sicuro
def ottieni_valore_riep(riga_excel, valore_default):
    try:
        if df_riep is not None:
            indice_python = riga_excel - 1
            valore = str(df_riep.iloc[indice_python, 1]).strip()
            if valore != "nan" and valore != "" and valore != "None":
                return valore
    except: pass
    return valore_default

# ==================== NUOVO: PUNTEGGIO DI SALUTE ODIERNO (CELLA B5) ====================
punteggio_val = ottieni_valore_riep(5, "70,0")

# Logica di colorazione dinamica (Verde, Giallo, Rosso) basata sulla formattazione condizionale
classe_punteggio = "border-giallo"
try:
    punteggio_num = float(punteggio_val.replace(',', '.'))
    if punteggio_num >= 70.0:
        classe_punteggio = "border-verde"
    elif punteggio_num <= 30.0:
        classe_punteggio = "border-rosso"
except: pass

st.markdown(f'''
    <div class="punteggio-card {classe_punteggio}">
        <div class="punteggio-title">🎯 PUNTEGGIO DI SALUTE ODIERNO</div>
        <div class="punteggio-value">{punteggio_val} <span style="font-size:20px; font-weight:500; color:#666;">/ 100</span></div>
        <div style="font-size: 12px; margin-top: 5px; font-weight: bold;">Indice generale calcolato dall'ultimo inserimento dati</div>
    </div>
''', unsafe_allow_html=True)


# ==================== SEZIONE 1: MEDIE STORICHE DI CONTROLLO ====================
st.markdown('<div class="section-header">📊 Medie Storiche di Controllo (Orizzonte Complessivo)</div>', unsafe_allow_html=True)

st.markdown(f'<div class="metric-card bg-giallo"><div class="metric-title">Pressione Sistolica Media (Storica)</div><div class="metric-value">{ottieni_valore_riep(11, "102")} mmHg</div><div class="metric-status">Target ottimale stabilità: < 130-140</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Pressione Diastolica Media (Storica)</div><div class="metric-value">{ottieni_valore_riep(12, "70")} mmHg</div><div class="metric-status">Target ottimale stabilità: < 80-85</div></div>', unsafe_allow_html=True)

# Controllo dinamico colore FC a Riposo per Bradicardia
fc_riposo_val = ottieni_valore_riep(8, "52")
colore_fc = "bg-verde"
nota_fc = "Verifica tolleranza Betabloccante M/S"
try:
    fc_num = float(fc_riposo_val.replace(',', '.'))
    if fc_num < 48:
        colore_fc = "bg-rosso"
        nota_fc = "⚠️ ATTENZIONE: Frequenza bassa (Possibile Bradicardia da Betabloccante)"
except: pass

st.markdown(f'<div class="metric-card {colore_fc}"><div class="metric-title">Frequenza Cardiaca Media a Riposo (7gg)</div><div class="metric-value">{fc_riposo_val} bpm</div><div class="metric-status">{nota_fc}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-rosso"><div class="metric-title">Media Risvegli Notturni (7gg)</div><div class="metric-value">{ottieni_valore_riep(19, "3,1")}</div><div class="metric-status">Indice nicturia / disturbi urinari da prostata</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Media Ossigenazione Notturna (SpO2)</div><div class="metric-value">{ottieni_valore_riep(10, "96,2")} %</div><div class="metric-status">Efficacia respiratoria combinata a CPAP</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-blu"><div class="metric-title">Numero Giorni Analizzati</div><div class="metric-value">{ottieni_valore_riep(4, "18")} giorni</div><div class="metric-status">Ampiezza dello storico dati attuale</div></div>', unsafe_allow_html=True)


# ==================== SEZIONE 2: I PARAMETRI REALI DIRETTI (28 INDICI) ====================
st.markdown('<div class="section-header">📋 Elenco Completo dei Parametri Analizzati</div>', unsafe_allow_html=True)

# Mappatura basata sul foglio Excel reale (28 parametri totali elencati sotto)
parametri = [
    (3, "Passi", "bg-verde", "Stile di Vita e Attività"),
    (4, "Numero Giorni Analizzati", "bg-blu", "Giorni totali"),
    (5, "Punticcio di Saluti Odierno (Valore Cella)", "bg-verde", "Indice di Salute Olistico calcolato"),
    (7, "FC Tempo Medio Sveglio (Diurna)", "bg-giallo", "Frequenza Cardiaca Diurna"),
    (8, "FC Media Durante il Sonno (Riposo)", "bg-verde", "Effetto farmaci / battiti minimi"),
    (9, "HRV Durante il Sonno (7gg)", "bg-blu", "Variabilità della frequenza cardiaca"),
    (10, "SpO2 Media Durante il Sonno (7gg)", "bg-verde", "Saturazione ossigeno nel sangue"),
    (11, "Pressione Sistolica (Massima)", "bg-giallo", "Media pressione sistolica"),
    (12, "Pressione Diastolica (Minima)", "bg-verde", "Media pressione diolica"),
    (13, "ECG Ultimo Esito", "bg-blu", "Stato tracciato cardiaco"),
    (14, "Livello di Stress Stimato", "bg-blu", "Valutazione da HRV"),
    (17, "Media Ore di Sonno (7gg)", "bg-giallo", "Durata sonno globale"),
    (18, "Media Punteggio Sonno Storico", "bg-giallo", "Punteggio di qualità generale"),
    (19, "Interruzioni Notturne (Risvegli)", "bg-rosso", "Frequenza microrisvegli"),
    (20, "Efficienza del Sonno Media (7gg)", "bg-giallo", "Punteggio di qualità del sonno (%)"),
    (21, "Temperatura del Sonno Corporea", "bg-verde", "Media termica basale"),
    (22, "Valutazione Qualità Respiratoria", "bg-verde", "Ultima valutazione registrata"),
    (23, "Stato Regolarità Ritmo Circadiano", "bg-blu", "Profondità del sonno giudizio"),
    (24, "Media Ore Sonno Profondo (7gg)", "bg-blu", "Valore espresso in ore decimali"),
    (25, "Frequenza Respiratoria Notturna", "bg-verde", "Media atti respiratori (RPM)"),
    (26, "Rapporto Recupero HRV (Fine vs Inizio)", "bg-blu", "Confronto primi/secondi 90 minuti"),
    (27, "Punteggio di Recupero Fisico", "bg-verde", "Scala 0-100"),
    (28, "Punteggio di Recupero Mentale", "bg-blu", "Scala 0-100"),
    (29, "Monitoraggio Rischio Apnea Notturna", "bg-blu", "Rilevazione da sensori / CPAP"),
    (30, "Picco Frequenza Cardiaca Massima (7gg)", "bg-rosso", "Massimo battito diurno registrato"),
    (31, "Media Ore Utilizzo CPAP (7gg)", "bg-blu", "Tempo di utilizzo del ventilatore"),
    (32, "Raggiungimento Obiettivi Attività", "bg-verde", "Target passi quotidiano")
]

for riga, titolo, colore, nota in parametri:
    valore_mostrato = ottieni_valore_riep(riga, "--")
    
    # Adattamento cromatico automatico anche nel bottone interno se scende sotto una certa soglia
    if riga == 5:
        try:
            val_num = float(valore_mostrato.replace(',', '.'))
            if val_num >= 70.0: colore = "bg-verde"
            elif val_num <= 30.0: colore = "bg-rosso"
            else: colore = "bg-giallo"
        except: pass
        
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
    st.write("Le tue colonne sono:", list(df_cron.columns))
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
