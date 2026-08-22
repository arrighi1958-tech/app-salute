import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Pannello Clinico Renato", page_icon="🩺", layout="wide")

# CSS DEDICATO PER RIPRODURRE LO STILE ORIGINALE
st.markdown("""
    <style>
    .stApp { background-color: #F4F6F9; }
    
    .card-container {
        background-color: #ffffff;
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        border-left-width: 8px;
        border-left-style: solid;
    }
    
    .card-title {
        font-size: 13px;
        font-weight: 700;
        color: #2C3E50;
        margin-bottom: 6px;
    }
    
    .card-value {
        font-size: 26px;
        font-weight: 800;
        color: #111111;
        margin-bottom: 6px;
    }
    
    .card-subtitle {
        font-size: 12px;
        font-weight: 600;
    }
    
    /* VARIANTI COLORE */
    .border-red { border-left-color: #E74C3C; }
    .text-red { color: #C0392B; }
    
    .border-green { border-left-color: #2ECC71; }
    .text-green { color: #27AE60; }
    
    .border-blue { border-left-color: #3498DB; }
    .text-blue { color: #2980B9; }
    
    .border-yellow { border-left-color: #F1C40F; }
    .text-yellow { color: #D4AC0D; }

    .section-header {
        font-size: 18px; font-weight: 800; color: #1B4F72; margin-top: 15px;
        margin-bottom: 15px; border-bottom: 2px solid #2980B9; padding-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

SHEET_ID = "1sKNtsluKQKPwqA-YToNexsHa0Gu7-Nnx8pCv628qeog"

URL_PANNELLO = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
URL_CRONOLOGIA = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=320500951"

@st.cache_data(ttl=2)
def carica_dati(url):
    try:
        return pd.read_csv(url, header=None)
    except Exception:
        return None

def calcola_formattazione_condizionale(label, valore):
    lbl = str(label).lower()
    val_str = str(valore).strip().lower()
    
    # 1. VALORI MANCANTI -> ROSSO
    if val_str in ["--", "", "nan", "none", "n/a"]:
        return "border-red", "text-red", "Dato non pervenuto / Monitoraggio richiesto"

    # Estrazione eventuale valore numerico
    val_num = None
    try:
        # Pulisce stringhe con percentuali o virgole per estrarre numeri
        clean_val = val_str.replace('%', '').replace(',', '.').strip()
        val_num = float(clean_val)
    except ValueError:
        pass

    # 2. VALUTAZIONE SPECIFICA DEI PARAMETRI

    # SpO2 / Saturazione
    if "spo2" in lbl or "saturazione" in lbl:
        if val_num is not None:
            if val_num < 95.0:
                return "border-red", "text-red", "Saturazione bassa under-CPAP"
            elif val_num >= 95.0:
                return "border-green", "text-green", "Efficienza respiratoria notturna ottima"

    # CPAP Utilizzo
    if "cpap" in lbl:
        if val_num is not None:
            if val_num < 4.0:
                return "border-red", "text-red", "Aderenza CPAP insufficiente (< 4 ore)"
            elif val_num < 6.0:
                return "border-yellow", "text-yellow", "Aderenza CPAP moderata"
            else:
                return "border-green", "text-green", "Aderenza alla terapia di ventilazione notturna"

    # Risvegli / Interruzioni
    if "risvegli" in lbl or "interruzioni" in lbl:
        if val_num is not None:
            if val_num > 4.0:
                return "border-red", "text-red", "Frequenti interruzioni notturne"
            elif val_num >= 2.0:
                return "border-yellow", "text-yellow", "Interruzioni notturne legate a riposo / prostata"
            else:
                return "border-green", "text-green", "Qualità del sonno e continuità ottimali"

    # Pressione Sistolica
    if "sistole" in lbl or "massima" in lbl:
        if val_num is not None:
            if val_num > 135:
                return "border-red", "text-red", "Valore di pressione massima elevato"
            elif val_num > 125:
                return "border-yellow", "text-yellow", "Pressione massima borderline"
            else:
                return "border-green", "text-green", "Pressione massima nella norma"

    # HRV / Variabilità Cardiaca
    if "hrv" in lbl:
        if val_num is not None:
            if val_num < 20:
                return "border-red", "text-red", "Variabilità cardiaca ridotta (Recupero basso)"
            elif val_num < 35:
                return "border-yellow", "text-yellow", "Variabilità cardiaca nella media"
            else:
                return "border-green", "text-green", "Ottimo livello di variabilità cardiaca"

    # Stress
    if "stress" in lbl:
        if "alto" in val_str or "elevato" in val_str:
            return "border-red", "text-red", "Livello di stress elevato"
        elif "moderato" in val_str or "medio" in val_str:
            return "border-yellow", "text-yellow", "Consigliato riposo attivo"
        else:
            return "border-green", "text-green", "Livello di stress ottimale"

    # ECG
    if "ecg" in lbl or "tracciato" in lbl:
        if "sinusale" in val_str:
            return "border-blue", "text-blue", "Controllo aritmie / Ritmo Sinusale"
        elif any(w in val_str for w in ["aritmia", "fibrillazione", "anomalo"]):
            return "border-red", "text-red", "Anomalia rilevata nel tracciato"

    # Target / Obiettivi
    if "raggiungimento" in lbl or "obiettivi" in lbl or "target" in lbl:
        if "raggiunto" in val_str:
            return "border-green", "text-green", "Target giornaliero completato"
        else:
            return "border-yellow", "text-yellow", "Target in corso di completamento"

    # Predefinito per parametri informativi standard (Pas, Giorni Analizzati, ecc.)
    return "border-blue", "text-blue", "Indicatore di monitoraggio generale"

df_p = carica_dati(URL_PANNELLO)
df_c = carica_dati(URL_CRONOLOGIA)

st.title("🩺 Scheda Clinica e Monitoraggio")

if df_p is not None:
    st.markdown('<div class="section-header">🚨 PARAMETRI CLINICI E BENESSERE</div>', unsafe_allow_html=True)
    
    items = []
    for idx, row in df_p.iterrows():
        if len(row) >= 2 and pd.notna(row[0]) and str(row[0]).strip() != "":
            label = str(row[0]).strip()
            valore = str(row[1]).strip() if pd.notna(row[1]) else "--"
            if valore != "--" and label.lower() not in ["date", "data", "date [data]"]:
                items.append((label, valore))
    
    cols = st.columns(3)
    for index, (lbl, val) in enumerate(items):
        cls_border, cls_text, nota = calcola_formattazione_condizionale(lbl, val)
        col = cols[index % 3]
        with col:
            st.markdown(f'''
                <div class="card-container {cls_border}">
                    <div class="card-title">{lbl}</div>
                    <div class="card-value">{val}</div>
                    <div class="card-subtitle {cls_text}">{nota}</div>
                </div>
            ''', unsafe_allow_html=True)

# SEZIONE GRAFICO CRONOLOGIA
st.markdown('<div class="section-header">📈 GRAFICI DI TENDENZA CLINICA</div>', unsafe_allow_html=True)

if df_c is not None and len(df_c) > 1:
    try:
        df_plot = df_c.copy()
        df_plot.columns = df_plot.iloc[0]
        df_plot = df_plot[1:]
        
        col_x = df_plot.columns[0]
        col_y = df_plot.columns[1]
        
        df_plot[col_x] = pd.to_datetime(df_plot[col_x], dayfirst=True, errors='coerce')
        df_plot[col_y] = pd.to_numeric(df_plot[col_y].astype(str).str.replace(',', '.'), errors='coerce')
        
        df_plot = df_plot.dropna(subset=[col_x, col_y]).sort_values(by=col_x)
        
        if not df_plot.empty:
            fig = px.line(
                df_plot, 
                x=col_x, 
                y=col_y, 
                markers=True, 
                title=f"Andamento: {col_y}",
                labels={col_x: "Data", col_y: "Valore"}
            )
            fig.update_traces(line_color='#2980B9', line_width=3, marker_size=6)
            st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.info("Aggiornamento grafico in corso...")
