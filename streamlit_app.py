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

# MAPPATURA SPECIFICA PERICOLI E NOTE IN BASE AI PARAMETRI
def ottieni_stile_e_nota(label, valore):
    lbl = str(label).lower()
    val = str(valore).lower()
    
    # 1. ROSSO (Valori mancanti o alterati)
    if "range fc" in lbl or valore == "--" or "elevato" in val:
        return "border-red", "text-red", "Monitoraggio picchi e minimi bradicardici"
        
    # 2. VERDE (CPAP, SpO2, Valori ottimali)
    if "cpap" in lbl:
        return "border-green", "text-green", "Aderenza alla terapia di ventilazione notturna"
    if "spo2" in lbl or "saturazione" in lbl:
        return "border-green", "text-green", "Efficienza respiratoria notturna under-CPAP"
    if any(w in val for w in ["ottimale", "buono", "raggiunto", "basso / assente"]):
        return "border-green", "text-green", "Parametro nei limiti di riferimento"

    # 3. GIALLO (Risvegli, Nicturia, Stress)
    if "risvegli" in lbl or "interruzioni" in lbl or "stress" in lbl:
        return "border-yellow", "text-yellow", "Interruzioni notturne legate a riposo / prostata"
        
    # 4. BLU (ECG, Pressione, Standard)
    if "ecg" in lbl or "sinusale" in val:
        return "border-blue", "text-blue", "Controllo aritmie / Fibrillazione Atriale"
        
    return "border-blue", "text-blue", "Indicatore di benessere"

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
        cls_border, cls_text, nota = ottieni_stile_e_nota(lbl, val)
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
