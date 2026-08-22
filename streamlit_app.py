import streamlit as st
import pandas as pd
import time
import plotly.express as px

# CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Pannello Clinico Renato", page_icon="🩺", layout="centered")

# CSS OTTIMIZZATO
st.markdown("""
    <style>
    .stApp { background-color: #F4F6F7; }
    .metric-card {
        background-color: #ffffff; padding: 14px; border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06); margin-bottom: 12px; border-left: 8px solid #cccccc;
    }
    .metric-title { font-size: 14px; font-weight: 700; color: #2C3E50 !important; margin-bottom: 4px; }
    .metric-value { font-size: 24px; font-weight: 800; color: #111111 !important; }
    .metric-status { font-size: 12px; font-weight: 600; margin-top: 4px; }
    .section-header {
        font-size: 18px; font-weight: 800; color: #1A5276; margin-top: 20px;
        margin-bottom: 12px; border-bottom: 2px solid #1A5276; padding-bottom: 4px;
    }
    .clinical-box {
        background-color: #EBF5FB; padding: 12px; border-radius: 8px;
        border-left: 5px solid #1A5276; margin-bottom: 16px; font-size: 13px; color: #1B4F72 !important;
    }
    .bg-verde { border-left-color: #2ECC71 !important; }
    .bg-verde .metric-status { color: #27AE60 !important; }
    .bg-giallo { border-left-color: #F1C40F !important; }
    .bg-giallo .metric-status { color: #D4AC0D !important; }
    .bg-rosso { border-left-color: #E74C3C !important; }
    .bg-rosso .metric-status { color: #C0392B !important; }
    .bg-blu { border-left-color: #3498DB !important; }
    .bg-blu .metric-status { color: #2980B9 !important; }
    .punteggio-card {
        background-color: #ffffff; padding: 16px; border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06); margin-bottom: 15px; text-align: center; border: 2px solid #3498DB;
    }
    .punteggio-title { font-size: 14px; font-weight: 700; color: #333333 !important; }
    .punteggio-value { font-size: 32px; font-weight: 900; color: #1A5276 !important; }
    </style>
""", unsafe_allow_html=True)

# LINK PUBBLICATI GOOGLE SHEETS
URL_PANNELLO = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTPoEryjtZvVcaBEvSkgfh7qaeYXUJEmmDcZJh6fzBMZz80v1p7M009sdIVicHuI-Lj6AmC6SdWWsDj/pub?gid=320500951&single=true&output=csv"
URL_CRONOLOGIA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTPoEryjtZvVcaBEvSkgfh7qaeYXUJEmmDcZJh6fzBMZz80v1p7M009sdIVicHuI-Lj6AmC6SdWWsDj/pub?gid=784819219&single=true&output=csv"

timestamp = int(time.time())
CSV_PANNELLO = f"{URL_PANNELLO}&cache_bypass={timestamp}"
CSV_CRONOLOGIA = f"{URL_CRONOLOGIA}&cache_bypass={timestamp}"

@st.cache_data(ttl=2)
def load_data(url):
    try:
        df = pd.read_csv(url, header=None)
        return df
    except Exception as e:
        return None

df_riep = load_data(CSV_PANNELLO)
df_cron = load_data(CSV_CRONOLOGIA)

def cerca_valore(df, parola):
    if df is None or df.empty:
        return "--"
    try:
        for r_idx in range(len(df)):
            for c_idx in range(len(df.columns)):
                val_cell = str(df.iat[r_idx, c_idx])
                if parola.lower() in val_cell.lower():
                    # Cerca il primo valore utile nelle celle a destra o sotto
                    if c_idx + 1 < len(df.columns):
                        v = str(df.iat[r_idx, c_idx + 1]).strip()
                        if v and v.lower() not in ["nan", "none", "#div/0!"]:
                            return v
                    if r_idx + 1 < len(df):
                        v = str(df.iat[r_idx + 1, c_idx]).strip()
                        if v and v.lower() not in ["nan", "none", "#div/0!"]:
                            return v
        return "--"
    except:
        return "--"

st.title("🩺 Scheda Clinica e Monitoraggio")
st.markdown('<div class="clinical-box"><strong>PROFILO PAZIENTE (68 anni):</strong> Monitoraggio Terapia Anti-ipertensiva, Betabloccante (Bradicardia), Prostata/Nicturia e Terapia Ventilatoria CPAP.</div>', unsafe_allow_html=True)

