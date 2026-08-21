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
        df = pd.read_csv(url, header=0)
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

df_riep = load_data(CSV_RIEPILOGO)
df_cron = load_data(CSV_CRONOLOGIA)

st.title("🩺 Cruscotto Salute Renato")
st.markdown('<div class="clinical-box"><strong>Quadro Clinico (68 anni):</strong> Monitoraggio bilanciamento farmaci Ipertensione, Betabloccanti (M/S), Prostata, Anticoagulante permanente. Soglia minima FC impostata per controllo Bradicardia.</div>', unsafe_allow_html=True)

# FUNZIONE ESTRAZIONE DATI PER INDICE DI COLONNA SPECIFICO (0-based)
def estrai_valore_colonna(df, idx_colonna, media_7gg=True, e_testo=False):
    if df is None or df.empty or idx_colonna >= len(df.columns):
        return "--"
    try:
        col = df.columns[idx_colonna]
        if e_testo:
            val_serie = df[col].dropna()
            if val_serie.empty: return "--"
            val = str(val_serie.iloc[-1]).strip()
            return val if val not in ["nan", "", "None", "#DIV/0!"] else "--"
            
        serie_num = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce').dropna()
        if serie_num.empty:
            return "--"
            
        # Per i dati numerici: se media_7gg è True calcola la media mobile degli ultimi 7 rilevamenti validi
        if media_7gg:
            serie_valida = serie_num[serie_num > 0].tail(7)
            if serie_valida.empty: return "--"
            return f"{serie_valida.mean():.1f}".replace('.', ',')
        else:
            # Ultimo valore singolo (Giornaliero)
            ultimo_val = serie_num.iloc[-1]
            return f"{ultimo_val:.1f}".replace('.', ',') if ultimo_val % 1 != 0 else f"{int(ultimo_val)}"
    except:
        return "--"

# FUNZIONE RICERCA ROBUSTA PER NOME COLONNA
def calcola_media_flessibile(df, lista_parole_chiave, media_7gg=True, e_testo=False):
    if df is None or df.empty:
        return "--"
    for parola in lista_parole_chiave:
        for idx, col in enumerate(df.columns):
            if parola.lower() in col.lower():
                return estrai_valore_colonna(df, idx, media_7gg=media_7gg, e_testo=e_testo)
    return "--"

# PUNTEGGIO DI SALUTE
punteggio_val = calcola_media_flessibile(df_riep, ["Indice di Salute Olistico", "Indice di Salute"], media_7gg=True)
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
        <div class="punteggio-title">🎯 PUNTEGGIO DI SALUTE OLISTICO (Media 7 Giorni)</div>
        <div class="punteggio-value">{punteggio_val} <span style="font-size:20px; font-weight:500; color:#666;">/ 100</span></div>
        <div style="font-size: 12px; margin-top: 5px; font-weight: bold;">Valutazione globale ponderata del benessere generale</div>
    </div>
