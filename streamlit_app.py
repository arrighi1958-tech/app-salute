import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Pannello Clinico Renato", page_icon="🩺", layout="wide")

# CSS DEDICATO STILE CLINICO
st.markdown("""
    <style>
    .stApp { background-color: #F4F6F9; }
    
    /* SCHEDA PROFILO PAZIENTE */
    .patient-header {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-left: 8px solid #1B4F72;
    }
    .patient-title {
        font-size: 20px;
        font-weight: 800;
        color: #1B4F72;
        margin-bottom: 8px;
    }
    .patient-info {
        font-size: 14px;
        color: #2C3E50;
        line-height: 1.6;
    }
    .badge-tag {
        background-color: #EBF5FB;
        color: #1B4F72;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 12px;
        margin-right: 6px;
        display: inline-block;
        margin-bottom: 4px;
    }

    /* CARD PARAMETRI */
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
        margin-bottom: 4px;
    }
    
    .card-value {
        font-size: 26px;
        font-weight: 800;
        color: #111111;
        margin-bottom: 4px;
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
        font-size: 17px; font-weight: 800; color: #1B4F72; margin-top: 20px;
        margin-bottom: 15px; border-bottom: 2px solid #2980B9; padding-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

SHEET_ID = "1sKNtsluKQKPwqA-YToNexsHa0Gu7-Nnx8pCv628qeog"

URL_PANNELLO = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
URL_WITHINGS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=320500951"

@st.cache_data(ttl=2)
def carica_pannello(url):
    try:
        return pd.read_csv(url, header=None)
    except Exception:
        return None

@st.cache_data(ttl=2)
def carica_withings(url):
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except Exception:
        return None

def converti_ore_decimale(val):
    val_str = str(val).strip().replace(',', '.')
    if ':' in val_str:
        parts = val_str.split(':')
        ore = float(parts[0]) if len(parts) > 0 and parts[0].isdigit() else 0
        minuti = float(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        return round(ore + (minuti / 60), 2)
    try:
        return float(val_str)
    except ValueError:
        return 0.0

def analizza_parametro(label, valore):
    lbl = str(label).lower()
    val_str = str(valore).strip().lower()
    
    is_media_7gg = "7gg" in lbl or "media" in lbl or "settimanale" in lbl
    tipo_tempo = "(Media 7 giorni)" if is_media_7gg else "(Valore Giornaliero)"

    val_num = None
    try:
        clean_val = val_str.replace('%', '').replace(',', '.').strip()
        val_num = float(clean_val)
    except ValueError:
        pass

    if val_str in ["--", "", "nan", "none", "n/a"]:
        return "border-red", "text-red", f"Dato non registrato • {tipo_tempo}", 1

    if "spo2" in lbl or "saturazione" in lbl:
        if val_num is not None and val_num < 95.0:
            return "border-red", "text-red", f"Saturazione bassa under-CPAP • {tipo_tempo}", 1
        return "border-green", "text-green", f"Efficienza respiratoria notturna • {tipo_tempo}", 1

    if "sistole" in lbl or "diastolica" in lbl or "pressione" in lbl:
        if val_num is not None and val_num > 135:
            return "border-red", "text-red", f"Pressione elevata • {tipo_tempo}", 1
        elif val_num is not None and val_num > 125:
            return "border-yellow", "text-yellow", f"Pressione borderline • {tipo_tempo}", 1
        return "border-green", "text-green", f"Pressione nella norma • {tipo_tempo}", 1

    if "ecg" in lbl or "tracciato" in lbl:
        if "sinusale" in val_str:
            return "border-blue", "text-blue", f"Ritmo Sinusale / Regolare • {tipo_tempo}", 1
        return "border-red", "text-red", f"Anomalia ritmo rilevata • {tipo_tempo}", 1

    if "cpap" in lbl:
        if val_num is not None and val_num < 4.0:
            return "border-red", "text-red", f"Aderenza CPAP insufficiente (<4h) • {tipo_tempo}", 1
        elif val_num is not None and val_num < 6.0:
            return "border-yellow", "text-yellow", f"Aderenza CPAP moderata • {tipo_tempo}", 1
        return "border-green", "text-green", f"Aderenza terapia ventilatoria • {tipo_tempo}", 1

    if "risvegli" in lbl or "interruzioni" in lbl:
        if val_num is not None and val_num > 4.0:
            return "border-red", "text-red", f"Risvegli frequenti • {tipo_tempo}", 2
        elif val_num is not None and val_num >= 2.0:
            return "border-yellow", "text-yellow", f"Interruzioni notturne / prostata • {tipo_tempo}", 2
        return "border-green", "text-green", f"Continuità sonno ottimale • {tipo_tempo}", 2

    if "hrv" in lbl or "stress" in lbl:
        if "moderato" in val_str or (val_num is not None and val_num < 20):
            return "border-yellow", "text-yellow", f"Consigliato riposo attivo • {tipo_tempo}", 2
        return "border-green", "text-green", f"Livello di recupero idoneo • {tipo_tempo}", 2

    if "passi" in lbl or "target" in lbl:
        return "border-green", "text-green", f"Obiettivo movimento • {tipo_tempo}", 3

    return "border-blue", "text-blue", f"Parametro generale • {tipo_tempo}", 3

df_p = carica_pannello(URL_PANNELLO)
df_w = carica_withings(URL_WITHINGS)

st.title("🩺 Scheda Clinica e Monitoraggio")

# SEZIONE PROFILO PAZIENTE
st.markdown("""
    <div class="patient-header">
        <div class="patient-title">👤 Profilo Paziente — 68 Anni</div>
        <div class="patient-info">
            <b>Quadri clinici e terapie in corso:</b><br>
            <span class="badge-tag">Terapia Antipertensiva</span>
            <span class="badge-tag">Beta-Bloccanti (Bradicardia)</span>
            <span class="badge-tag">Terapia Anticoagulante a Vita</span>
            <span class="badge-tag">Terapia Ventilatoria CPAP</span>
            <span class="badge-tag">Prostata / Nicturia</span>
        </div>
    </div>
""", unsafe_allow_html=True)

if df_p is not None:
    gruppo_vitali, gruppo_sonno, gruppo_generale = [], [], []
    
    for idx, row in df_p.iterrows():
        if len(row) >= 2 and pd.notna(row[0]) and str(row[0]).strip() != "":
            label = str(row[0]).strip()
            valore = str(row[1]).strip() if pd.notna(row[1]) else "--"
            if valore != "--" and label.lower() not in ["date", "data", "date [data]"]:
                cls_b, cls_t, nota, priorita = analizza_parametro(label, valore)
                item = (label, valore, cls_b, cls_t, nota)
                
                if priorita == 1:
                    gruppo_vitali.append(item)
                elif priorita == 2:
                    gruppo_sonno.append(item)
                else:
                    gruppo_generale.append(item)

    if gruppo_vitali:
        st.markdown('<div class="section-header">🚨 PARAMETRI VITALI E TERAPIA (Priorità Medica)</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for index, (lbl, val, cls_b, cls_t, nota) in enumerate(gruppo_vitali):
            with cols[index % 3]:
                st.markdown(f'''
                    <div class="card-container {cls_b}">
                        <div class="card-title">{lbl}</div>
                        <div class="card-value">{val}</div>
                        <div class="card-subtitle {cls_t}">{nota}</div>
                    </div>
                ''', unsafe_allow_html=True)

    if gruppo_sonno:
        st.markdown('<div class="section-header">🌙 SONNO, RESPIRAZIONE E RECUPERO</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for index, (lbl, val, cls_b, cls_t, nota) in enumerate(gruppo_sonno):
            with cols[index % 3]:
                st.markdown(f'''
                    <div class="card-container {cls_b}">
                        <div class="card-title">{lbl}</div>
                        <div class="card-value">{val}</div>
                        <div class="card-subtitle {cls_t}">{nota}</div>
                    </div>
                ''', unsafe_allow_html=True)

    if gruppo_generale:
        st.markdown('<div class="section-header">🏃 STILE DI VITA E ATTIVITÀ</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for index, (lbl, val, cls_b, cls_t, nota) in enumerate(gruppo_generale):
            with cols[index % 3]:
                st.markdown(f'''
                    <div class="card-container {cls_b}">
                        <div class="card-title">{lbl}</div>
                        <div class="card-value">{val}</div>
                        <div class="card-subtitle {cls_t}">{nota}</div>
                    </div>
                ''', unsafe_allow_html=True)

# SEZIONE GRAFICI CLINICI
st.markdown('<div class="section-header">📈 GRAFICI DI TENDENZA CLINICA</div>', unsafe_allow_html=True)

if df_w is not None and not df_w.empty:
    try:
        col_data = [c for c in df_w.columns if "date" in c.lower() or "data" in c.lower()][0]
        
        df_plot = df_w.copy()
        df_plot[col_data] = pd.to_datetime(df_plot[col_data], dayfirst=True, errors='coerce')
        df_plot = df_plot.dropna(subset=[col_data]).sort_values(by=col_data)

        opzione_grafico = st.selectbox(
            "Seleziona il quadro clinico da analizzare per il medico:",
            [
                "🫀 Pressione Arteriosa (Sistolica / Diastolica)",
                "🫁 Saturazione Ossigeno (SpO2 %) under-CPAP",
                "🌙 Interruzioni Notturne / Risvegli (Nicturia)",
                "⚡ Variabilità Cardiaca (HRV)",
                "🌬️ Ore Utilizzo CPAP",
                "📊 Punteggio Qualità del Sonno"
            ]
        )

        if "Pressione Arteriosa" in opzione_grafico:
            col_sist = [c for c in df_plot.columns if "sistole" in c.lower()][0]
            col_diast = [c for c in df_plot.columns if "dias" in c.lower()][0]
            
            df_plot[col_sist] = pd.to_numeric(df_plot[col_sist].astype(str).str.replace(',', '.'), errors='coerce')
            df_plot[col_diast] = pd.to_numeric(df_plot[col_diast].astype(str).str.replace(',', '.'), errors='coerce')
            
            fig = px.line(
                df_plot, x=col_data, y=[col_sist, col_diast],
                markers=True, title="Andamento Pressione Arteriosa (Sistolica / Diastolica)",
                labels={col_data: "Data", "value": "mmHg", "variable": "Parametro"}
            )
            fig.add_hline(y=135, line_dash="dash", line_color="red", annotation_text="Soglia Sistolica (135)")
            fig.add_hline(y=85, line_dash="dash", line_color="orange", annotation_text="Soglia Diastolica (85)")
            st.plotly_chart(fig, use_container_width=True)

        elif "Saturazione" in opzione_grafico:
            col_spo2 = [c for c in df_plot.columns if "spo2" in c.lower()][0]
            df_plot[col_spo2] = pd.to_numeric(df_plot[col_spo2].astype(str).str.replace(',', '.'), errors='coerce')
            
            fig = px.line(
                df_plot, x=col_data, y=col_spo2,
                markers=True, title="Andamento Saturazione Ossigeno (SpO2 %) under-CPAP",
                labels={col_data: "Data", col_spo2: "SpO2 %"}
            )
            fig.add_hline(y=95, line_dash="dash", line_color="green", annotation_text="Target Minimo (95%)")
            st.plotly_chart(fig, use_container_width=True)

        elif "Interruzioni" in opzione_grafico:
            col_risv = [c for c in df_plot.columns if "interruz" in c.lower() or "risvegl" in c.lower()][0]
            df_plot[col_risv] = pd.to_numeric(df_plot[col_risv].astype(str).str.replace(',', '.'), errors='coerce')
            
            fig = px.bar(
                df_plot, x=col_data, y=col_risv,
                title="Frequenza Interruzioni Notturne / Risvegli",
                labels={col_data: "Data", col_risv: "Numero Risvegli"}
            )
            st.plotly_chart(fig, use_container_width=True)

        elif "Variabilità Cardiaca" in opzione_grafico:
            col_hrv = [c for c in df_plot.columns if "hrv" in c.lower()][0]
            df_plot[col_hrv] = pd.to_numeric(df_plot[col_hrv].astype(str).str.replace(',', '.'), errors='coerce')
            
            fig = px.line(
                df_plot, x=col_data, y=col_hrv,
                markers=True, title="Variabilità della Frequenza Cardiaca (HRV)",
                labels={col_data: "Data", col_hrv: "HRV (ms)"}
            )
            st.plotly_chart(fig, use_container_width=True)

        elif "CPAP" in opzione_grafico:
            col_cpap = [c for c in df_plot.columns if "cpap" in c.lower()]
            nome_col = col_cpap[0]
            
            df_plot['CPAP_Numerico'] = df_plot[nome_col].apply(converti_ore_decimale)
            
            fig = px.bar(
                df_plot, x=col_data, y='CPAP_Numerico',
                title="Ore Terapia CPAP Utilizzate per Notte",
                labels={col_data: "Data", 'CPAP_Numerico': "Ore CPAP"}
            )
            fig.add_hline(y=4.0, line_dash="dash", line_color="red", annotation_text="Soglia Aderenza Minima (4 ore)")
            st.plotly_chart(fig, use_container_width=True)

        else:
            col_qual = [c for c in df_plot.columns if "punteggio" in c.lower() or "qualit" in c.lower()][0]
            df_plot[col_qual] = pd.to_numeric(df_plot[col_qual].astype(str).str.replace(',', '.'), errors='coerce')
            
            fig = px.line(
                df_plot, x=col_data, y=col_qual,
                markers=True, title=f"Andamento: {col_qual}",
                labels={col_data: "Data", col_qual: "Punteggio"}
            )
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Si è verificato un errore durante la lettura dei dati: {e}")
