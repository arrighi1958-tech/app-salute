import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Pannello Clinico Renato", page_icon="🩺", layout="wide")

# CSS BASE
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    .metric-card {
        background-color: #ffffff; padding: 14px; border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 12px;
    }
    .metric-title { font-size: 12px; font-weight: 700; color: #566573 !important; text-transform: uppercase; }
    .metric-value { font-size: 20px; font-weight: 800; color: #1B2631 !important; margin-top: 4px; }
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

# FUNZIONE FORMATTAZIONE CONDIZIONALE (ASSEGNAZIONE COLORE BORDO)
def ottieni_colore_bordo(label, valore):
    val_str = str(valore).lower()
    lbl_str = str(label).lower()
    
    if any(w in val_str for w in ["ottimale", "buono", "sinusale", "raggiunto", "basso / assente"]):
        return "#2ECC71"  # Verde
    elif any(w in val_str for w in ["moderato", "attenzione", "medio"]):
        return "#F39C12"  # Arancione
    elif any(w in val_str for w in ["alto", "critico", "elevato"]):
        return "#E74C3C"  # Rosso
    
    # Regole sui valori numerici principali
    try:
        val_num = float(str(valore).replace(',', '.'))
        if "passi" in lbl_str and val_num >= 5000:
            return "#2ECC71"
        if "spo2" in lbl_str and val_num >= 95:
            return "#2ECC71"
    except ValueError:
        pass

    return "#3498DB"  # Blu predefinito

df_p = carica_dati(URL_PANNELLO)
df_c = carica_dati(URL_CRONOLOGIA)

st.title("🩺 Scheda Clinica e Monitoraggio")

# SEZIONE PARAMETRI CLINICI
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
        colore = ottieni_colore_bordo(lbl, val)
        col = cols[index % 3]
        with col:
            st.markdown(f'''
                <div class="metric-card" style="border-left: 6px solid {colore};">
                    <div class="metric-title">{lbl}</div>
                    <div class="metric-value">{val}</div>
                </div>
            ''', unsafe_allow_html=True)

# SEZIONE GRAFICO DI TENDENZA
st.markdown('<div class="section-header">📈 GRAFICI DI TENDENZA CLINICA</div>', unsafe_allow_html=True)

if df_c is not None and len(df_c) > 1:
    try:
        df_plot = df_c.copy()
        df_plot.columns = df_plot.iloc[0]
        df_plot = df_plot[1:]
        
        col_x = df_plot.columns[0]
        col_y = df_plot.columns[1]
        
        # Conversione data universale flessibile
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
            fig.update_traces(line_color='#2980B9', line_width=3, marker_size=7)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nessun dato numerico valido trovato nella Cronologia per generare il grafico.")
    except Exception as e:
        st.info("In attesa di sincronizzazione del grafico...")
else:
    st.info("Impossibile recuperare lo storico cronologia.")