''', unsafe_allow_html=True)

# SEZIONE 1: MEDIE DI CONTROLLO
st.markdown('<div class="section-header">📊 Parametri Clinici Principali (Media 7 Giorni)</div>', unsafe_allow_html=True)

press_sist = calcola_media_flessibile(df_riep, ["sistole"], media_7gg=True)
press_diast = calcola_media_flessibile(df_riep, ["diastole"], media_7gg=True)
fc_riposo = estrai_valore_colonna(df_riep, 4, media_7gg=True) # COLONNA E: FC Media durante il sonno
risvegli = calcola_media_flessibile(df_riep, ["interruzioni notturne", "interruzioni"], media_7gg=True)
spo2 = calcola_media_flessibile(df_riep, ["SpO2 media", "SpO2"], media_7gg=True)
giorni_tot = len(df_riep) if df_riep is not None else "--"

st.markdown(f'<div class="metric-card bg-giallo"><div class="metric-title">Pressione Arteriosa Sistolica (Media 7gg)</div><div class="metric-value">{press_sist} mmHg</div><div class="metric-status">Soglia di stabilità ipertensiva: < 130-140 mmHg</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Pressione Arteriosa Diastolica (Media 7gg)</div><div class="metric-value">{press_diast} mmHg</div><div class="metric-status">Soglia di stabilità ipertensiva: < 80-85 mmHg</div></div>', unsafe_allow_html=True)

colore_fc = "bg-verde"
nota_fc = "Frequenza notturna stabile (Tolleranza betabloccante)"
try:
    if float(fc_riposo.replace(',', '.')) < 48:
        colore_fc = "bg-rosso"
        nota_fc = "⚠️ ATTENZIONE: Frequenza cardiaca media ridotta (< 48 bpm)"
except: pass

st.markdown(f'<div class="metric-card {colore_fc}"><div class="metric-title">FC Media Durante il Sonno [Colonna E] (Media 7gg)</div><div class="metric-value">{fc_riposo} bpm</div><div class="metric-status">{nota_fc}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-rosso"><div class="metric-title">Risvegli Notturni Medi (Media 7gg)</div><div class="metric-value">{risvegli}</div><div class="metric-status">Monitoraggio continuo nicturia / sonno disturbato</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Saturazione Ossigeno SpO2 (Media 7gg)</div><div class="metric-value">{spo2} %</div><div class="metric-status">Efficacia scambio respiratorio durante il sonno</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-blu"><div class="metric-title">Totale Giornate Monitorate</div><div class="metric-value">{giorni_tot} giorni</div><div class="metric-status">Storico dati registrato nel sistema</div></div>', unsafe_allow_html=True)

# SEZIONE 2: PARAMETRI DETTAGLIATI
st.markdown('<div class="section-header">📋 Dettaglio Qualità Sonno e CPAP</div>', unsafe_allow_html=True)

# Mappatura e puntamenti precisi: (Metodo/Indice, Titolo, Colore, Nota, Media_7gg, Es_Testo)
parametri = [
    (calcola_media_flessibile(df_riep, ["punteggio di qualità del sonno", "qualità del sonno"], media_7gg=True), "Punteggio Qualità Sonno (Media 7gg)", "bg-giallo", "Indice sintetico Withings qualità riposo"),
    (estrai_valore_colonna(df_riep, 2, media_7gg=False, e_testo=True), "Durata Sonno [Colonna C] (Giornaliero)", "bg-giallo", "Ore effetive di riposo dell'ultima notte"),
    (estrai_valore_colonna(df_riep, 8, media_7gg=False, e_testo=True), "Profondità del Sonno [Colonna I] (Giornaliero)", "bg-blu", "Giudizio sulla profondità del sonno dell'ultima notte"),
    (estrai_valore_colonna(df_riep, 7, media_7gg=False, e_testo=True), "Profondità Sonno REM [Colonna H] (Giornaliero)", "bg-blu", "Tempo di sonno in fase REM dell'ultima notte"),
    (calcola_media_flessibile(df_riep, ["HRV durante il sonno", "HRV"], media_7gg=True), "Variabilità Cardiaca HRV (Media 7gg)", "bg-blu", "Indice di recupero del sistema nervoso autonomo"),
    (calcola_media_flessibile(df_riep, ["frequenza respiratoria"], media_7gg=True), "Frequenza Respiratoria (Media 7gg)", "bg-verde", "Atti respiratori medi al minuto (RPM)"),
    (calcola_media_flessibile(df_riep, ["ECG"], media_7gg=False, e_testo=True), "Tracciato ECG (Giornaliero)", "bg-blu", "Risultato dell'ultima rilevazione elettrocardiografica"),
    (calcola_media_flessibile(df_riep, ["temperatura del sonno", "temperatura"], media_7gg=True), "Temperatura Corporea Basale (Media 7gg)", "bg-verde", "Variazione termica durante la notte (°C)"),
    (calcola_media_flessibile(df_riep, ["Ore_CPAP", "Ore CPAP", "CPAP"], media_7gg=True), "Ore Utilizzo Ventilatore CPAP (Media 7gg)", "bg-blu", "Tempo di utilizzo effettivo della ventilazione"),
    (calcola_media_flessibile(df_riep, ["CPA P Decimale", "CPA P", "CPAP Decimale"], media_7gg=True), "Indice Efficacia Terapia CPAP (Media 7gg)", "bg-verde", "Qualità ed efficacia del supporto respiratorio")
]

for valore, titolo, colore, nota in parametri:
    st.markdown(f'''
        <div class="metric-card {colore}">
            <div class="metric-title">{titolo}</div>
            <div class="metric-value">{valore}</div>
            <div class="metric-status">{nota}</div>
        </div>
    ''', unsafe_allow_html=True)

# SEZIONE 3: GRAFICI TEMPORALI
st.markdown('<div class="section-header">📈 Grafici di Tendenza Temporale (Giornaliero)</div>', unsafe_allow_html=True)

if df_cron is not None and not df_cron.empty:
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
                    title=f"{titolo_grafico} (Giornaliero)",
                    markers=True, 
                    color_discrete_sequence=[colore_linea]
                )
                fig.update_layout(
                    xaxis_title="Data", 
                    yaxis_title="Valore", 
                    height=300, 
                    margin=dict(l=10, r=10, t=40, b=10)
                )
                st.plotly_chart(fig, use_container_width=True)

    disegna_grafico('Passi', '🏃 Conteggio Passi', '#34495E')
    disegna_grafico('Frequenza Cardiac', '❤️ Frequenza Cardiaca', '#2ECC71')
    disegna_grafico('Carico', '⚡ Indice di Carico Calcolato', '#E74C3C')
    disegna_grafico('Rockport', '🫁 Rockport VO2 Max', '#3498DB')
