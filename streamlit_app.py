import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Pannello Clinico Renato", page_icon="🩺", layout="wide")

# CSS DEDICATO
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
        margin-bottom: 4px;
    }
    
    .card-value {
        font-size: 24px;
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
URL_CRONOLOGIA = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=320500951"

@st.cache_data(ttl=2)
def carica_dati(url):
    try:
        return pd.read_csv(url, header=None)
    except Exception:
        return None

def analizza_parametro(label, valore):
    lbl = str(label).strip().lower()
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

    # B3: PASSI MEDIA SETTIMANALE
    if "passi" in lbl:
        if val_num is not None:
            if val_num >= 8000: return "border-green", "text-green", f"Target Raggiunto • {tipo_tempo}", 3
            if val_num >= 5000: return "border-yellow", "text-yellow", f"Livello Moderato • {tipo_tempo}", 3
        return "border-red", "text-red", f"Attività Bassa • {tipo_tempo}", 3

    # B5: PUNTEGGIO DI SALUTE ODIERNO
    if "punteggio di salute" in lbl:
        if val_num is not None:
            if val_num >= 75: return "border-green", "text-green", f"Ottimo Stato • {tipo_tempo}", 1
            if val_num >= 50: return "border-yellow", "text-yellow", f"Stato Moderato • {tipo_tempo}", 1
        return "border-red", "text-red", f"Attenzione Richiesta • {tipo_tempo}", 1

    # B7: FC TEMPO MEDIO SVEGLIO
    if "fc tempo medio" in lbl or "fc sveglio" in lbl:
        if val_num is not None:
            if 60 <= val_num <= 75: return "border-green", "text-green", f"FC Ottimale • {tipo_tempo}", 1
            if 76 <= val_num <= 85: return "border-yellow", "text-yellow", f"FC Accettabile • {tipo_tempo}", 1
        return "border-red", "text-red", f"FC Fuori Soglia • {tipo_tempo}", 1

    # B8: FC MEDIA DURANTE IL SONNO
    if "fc media" in lbl and "sonno" in lbl:
        if val_num is not None:
            if 50 <= val_num <= 65: return "border-green", "text-green", f"FC Notturna Ottimale • {tipo_tempo}", 1
            if 66 <= val_num <= 75: return "border-yellow", "text-yellow", f"FC Notturna Moderata • {tipo_tempo}", 1
        return "border-red", "text-red", f"FC Notturna Elevata • {tipo_tempo}", 1

    # B9 & B26: HRV E RAPPORTO HRV
    if "hrv" in lbl:
        if "rapporto" in lbl:
            if val_num is not None:
                if val_num >= 1.05: return "border-green", "text-green", f"Recupero Buono • {tipo_tempo}", 2
                if val_num >= 0.95: return "border-yellow", "text-yellow", f"Recupero Stabile • {tipo_tempo}", 2
            return "border-red", "text-red", f"Recupero Ridotto • {tipo_tempo}", 2
        else:
            if val_num is not None:
                if val_num >= 30: return "border-green", "text-green", f"Variabilità Buona • {tipo_tempo}", 2
                if val_num >= 15: return "border-yellow", "text-yellow", f"Variabilità Moderata • {tipo_tempo}", 2
            return "border-red", "text-red", f"Variabilità Bassa • {tipo_tempo}", 2

    # B10: SPO2 DURANTE IL SONNO
    if "spo2" in lbl or "saturazione" in lbl:
        if val_num is not None:
            if val_num >= 95: return "border-green", "text-green", f"Saturazione Ottimale • {tipo_tempo}", 1
            if val_num >= 90: return "border-yellow", "text-yellow", f"Saturazione Moderata • {tipo_tempo}", 1
        return "border-red", "text-red", f"Saturazione Bassa • {tipo_tempo}", 1

    # B11 & B12: PRESSIONE ARTERIOSA
    if "sistole" in lbl:
        if val_num is not None:
            if 115 <= val_num <= 130: return "border-green", "text-green", f"Sistole Ottimale • {tipo_tempo}", 1
            if 131 <= val_num <= 140: return "border-yellow", "text-yellow", f"Sistole Borderline • {tipo_tempo}", 1
        return "border-red", "text-red", f"Sistole Fuori Soglia • {tipo_tempo}", 1

    if "diastolica" in lbl:
        if val_num is not None:
            if 70 <= val_num <= 79: return "border-green", "text-green", f"Diastole Ottimale • {tipo_tempo}", 1
            if 80 <= val_num <= 89: return "border-yellow", "text-yellow", f"Diastole Borderline • {tipo_tempo}", 1
        return "border-red", "text-red", f"Diastole Fuori Soglia • {tipo_tempo}", 1

    # B13: ECG
    if "ecg" in lbl or "tracciato" in lbl:
        if "sinusale" in val_str: return "border-green", "text-green", f"Ritmo Sinusale • {tipo_tempo}", 1
        if "inconcludente" in val_str: return "border-yellow", "text-yellow", f"Esito Inconcludente • {tipo_tempo}", 1
        return "border-red", "text-red", f"Anomalia Rilevata • {tipo_tempo}", 1

    # B14: STRESS
    if "stress" in lbl:
        if "ottimale" in val_str or (val_num is not None and val_num < 30):
            return "border-green", "text-green", f"Stress Basso • {tipo_tempo}", 2
        if "moderato" in val_str or (val_num is not None and val_num <= 60):
            return "border-yellow", "text-yellow", f"Stress Moderato • {tipo_tempo}", 2
        return "border-red", "text-red", f"Stress Elevato • {tipo_tempo}", 2

    # B15: VO2 MAX
    if "vo2" in lbl:
        if val_num is not None:
            if val_num >= 40: return "border-green", "text-green", f"Capacità Ottima • {tipo_tempo}", 3
            if val_num > 30: return "border-yellow", "text-yellow", f"Capacità Media • {tipo_tempo}", 3
        return "border-red", "text-red", f"Capacità Bassa • {tipo_tempo}", 3

    # B17, B18, B19, B20, B24: PARAMETRI SONNO
    if "interruzioni" in lbl or "risvegli" in lbl:
        if val_num is not None:
            if val_num < 1.5: return "border-green", "text-green", f"Sonno Continuo • {tipo_tempo}", 2
            if val_num <= 3: return "border-yellow", "text-yellow", f"Interruzioni Moderate • {tipo_tempo}", 2
        return "border-red", "text-red", f"Interruzioni Frequenti • {tipo_tempo}", 2

    if "ore di sonno" in lbl or "ore sonno profondo" in lbl:
        if "profondo" in lbl:
            if val_num is not None:
                if val_num > 1.5: return "border-green", "text-green", f"Profondo Ottimale • {tipo_tempo}", 2
                if val_num >= 0.9: return "border-yellow", "text-yellow", f"Profondo Sufficiente • {tipo_tempo}", 2
            return "border-red", "text-red", f"Profondo Insufficiente • {tipo_tempo}", 2
        else:
            if val_num is not None:
                if 7 <= val_num <= 9: return "border-green", "text-green", f"Durata Ottimale • {tipo_tempo}", 2
                if 6 <= val_num < 7: return "border-yellow", "text-yellow", f"Durata Accettabile • {tipo_tempo}", 2
            return "border-red", "text-red", f"Durata Insufficiente • {tipo_tempo}", 2

    if "punteggio sonno" in lbl or "qualità del sonno" in lbl:
        if val_num is not None:
            pct = val_num if val_num > 1 else val_num * 100
            if pct >= 85: return "border-green", "text-green", f"Qualità Ottima • {tipo_tempo}", 2
            if pct >= 60: return "border-yellow", "text-yellow", f"Qualità Accettabile • {tipo_tempo}", 2
        return "border-red", "text-red", f"Qualità Bassa • {tipo_tempo}", 2

    # B21, B22, B23, B25, B33, B34: TEMPERATURA E RESPIRAZIONE
    if "temperatura" in lbl:
        if val_num is not None:
            if 35.0 <= val_num <= 36.9: return "border-green", "text-green", f"Temp. Normale • {tipo_tempo}", 2
            if val_num > 37.0: return "border-red", "text-red", f"Temp. Elevata • {tipo_tempo}", 2
        return "border-yellow", "text-yellow", f"Temp. da Monitorare • {tipo_tempo}", 2

    if "qualità respiratoria" in lbl:
        if "ottimale" in val_str: return "border-green", "text-green", f"Respirazione Ottima • {tipo_tempo}", 2
        if "accettabile" in val_str: return "border-yellow", "text-yellow", f"Respirazione Accettabile • {tipo_tempo}", 2
        return "border-red", "text-red", f"Da Migliorare • {tipo_tempo}", 2

    if "profondità del sonno" in lbl:
        if "buono" in val_str: return "border-green", "text-green", f"Livello Buono • {tipo_tempo}", 2
        if "media" in val_str: return "border-yellow", "text-yellow", f"Livello Medio • {tipo_tempo}", 2
        return "border-red", "text-red", f"Livello Scarso • {tipo_tempo}", 2

    if "frequenza respiratoria" in lbl:
        if "minima" in lbl:
            if is_media_7gg: # B34
                if val_num is not None:
                    if val_num >= 12: return "border-green", "text-green", f"Resp. Minima Stabile • {tipo_tempo}", 2
                    if val_num >= 10: return "border-yellow", "text-yellow", f"Resp. Minima Bassa • {tipo_tempo}", 2
                return "border-red", "text-red", f"Resp. Minima Critica • {tipo_tempo}", 2
            else: # B33
                if val_num is not None and val_num >= 10:
                    return "border-green", "text-green", f"Resp. Minima Regolare • {tipo_tempo}", 2
                return "border-red", "text-red", f"Resp. Minima Bassa • {tipo_tempo}", 2
        else: # B25
            if val_num is not None:
                if 12 <= val_num <= 18: return "border-green", "text-green", f"Frequenza Regolare • {tipo_tempo}", 2
                if 18 < val_num <= 20: return "border-yellow", "text-yellow", f"Frequenza Moderata • {tipo_tempo}", 2
            return "border-red", "text-red", f"Frequenza Anomala • {tipo_tempo}", 2

    # B27 & B28: RECUPERO FISICO E MENTALE
    if "recupero" in lbl:
        if val_num is not None:
            if val_num >= 70: return "border-green", "text-green", f"Recupero Ottimo • {tipo_tempo}", 2
            if val_num >= 50: return "border-yellow", "text-yellow", f"Recupero Medio • {tipo_tempo}", 2
        return "border-red", "text-red", f"Recupero Insufficiente • {tipo_tempo}", 2

    # B29 & B31: APNEE & CPAP
    if "apnea" in lbl:
        if "basso" in val_str or "assente" in val_str:
            return "border-green", "text-green", f"Rischio Basso • {tipo_tempo}", 1
        if "moderato" in val_str or "monitorare" in val_str:
            return "border-yellow", "text-yellow", f"Rischio Moderato • {tipo_tempo}", 1
        return "border-red", "text-red", f"Rischio Elevato • {tipo_tempo}", 1

    if "cpap" in lbl:
        if val_num is not None:
            if val_num >= 0.25 or val_num >= 6.0: return "border-green", "text-green", f"Aderenza Ottima (≥6h) • {tipo_tempo}", 1
            if val_num >= 0.1667 or val_num >= 4.0: return "border-yellow", "text-yellow", f"Aderenza Media (4-6h) • {tipo_tempo}", 1
        return "border-red", "text-red", f"Aderenza Bassa (<4h) • {tipo_tempo}", 1

    # B30: FC MAX E MIN
    if "fc max" in lbl or "massima e minima" in lbl:
        if "-" in val_str:
            try:
                parti = val_str.split("-")
                f_min = float(parti[0].strip())
                f_max = float(parti[1].strip())
                if f_min < 40 or f_max > 150:
                    return "border-red", "text-red", f"Valori Fuori Soglia • {tipo_tempo}", 1
            except ValueError:
                pass
        return "border-green", "text-green", f"Limiti Sicuri • {tipo_tempo}", 1

    # B32: OBIETTIVI ATTIVITÀ
    if "obiettivi attività" in lbl:
        if "raggiunto" in val_str and "quasi" not in val_str: return "border-green", "text-green", f"Target Raggiunto • {tipo_tempo}", 3
        if "quasi" in val_str: return "border-yellow", "text-yellow", f"Quasi Raggiunto • {tipo_tempo}", 3
        return "border-red", "text-red", f"Da Incrementare • {tipo_tempo}", 3

    # DEFAULT INFORMATIVO
    return "border-blue", "text-blue", f"Parametro Generale • {tipo_tempo}", 3

df_p = carica_dati(URL_PANNELLO)
df_c = carica_dati(URL_CRONOLOGIA)

st.title("🩺 Scheda Clinica e Monitoraggio")

if df_p is not None:
    gruppo_vitali = []
    gruppo_sonno = []
    gruppo_generale = []
    
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

# GRAFICO STORICO
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
                title=f"Andamento Storico: {col_y}",
                labels={col_x: "Data", col_y: "Valore"}
            )
            fig.update_traces(line_color='#2980B9', line_width=3, marker_size=6)
            st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.info("Aggiornamento grafico in corso...")
