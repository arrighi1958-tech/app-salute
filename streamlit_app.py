import streamlit as st
import pandas as pd
import time
import plotly.express as px

# CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Pannello Clinico Renato", page_icon="🩺", layout="centered")

# CSS OTTIMIZZATO PER MOBILE E CONTRASTO
st.markdown("""
    <style>
    /* Forzatura sfondo globale */
    .stApp {
        background-color: #F4F6F7;
    }
    
    .metric-card {
        background-color: #ffffff;
        padding: 14px;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        margin-bottom: 12px;
        border-left: 8px solid #cccccc;
    }
    .metric-title {
        font-size: 14px;
        font-weight: 700;
        color: #2C3E50 !important;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 26px;
        font-weight: 800;
        color: #111111 !important;
    }
    .metric-status {
        font-size: 12px;
        font-weight: 600;
        margin-top: 4px;
    }
    .section-header {
        font-size: 18px;
        font-weight: 800;
        color: #1A5276;
        margin-top: 20px;
        margin-bottom: 12px;
        border-bottom: 2px solid #1A5276;
        padding-bottom: 4px;
    }
    .clinical-box {
        background-color: #EBF5FB;
        padding: 12px;
        border-radius: 8px;
        border-left: 5px solid #1A5276;
        margin-bottom: 16px;
        font-size: 13px;
        color: #1B4F72 !important;
    }
    
    /* Bordi di stato */
    .bg-verde { border-left-color: #2ECC71 !important; }
    .bg-verde .metric-status { color: #27AE60 !important; }
    .bg-giallo { border-left-color: #F1C40F !important; }
    .bg-giallo .metric-status { color: #D4AC0D !important; }
    .bg-rosso { border-left-color: #E74C3C !important; }
    .bg-rosso .metric-status { color: #C0392B !important; }
    .bg-blu { border-left-color: #3498DB !important; }
    .bg-blu .metric-status { color: #2980B9 !important; }
    
    /* Card Punteggio con testo scuro visibile */
    .punteggio-card {
        background-color: #ffffff;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        margin-bottom: 15px;
        text-align: center;
        border: 2px solid #3498DB;
    }
    .punteggio-title {
        font-size: 14px;
        font-weight: 700;
        color: #333333 !important;
    }
    .punteggio-value {
        font-size: 32px;
        font-weight: 900;
        color: #1A5276 !important;
    }
    </style>
""", unsafe_allow_html=True)

# URL GOOGLE SHEETS
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

def ottieni_valore(df, parole_chiave, e_testo=False, media_7gg=True, e_passi=False):
    if df is None or df.empty:
        return "--"
    
    col_trovata = None
    for parola in parole_chiave:
        for col in df.columns:
            if parola.lower() in col.lower():
                col_trovata = col
                break
        if col_trovata:
            break
            
    if not col_trovata:
        return "--"
        
    try:
        serie_pulita = df[col_trovata].dropna()
        if serie_pulita.empty:
            return "--"
            
        ultimo_grezzo = str(serie_pulita.iloc[-1]).strip()
        
        if e_testo or "-" in ultimo_grezzo or ":" in ultimo_grezzo:
            return ultimo_grezzo if ultimo_grezzo not in ["nan", "", "None", "#DIV/0!"] else "--"
            
        serie_num = pd.to_numeric(
            serie_pulita.astype(str).str.replace(',', '.', regex=False), 
            errors='coerce'
        ).dropna()
        
        if serie_num.empty:
            return ultimo_grezzo
            
        if media_7gg:
            val_validi = serie_num[serie_num > 0].tail(7)
            if val_validi.empty:
                return "--"
            v = val_validi.mean()
        else:
            v = serie_num.iloc[-1]
            
        if e_passi:
            if v < 100:
                v = v * 1000
            return f"{int(round(v)):,}".replace(',', '.')
            
        return f"{v:.1f}".replace('.', ',') if v % 1 != 0 else f"{int(v)}"
    except:
        return "--"

# ==========================================
# 🚨 PARTE 1: PARAMETRI CLINICI PRIORITARI
# ==========================================
st.markdown('<div class="section-header">🚨 PARAMETRI CLINICI PRIORITARI</div>', unsafe_allow_html=True)

press_sist = ottieni_valore(df_riep, ["sistole", "pressione sistolica"], media_7gg=True)
press_diast = ottieni_valore(df_riep, ["diastole", "pressione diastolica"], media_7gg=True)
fc_sonno = ottieni_valore(df_riep, ["fc sonno", "frequenza sonno", "fc riposo"], media_7gg=True)
fc_diurna = ottieni_valore(df_riep, ["fc diurna", "sveglio", "diurna"], media_7gg=True)
fc_min_max = ottieni_valore(df_riep, ["range fc", "min - max", "analisi fc"], e_testo=True)
ecg = ottieni_valore(df_riep, ["ecg", "tracciato"], e_testo=True)
spo2 = ottieni_valore(df_riep, ["spo2", "saturazione"], media_7gg=True)
ore_cpap = ottieni_valore(df_riep, ["cpap", "ore cpap"], media_7gg=True)
risvegli = ottieni_valore(df_riep, ["risvegli", "nicturia", "interruzioni"], media_7gg=True)

st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Pressione Arteriosa (Media 7gg)</div><div class="metric-value">{press_sist} / {press_diast} <span style="font-size:16px;">mmHg</span></div><div class="metric-status">Target clinico ipertensione: < 130-140 / 80-85 mmHg</div></div>', unsafe_allow_html=True)

colore_fc = "bg-verde"
nota_fc = "Frequenza cardiaca in target sotto betabloccante"
try:
    if float(str(fc_sonno).replace(',', '.')) < 48:
        colore_fc = "bg-rosso"
        nota_fc = "⚠️ SOGLIA CRITICA: Rischio bradicardia notturna (< 48 bpm)"
