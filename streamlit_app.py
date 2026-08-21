import streamlit as st
import pandas as pd
import time
import plotly.express as px

# CONFIGURAZIONE GENERALE
st.set_page_config(page_title="Pannello Clinico Renato", page_icon="🩺", layout="centered")

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
        background-color: #EBF5FB;
        padding: 14px;
        border-radius: 8px;
        border-left: 6px solid #1A5276;
        margin-bottom: 20px;
        font-size: 13px;
        color: #1B4F72;
    }
    .bg-verde { border-left-color: #2ECC71 !important; color: #27AE60; }
    .bg-giallo { border-left-color: #F1C40F !important; color: #D4AC0D; }
    .bg-rosso { border-left-color: #E74C3C !important; color: #C0392B; }
    .bg-blu { border-left-color: #3498DB !important; color: #2980B9; }
    
    .punteggio-card {
        background-color: #fcfcfc;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        text-align: center;
        border: 2px solid #dddddd;
    }
    .punteggio-title {
        font-size: 15px;
        font-weight: bold;
        color: #555555;
    }
    .punteggio-value {
        font-size: 34px;
        font-weight: 900;
    }
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

st.title("🩺 Scheda Clinica e Monitoraggio")
st.markdown('<div class="clinical-box"><strong>PROFILO PAZIENTE (68 anni):</strong> Monitoraggio Terapia Anti-ipertensiva, Betabloccante (Bradicardia), Prostata/Nicturia e Terapia Ventilatoria CPAP.</div>', unsafe_allow_html=True)

# FUNZIONI ESTRAZIONE DATI
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
        if serie_num.empty: return "--"
            
        if media_7gg:
            serie_valida = serie_num[serie_num > 0].tail(7)
            if serie_valida.empty: return "--"
            return f"{serie_valida.mean():.1f}".replace('.', ',')
        else:
            ultimo_val = serie_num.iloc[-1]
            return f"{ultimo_val:.1f}".replace('.', ',') if ultimo_val % 1 != 0 else f"{int(ultimo_val)}"
    except:
        return "--"

def calcola_media_flessibile(df, lista_parole_chiave, media_7gg=True, e_testo=False):
    if df is None or df.empty: return "--"
    for parola in lista_parole_chiave:
        for idx, col in enumerate(df.columns):
            if parola.lower() in col.lower():
                return estrai_valore_colonna(df, idx, media_7gg=media_7gg, e_testo=e_testo)
    return "--"

# ==========================================
# 🚨 PARTE 1: PRIORITÀ CLINICA (MEDICO)
# ==========================================
st.markdown('<div class="section-header">🚨 PAROMETRI CLINICI PRIORITARI</div>', unsafe_allow_html=True)

press_sist = calcola_media_flessibile(df_riep, ["sistole"], media_7gg=True)
press_diast = calcola_media_flessibile(df_riep, ["diastole"], media_7gg=True)
fc_sonno = estrai_valore_colonna(df_riep, 4, media_7gg=True) # Colonna E
fc_diurna = calcola_media_flessibile(df_riep, ["FC tempo medio sveglio", "FC diurna"], media_7gg=True)
fc_min_max = calcola_media_flessibile(df_riep, ["Analisi FC Massima e Minima", "FC Massima e Minima"], media_7gg=False, e_testo=True)
ecg = calcola_media_flessibile(df_riep, ["ECG"], media_7gg=False, e_testo=True)
spo2 = calcola_media_flessibile(df_riep, ["SpO2"], media_7gg=True)
ore_cpap = calcola_media_flessibile(df_riep, ["Ore_CPAP", "Ore CPAP"], media_7gg=True)
risvegli = calcola_media_flessibile(df_riep, ["interruzioni notturne", "risvegli"], media_7gg=True)

# Pressione
st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Pressione Arteriosa (Media 7gg)</div><div class="metric-value">{press_sist} / {press_diast} <span style="font-size:16px;">mmHg</span></div><div class="metric-status">Target clinico ipertensione: < 130-140 / 80-85 mmHg</div></div>', unsafe_allow_html=True)

# Frequenze e Alert Bradicardia
colore_fc = "bg-verde"
nota_fc = "Frequenza cardiaca in target sotto betabloccante"
try:
    if float(fc_sonno.replace(',', '.')) < 48:
        colore_fc = "bg-rosso"
        nota_fc = "⚠️ SOGLIA CRITICA: Rischio bradicardia notturna (< 48 bpm)"
except: pass

st.markdown(f'<div class="metric-card {colore_fc}"><div class="metric-title">Frequenza Cardiaca Riposo / Sonno (Media 7gg)</div><div class="metric-value">{fc_sonno} <span style="font-size:16px;">bpm</span></div><div class="metric-status">{nota_fc}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-blu"><div class="metric-title">Frequenza Cardiaca Diurna (Media 7gg)</div><div class="metric-value">{fc_diurna} <span style="font-size:16px;">bpm</span></div><div class="metric-status">Valore medio durante la veglia</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-rosso"><div class="metric-title">Range FC Notturno (Min - Max Giornaliero)</div><div class="metric-value">{fc_min_max} <span style="font-size:16px;">bpm</span></div><div class="metric-status">Monitoraggio picchi e minimi bradicardici</div></div>', unsafe_allow_html=True)

# Respirazione e Terapia CPAP
st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Ore Utilizzo CPAP (Media 7gg)</div><div class="metric-value">{ore_cpap} <span style="font-size:16px;">ore</span></div><div class="metric-status">Aderenza alla terapia di ventilazione notturna</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Saturazione Ossigeno SpO2 (Media 7gg)</div><div class="metric-value">{spo2} %</div><div class="metric-status">Efficienza respiratoria notturna under-CPAP</div></div>', unsafe_allow_html=True)

# ECG & Risvegli
st.markdown(f'<div class="metric-card bg-blu"><div class="metric-title">Tracciato ECG (Ultimo Esito Giornaliero)</div><div class="metric-value">{ecg}</div><div class="metric-status">Controllo aritmie / Fibrillazione Atriale</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-giallo"><div class="metric-title">Risvegli Notturni / Nicturia (Media 7gg)</div><div class="metric-value">{risvegli}</div><div class="metric-status">Interruzioni notturne legate a riposo / prostata</div></div>', unsafe_allow_html=True)


# ==========================================
# ℹ️ PARTE 2: DATI SECONDARI E STILE DI VITA
# ==========================================
st.markdown('<div class="section-header">📊 INDICATORI DI BENESSERE E STILE DI VITA</div>', unsafe_allow_html=True)

punteggio_val = calcola_media_flessibile(df_riep, ["Indice di Salute Olistico", "Indice di Salute"], media_7gg=True)
passi = calcola_media_flessibile(df_riep, ["PASSI MEDIA SETTIMANALE", "Passi"], media_7gg=True)
durata_sonno = estrai_valore_colonna(df_riep, 2, media_7gg=False, e_testo=True)
sonno_prof = estrai_valore_colonna(df_riep, 8, media_7gg=False, e_testo=True)
hrv = calcola_media_flessibile(df_riep, ["HRV"], media_7gg=True)
stress = calcola_media_flessibile(df_riep, ["Stress"], media_7gg=False, e_testo=True)
vo2max = calcola_media_flessibile(df_riep, ["VO2 MAX", "VO2"], media_7gg=False, e_testo=True)

st.markdown(f'''
    <div class="punteggio-card">
        <div class="punteggio-title">Punteggio di Salute Generale (Algoritmo Withings)</div>
        <div class="punteggio-value">{punteggio_val} / 100</div>
    </div>
''', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="metric-card bg-blu"><div class="metric-title">Passi Medi (7gg)</div><div class="metric-value">{passi}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-card bg-giallo"><div class="metric-title">Durata Sonno (Ultima notte)</div><div class="metric-value">{durata_sonno}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-card bg-blu"><div class="metric-title">Variabilità Cardiaca HRV (7gg)</div><div class="metric-value">{hrv} ms</div></div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="metric-card bg-blu"><div class="metric-title">Profondità Sonno (Ultima notte)</div><div class="metric-value">{sonno_prof}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-card bg-giallo"><div class="metric-title">Livello di Stress Stimato</div><div class="metric-value" style="font-size:18px;">{stress}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-card bg-rosso"><div class="metric-title">Fitness VO2 Max</div><div class="metric-value">{vo2max}</div></div>', unsafe_allow_html=True)


# ==========================================
# 📈 PARTE 3: GRAFICI TEMPORALI
# ==========================================
st.markdown('<div class="section-header">📈 GRAFICI DI TENDENZA TEMPORALE</div>', unsafe_allow_html=True)

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
                fig = px.line(df_valido, x='Data_Formattata', y=col_trovata, title=titolo_grafico, markers=True, color_discrete_sequence=[colore_linea])
                fig.update_layout(xaxis_title="Data", yaxis_title="Valore", height=280, margin=dict(l=10, r=10, t=35, b=10))
                st.plotly_chart(fig, use_container_width=True)

    disegna_grafico('Frequenza Cardiac', '❤️ Tendenza Frequenza Cardiaca', '#2ECC71')
    disegna_grafico('Passi', '🏃 Tendenza Passi Giornalieri', '#34495E')
    disegna_grafico('Carico', '⚡ Indice di Carico', '#E74C3C')
