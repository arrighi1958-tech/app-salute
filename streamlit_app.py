import streamlit as st
import pandas as pd
import time
import plotly.express as px

# CONFIGURAZIONE GENERALE
st.set_page_config(page_title="Pannello Salute Renato", page_icon="🩺", layout="centered")

# STILI CSS
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
URL_RIEPILOGO = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTPoEryjtZvVcaBEvSkgfh7qaeYXUJEmmDcZJh6fzBMZz80v1p7M009sdIVicHuI-Lj6AmC6SdWWsDj/pub?gid=320500951&single=true&output=csv"
URL_CRONOLOGIA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTPoEryjtZvVcaBEvSkgfh7qaeYXUJEmmDcZJh6fzBMZz80v1p7M009sdIVicHuI-Lj6AmC6SdWWsDj/pub?gid=784819219&single=true&output=csv"

timestamp = int(time.time())
CSV_RIEPILOGO = f"{URL_RIEPILOGO}&cache_bypass={timestamp}"
CSV_CRONOLOGIA = f"{URL_CRONOLOGIA}&cache_bypass={timestamp}"

@st.cache_data(ttl=5)
def load_data(url):
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

df_riep = load_data(CSV_RIEPILOGO)
df_cron = load_data(CSV_CRONOLOGIA)

st.title("🩺 Cruscotto Salute Renato")
st.markdown('<div class="clinical-box"><strong>Quadro Clinico (68 anni):</strong> Monitoraggio bilanciamento farmaci Ipertensione, Betabloccanti (M/S), Prostata, Anticoagulante permanente. Soglia minima FC impostata per controllo Bradicardia.</div>', unsafe_allow_html=True)

# FUNZIONE PER CALCOLARE LA MEDIA A 7 GIORNI CERCANDO LA COLONNA PER NOME
def calcola_media_per_nome(df, nome_colonna, e_testo=False):
    if df is None or df.empty:
        return "--"
    
    col_trovata = None
    for col in df.columns:
        if nome_colonna.lower() == col.lower() or nome_colonna.lower() in col.lower():
            col_trovata = col
            break
            
    if not col_trovata:
        return "--"
        
    try:
        ultimi_dati = df[col_trovata].dropna().tail(7)
        if ultimi_dati.empty:
            return "--"
            
        if e_testo:
            val = str(ultimi_dati.iloc[-1]).strip()
            return val if val not in ["nan", "", "None", "#DIV/0!"] else "--"
            
        serie_num = pd.to_numeric(ultimi_dati.astype(str).str.replace(',', '.'), errors='coerce').dropna()
        if serie_num.empty:
            return "--"
            
        media = serie_num.mean()
        return f"{media:.1f}".replace('.', ',')
    except:
        return "--"

# PUNTEGGIO DI SALUTE
punteggio_val = calcola_media_per_nome(df_riep, "Indice di Salute Olistico")
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
        <div class="punteggio-title">🎯 PUNTEGGIO DI SALUTE (Media 7 Giorni)</div>
        <div class="punteggio-value">{punteggio_val} <span style="font-size:20px; font-weight:500; color:#666;">/ 100</span></div>
        <div style="font-size: 12px; margin-top: 5px; font-weight: bold;">Media mobile calcolata sugli ultimi 7 rilevamenti</div>
    </div>