except: pass

st.markdown(f'<div class="metric-card {colore_fc}"><div class="metric-title">Frequenza Cardiaca Riposo / Sonno (Media 7gg)</div><div class="metric-value">{fc_sonno} <span style="font-size:16px;">bpm</span></div><div class="metric-status">{nota_fc}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-blu"><div class="metric-title">Frequenza Cardiaca Diurna (Media 7gg)</div><div class="metric-value">{fc_diurna} <span style="font-size:16px;">bpm</span></div><div class="metric-status">Valore medio durante la veglia</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-rosso"><div class="metric-title">Range FC Notturno (Min - Max Giornaliero)</div><div class="metric-value">{fc_min_max} <span style="font-size:16px;">bpm</span></div><div class="metric-status">Monitoraggio picchi e minimi bradicardici</div></div>', unsafe_allow_html=True)

st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Ore Utilizzo CPAP (Media 7gg)</div><div class="metric-value">{ore_cpap} <span style="font-size:16px;">ore</span></div><div class="metric-status">Aderenza alla terapia di ventilazione notturna</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-verde"><div class="metric-title">Saturazione Ossigeno SpO2 (Media 7gg)</div><div class="metric-value">{spo2} %</div><div class="metric-status">Efficienza respiratoria notturna under-CPAP</div></div>', unsafe_allow_html=True)

st.markdown(f'<div class="metric-card bg-blu"><div class="metric-title">Tracciato ECG (Ultimo Esito Giornaliero)</div><div class="metric-value">{ecg}</div><div class="metric-status">Controllo aritmie / Fibrillazione Atriale</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-giallo"><div class="metric-title">Risvegli Notturni / Nicturia (Media 7gg)</div><div class="metric-value">{risvegli}</div><div class="metric-status">Interruzioni notturne legate a riposo / prostata</div></div>', unsafe_allow_html=True)

# ==========================================
# 📊 PARTE 2: INDICATORI DI BENESSERE
# ==========================================
st.markdown('<div class="section-header">📊 INDICATORI DI BENESSERE E STILE DI VITA</div>', unsafe_allow_html=True)

punteggio_val = ottieni_valore(df_riep, ["punteggio", "indice di salute", "withings"], media_7gg=False)
passi = ottieni_valore(df_riep, ["passi"], media_7gg=False, e_passi=True)
durata_sonno = ottieni_valore(df_riep, ["durata sonno"], e_testo=True)
sonno_prof = ottieni_valore(df_riep, ["profondità"], e_testo=True)
hrv = ottieni_valore(df_riep, ["hrv", "variabilità"], media_7gg=True)
stress = ottieni_valore(df_riep, ["stress"], media_7gg=True)
vo2max = ottieni_valore(df_riep, ["vo2"], media_7gg=False)

st.markdown(f'''
    <div class="punteggio-card">
        <div class="punteggio-title">Punteggio di Salute Generale (Algoritmo Withings)</div>
        <div class="punteggio-value">{punteggio_val} / 100</div>
    </div>
''', unsafe_allow_html=True)

st.markdown(f'<div class="metric-card bg-blu"><div class="metric-title">Passi Medi (7gg)</div><div class="metric-value">{passi}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-giallo"><div class="metric-title">Durata Sonno (Giornaliero)</div><div class="metric-value">{durata_sonno}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-blu"><div class="metric-title">Variabilità Cardiaca HRV (7gg)</div><div class="metric-value">{hrv} ms</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-blu"><div class="metric-title">Profondità Sonno (Giornaliero)</div><div class="metric-value">{sonno_prof}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-giallo"><div class="metric-title">Livello di Stress Stimato</div><div class="metric-value">{stress}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-rosso"><div class="metric-title">Fitness VO2 Max</div><div class="metric-value">{vo2max}</div></div>', unsafe_allow_html=True)

# ==========================================
# 📈 PARTE 3: GRAFICI DI TENDENZA CLINICA
# ==========================================
st.markdown('<div class="section-header">📈 GRAFICI DI TENDENZA CLINICA</div>', unsafe_allow_html=True)

if df_cron is not None and not df_cron.empty:
    data_col = df_cron.columns[0]
    
    df_cron[data_col] = pd.to_datetime(df_cron[data_col], errors='coerce')
    df_cron = df_cron.dropna(subset=[data_col]).sort_values(by=data_col)
    
    def disegna_grafico(parola_chiave, titolo_grafico, colore_linea):
        col_trovata = None
        for col in df_cron.columns:
            if parola_chiave.lower() in col.lower():
                col_trovata = col
                break
        if col_trovata:
            df_plot = df_cron.copy()
            df_plot[col_trovata] = pd.to_numeric(df_plot[col_trovata].astype(str).str.replace(',', '.', regex=False), errors='coerce')
            df_valido = df_plot.dropna(subset=[col_trovata])
            
            if not df_valido.empty:
                df_valido['Data_Formattata'] = df_valido[data_col].dt.strftime('%d/%m')
                
                fig = px.line(
                    df_valido, 
                    x='Data_Formattata', 
                    y=col_trovata, 
                    markers=True, 
                    color_discrete_sequence=[colore_linea]
                )
                fig.update_layout(
                    title=dict(text=titolo_grafico, font=dict(size=14)),
                    xaxis_title="", 
                    yaxis_title="bpm", 
                    height=280, 
                    margin=dict(l=10, r=10, t=40, b=10)
                )
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    disegna_grafico('Frequenza Cardiac', '❤️ Tendenza Frequenza Cardiaca (bpm)', '#2ECC71')