# 🚨 PARTE 1: PARAMETRI CLINICI
st.markdown('<div class="section-header">🚨 PARAMETRI CLINICI PRIORITARI</div>', unsafe_allow_html=True)

press_sist = cerca_valore(df_riep, "sistole")
press_diast = cerca_valore(df_riep, "diastolica")
fc_sonno = cerca_valore(df_riep, "sonno")
fc_diurna = cerca_valore(df_riep, "sveglio")
fc_min_max = cerca_valore(df_riep, "massima")
ecg = cerca_valore(df_riep, "ecg")
spo2 = cerca_valore(df_riep, "spo2")
ore_cpap = cerca_valore(df_riep, "cpap")
risvegli = cerca_valore(df_riep, "risvegli")

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

# 📊 PARTE 2: INDICATORI DI BENESSERE
st.markdown('<div class="section-header">📊 INDICATORI DI BENESSERE E STILE DI VITA</div>', unsafe_allow_html=True)

punteggio_val = cerca_valore(df_riep, "punteggio")
passi = cerca_valore(df_riep, "passi")
durata_sonno = cerca_valore(df_riep, "ore di sonno")
sonno_prof = cerca_valore(df_riep, "profondità")
hrv = cerca_valore(df_riep, "hrv")
stress = cerca_valore(df_riep, "stress")
vo2max = cerca_valore(df_riep, "vo2")

st.markdown(f'''
    <div class="punteggio-card">
        <div class="punteggio-title">Punteggio di Salute Generale (Algoritmo Withings)</div>
        <div class="punteggio-value">{punteggio_val} / 100</div>
    </div>
''', unsafe_allow_html=True)

st.markdown(f'<div class="metric-card bg-blu"><div class="metric-title">Passi Medi (7gg)</div><div class="metric-value">{passi}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-giallo"><div class="metric-title">Durata Sonno (Giornaliero)</div><div class="metric-value">{durata_sonno} <span style="font-size:16px;">ore</span></div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-blu"><div class="metric-title">Variabilità Cardiaca HRV (7gg)</div><div class="metric-value">{hrv} <span style="font-size:16px;">ms</span></div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-blu"><div class="metric-title">Profondità Sonno (Giornaliero)</div><div class="metric-value">{sonno_prof}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-giallo"><div class="metric-title">Livello di Stress Stimato</div><div class="metric-value">{stress}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="metric-card bg-rosso"><div class="metric-title">Fitness VO2 Max</div><div class="metric-value">{vo2max}</div></div>', unsafe_allow_html=True)

# 📈 PARTE 3: GRAFICI DI TENDENZA
st.markdown('<div class="section-header">📈 GRAFICI DI TENDENZA CLINICA</div>', unsafe_allow_html=True)

if df_cron is not None and len(df_cron) > 1:
    try:
        # Pulisce la tabella e prende le prime due colonne (Data e Valore)
        df_plot = df_cron.copy()
        df_plot.columns = [str(c).strip() for c in df_plot.iloc[0]]
        df_plot = df_plot.iloc[1:].reset_index(drop=True)
        
        col_data = df_plot.columns[0]
        col_val = df_plot.columns[1] if len(df_plot.columns) > 1 else None
        
        if col_val:
            df_plot[col_data] = pd.to_datetime(df_plot[col_data], errors='coerce')
            df_plot[col_val] = pd.to_numeric(df_plot[col_val].astype(str).str.replace(',', '.', regex=False), errors='coerce')
            df_valido = df_plot.dropna(subset=[col_data, col_val]).sort_values(by=col_data)
            
            if not df_valido.empty:
                df_valido['Data_Fmt'] = df_valido[col_data].dt.strftime('%d/%m')
                fig = px.line(df_valido, x='Data_Fmt', y=col_val, markers=True, color_discrete_sequence=['#2ECC71'])
                fig.update_layout(title=dict(text=f"❤️ Tendenza ({col_val})", font=dict(size=14)), xaxis_title="", yaxis_title="Valore", height=280, margin=dict(l=10, r=10, t=40, b=10))
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    except Exception as e:
        st.info("I dati della cronologia saranno visualizzati non appena disponibili.")