''', unsafe_allow_html=True)

# SEZIONE 1: MEDIE DI CONTROLLO
st.markdown('<div class="section-header">📊 Medie di Controllo (Ultimi 7 Giorni)</div>', unsafe_allow_html=True)

press_sist = calcola_media_per_nome(df_riep, "sistole")
press_diast = calcola_media_per_nome(df_riep, "diastole")
fc_riposo = calcola_media_per_nome(df_riep, "FC a riposo alta")
if fc_riposo == "--":
    fc_riposo = calcola_media_per_nome(df_riep, "FC media durante il sonno")
risvegli = calcola_media_per_nome(df_riep, "interruzioni notturne")
spo2 = calcola_media_per_nome(df_riep, "SpO2 media durante il sonno")
giorni_tot = len(df_riep) if df_riep is not None else "--"

st.markdown(f'<div class="metric-card bg-giallo"><div class="metric-title">Pressione Sistolica Media (7gg)</div><div class="metric-value">{press_sist} mmHg</div><div class="metric-status">Target ottimale stabilità: < 130-140</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Pressione Diastolica Media (7gg)</div><div class="metric-value">{press_diast} mmHg</div><div class="metric-status">Target ottimale stabilità: < 80-85</div></div>', unsafe_allow_html=True)

colore_fc = "bg-verde"
nota_fc = "Verifica tolleranza Betabloccante M/S"
try:
    if float(fc_riposo.replace(',', '.')) < 48:
        colore_fc = "bg-rosso"
        nota_fc = "⚠️ ATTENZIONE: Frequenza media bassa (< 48 bpm)"
except: pass

st.markdown(f'<div class="metric-card {colore_fc}"><div class="metric-title">Frequenza Cardiaca Media Riposo (7gg)</div><div class="metric-value">{fc_riposo} bpm</div><div class="metric-status">{nota_fc}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-rosso"><div class="metric-title">Media Risvegli Notturni (7gg)</div><div class="metric-value">{risvegli}</div><div class="metric-status">Indice nicturia / disturbi urinari da prostata</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Media Ossigenazione Notturna SpO2 (7gg)</div><div class="metric-value">{spo2} %</div><div class="metric-status">Efficacia respiratoria combinata a CPAP</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-blu"><div class="metric-title">Numero Giorni Registrati nel Foglio</div><div class="metric-value">{giorni_tot} giorni</div><div class="metric-status">Ampiezza dello storico dati attuale</div></div>', unsafe_allow_html=True)

# SEZIONE 2: PARAMETRI DETTAGLIATI
st.markdown('<div class="section-header">📋 Parametri Dettagliati (Media 7 Giorni)</div>', unsafe_allow_html=True)

parametri = [
    ("punteggio di qualità del sonno", "Qualità del Sonno (Punteggio)", "bg-giallo", "Media punteggio sonno 7gg"),
    ("durata sonno", "Durata Sonno (Ore)", "bg-giallo", "Media ore dormite 7gg"),
    ("FC media durante il sonno", "FC Media Durante il Sonno", "bg-verde", "Effetto farmaci notturno"),
    ("HRV durante il sonno", "HRV Durante il Sonno", "bg-blu", "Variabilità frequenza cardiaca 7gg"),
    ("frequenza respiratoria", "Frequenza Respiratoria Notturna", "bg-verde", "Media atti respiratori (RPM)"),
    ("ECG", "ECG Ultimo Esito", "bg-blu", "Stato tracciato (Ultimo inserimento)", True),
    ("temperatura del sonno", "Temperatura Corporea Sonno", "bg-verde", "Media termica basale 7gg"),
    ("Ore_CPAP", "Ore Utilizzo CPAP", "bg-blu", "Media ore ventilazione notturna 7gg"),
    ("CPAP Decimale", "Indice Efficacia CPAP", "bg-verde", "Efficacia media CPAP 7gg")
]

for nome_col, titolo, colore, nota, *is_text in parametri:
    e_testo = is_text[0] if is_text else False
    valore = calcola_media_per_nome(df_riep, nome_col, e_testo=e_testo)
    
    st.markdown(f'''
        <div class="metric-card {colore}">
            <div class="metric-title">{titolo}</div>
            <div class="metric-value">{valore}</div>
            <div class="metric-status">{nota}</div>
        </div>
    ''', unsafe_allow_html=True)

# SEZIONE 3: GRAFICI TEMPORALI
st.markdown('<div class="section-header">📈 Grafici di Tendenza Temporale</div>', unsafe_allow_html=True)

if df_cron is None or df_cron.empty:
    st.error("⚠️ Impossibile caricare la Cronologia. Verifica la pubblicazione CSV della scheda 'dati_sport'.")
else:
    data_col = df_cron.columns[0]
    df_cron[data_col] = pd.to_datetime(df_cron[data_col], dayfirst=True, errors='coerce')
    df_cron = df_cron.dropna(subset=[data_col]).sort_values(by=data_col)
    
    def disegna_grafico(parola_chiave, titolo_grafico, colore_linea):
        col_trovata = None
        for col in df_cron.columns:
            if parola_chiave.lower() in col.lower():
                col_trovata = col
                break
        
        if col_trovata:
            df_plot = df_cron.copy()
            df_plot[col_trovata] = pd.to_numeric(df_plot[col_trovata].astype(str).str.replace(',', '.'), errors='coerce')
            df_valido = df_plot.dropna(subset=[col_trovata])
            
            if not df_valido.empty:
                df_valido['Data_Formattata'] = df_valido[data_col].dt.strftime('%d/%m/%Y')
                fig = px.line(
                    df_valido, 
                    x='Data_Formattata', 
                    y=col_trovata, 
                    title=titolo_grafico,
                    markers=True, 
                    color_discrete_sequence=[colore_linea]
                )
                fig.update_layout(xaxis_title="Data", yaxis_title="Valore", height=300, margin=dict(l=10, r=10, t=40, b=10))
                st.plotly_chart(fig, use_container_width=True)

    disegna_grafico('Passi', '🏃 Conteggio Passi Giornalieri', '#34495E')
    disegna_grafico('Frequenza Cardiac', '❤️ Frequenza Cardiaca Media', '#2ECC71')
    disegna_grafico('Carico', '⚡ Indice di Carico Calcolato', '#E74C3C')
    disegna_grafico('Rockport', '🫁 Rockport VO2 Max', '#3498DB')
