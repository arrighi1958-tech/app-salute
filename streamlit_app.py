import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIGURAZIONE PAGINA
st.set_page_config(page_title="Pannello di Controllo Generale", page_icon="🩺", layout="wide")

# STILI CSS PER CARD E BANNER
st.markdown("""
    <style>
    .stApp { background-color: #F4F6F9; }
    
    .profile-card {
        background-color: #EBF5FB;
        border-left: 6px solid #2980B9;
        border-radius: 10px;
        padding: 15px 18px;
        margin-bottom: 25px;
        color: #1B4F72;
        font-size: 14px;
        line-height: 1.5;
    }

    .card-container {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 14px;
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
        font-size: 22px;
        font-weight: 800;
        color: #111111;
        margin-bottom: 4px;
    }
    
    .card-subtitle {
        font-size: 11px;
        font-weight: 600;
    }

    /* COLORI FORMATTAZIONE CONDIZIONALE FOGLIO PANNELLO */
    .bg-green { border-left-color: #2ECC71; }
    .text-green { color: #27AE60; }

    .bg-yellow { border-left-color: #F1C40F; }
    .text-yellow { color: #D4AC0D; }

    .bg-red { border-left-color: #E74C3C; }
    .text-red { color: #C0392B; }

    .bg-blue { border-left-color: #3498DB; }
    .text-blue { color: #2980B9; }

    .section-header {
        font-size: 16px; font-weight: 800; color: #1B4F72; margin-top: 22px;
        margin-bottom: 14px; border-bottom: 2px solid #2980B9; padding-bottom: 4px;
    }
    </style>
""", unsafe_allow_html=True)

SHEET_ID = "1sKNtsluKQKPwqA-YToNexsHa0Gu7-Nnx8pCv628qeog"
URL_PANNELLO = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
URL_WITHINGS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=320500951"

@st.cache_data(ttl=2)
def carica_dati(url):
    try:
        return pd.read_csv(url, header=None)
    except Exception:
        return None

# LOGICA DI FORMATTAZIONE CONDIZIONALE PER OGNI RIGA DEL PANNELLO
def calcola_formattazione_condizionale(label, valore):
    lbl = str(label).strip().lower()
    val_str = str(valore).strip().lower()

    val_num = None
    try:
        clean_val = val_str.replace('%', '').replace(',', '.').strip()
        val_num = float(clean_val)
    except ValueError:
        pass

    # PRESSIONE UNIFICATA
    if "pressione arteriosa" in lbl:
        try:
            parti = val_str.replace("mmhg", "").strip().split("/")
            sist = float(parti[0].replace(',', '.').strip())
            diast = float(parti[1].replace(',', '.').strip())
            if sist <= 130 and diast <= 85:
                return "bg-green", "text-green", "Target Clinico Ipertensione Rispettato"
            if sist <= 140 and diast <= 90:
                return "bg-yellow", "text-yellow", "Valore Borderline"
            return "bg-red", "text-red", "Pressione Elevata"
        except Exception:
            return "bg-green", "text-green", "Target Clinico Ipertensione"

    # B3: PASSI MEDIA SETTIMANALE
    if "passi media settimanale" in lbl:
        if val_num is not None:
            if val_num >= 8000: return "bg-green", "text-green", "Target Raggiunto"
            if val_num >= 5000: return "bg-yellow", "text-yellow", "Livello Moderato"
        return "bg-red", "text-red", "Attività Bassa"

    # B4: NUMERO GIORNI ANALIZZATI
    if "numero giorni analizzati" in lbl:
        return "bg-blue", "text-blue", "Dati Storici"

    # B5: PUNTEGGIO DI SALUTE ODIERNO
    if "punteggio di salute" in lbl:
        if val_num is not None:
            if val_num >= 75: return "bg-green", "text-green", "Stato Ottimale"
            if val_num >= 50: return "bg-yellow", "text-yellow", "Stato Moderato"
        return "bg-red", "text-red", "Attenzione Richiesta"

    # B7: FC TEMPO MEDIO SVEGLIO
    if "fc tempo medio sveglio" in lbl:
        if val_num is not None:
            if 60 <= val_num <= 75: return "bg-green", "text-green", "Ottimale"
            if 76 <= val_num <= 85: return "bg-yellow", "text-yellow", "Moderata"
        return "bg-red", "text-red", "Fuori Soglia"

    # B8: FC MEDIA DURANTE IL SONNO
    if "fc media durante il sonno" in lbl:
        if val_num is not None:
            if 50 <= val_num <= 65: return "bg-green", "text-green", "Ottimale Notturna"
            if 66 <= val_num <= 75: return "bg-yellow", "text-yellow", "Moderata Notturna"
        return "bg-red", "text-red", "Elevata Notturna"

    # B9: HRV DURANTE IL SONNO
    if "hrv durante il sonno" in lbl:
        if val_num is not None:
            if val_num >= 30: return "bg-green", "text-green", "Buona Variabilità"
            if val_num >= 15: return "bg-yellow", "text-yellow", "Variabilità Moderata"
        return "bg-red", "text-red", "Variabilità Bassa"

    # B10: SPO2 DURANTE IL SONNO
    if "spo2 durante il sonno" in lbl:
        if val_num is not None:
            if val_num >= 95: return "bg-green", "text-green", "Saturazione Ottimale"
            if val_num >= 90: return "bg-yellow", "text-yellow", "Saturazione Moderata"
        return "bg-red", "text-red", "Saturazione Bassa"

    # B13: ECG ULTIMO ESITO
    if "ecg" in lbl:
        if "sinusale" in val_str: return "bg-green", "text-green", "Ritmo Sinusale"
        if "inconcludente" in val_str: return "bg-yellow", "text-yellow", "Inconcludente"
        return "bg-red", "text-red", "Anomalia"

    # B14: LIVELLO DI STRESS STIMATO
    if "livello di stress" in lbl:
        if "moderato" in val_str or "riposo attivo" in val_str:
            return "bg-yellow", "text-yellow", "Consigliato Riposo Attivo"
        if "basso" in val_str or "ottimale" in val_str:
            return "bg-green", "text-green", "Stress Basso"
        return "bg-red", "text-red", "Stress Elevato"

    # B15: LIVELLO DI FITNESS VO2 MAX
    if "vo2 max" in lbl or "vo2" in lbl:
        if val_num is not None:
            if val_num >= 30: return "bg-green", "text-green", "Buona Capacità"
            if val_num >= 20: return "bg-yellow", "text-yellow", "Capacità Moderata"
        return "bg-red", "text-red", "Capacità Ridotta (<20)"

    # B17: MEDIA ORE DI SONNO
    if "media ore di sonno" in lbl:
        if val_num is not None:
            if 7 <= val_num <= 9: return "bg-green", "text-green", "Ottimale"
            if 6 <= val_num < 7: return "bg-yellow", "text-yellow", "Accettabile"
        return "bg-red", "text-red", "Insufficiente (<6h)"

    # B18: MEDIA PUNTEGGIO SONNO
    if "media punteggio sonno" in lbl:
        if val_num is not None:
            if val_num >= 75: return "bg-green", "text-green", "Buono"
            if val_num >= 60: return "bg-yellow", "text-yellow", "Moderato"
        return "bg-red", "text-red", "Scarso"

    # B19: INTERRUZIONI NOTTURNE
    if "interruzioni notturne" in lbl:
        if val_num is not None:
            if val_num < 1.5: return "bg-green", "text-green", "Minime"
            if val_num <= 3.0: return "bg-yellow", "text-yellow", "Moderate"
        return "bg-red", "text-red", "Frequenti"

    # B20: PUNTEGGIO DI QUALITÀ DEL SONNO
    if "punteggio di qualità del sonno" in lbl:
        if val_num is not None:
            pct = val_num if val_num > 1 else val_num * 100
            if pct >= 80: return "bg-green", "text-green", "Ottimo"
            if pct >= 60: return "bg-yellow", "text-yellow", "Sufficiente"
        return "bg-red", "text-red", "Insoddisfacente"

    # B21: TEMPERATURA DEL SONNO
    if "temperatura del sonno" in lbl:
        if val_num is not None:
            if 35.5 <= val_num <= 36.8: return "bg-green", "text-green", "Normale"
        return "bg-yellow", "text-yellow", "Da Monitorare"

    # B22: QUALITÀ RESPIRATORIA
    if "qualità respiratoria" in lbl:
        if "ottimale" in val_str: return "bg-green", "text-green", "Ottimale"
        return "bg-yellow", "text-yellow", "Accettabile"

    # B23: PROFONDITÀ DEL SONNO GIUDIZIO
    if "profondità del sonno giudizio" in lbl:
        if "buono" in val_str: return "bg-green", "text-green", "Buono"
        if "medio" in val_str: return "bg-yellow", "text-yellow", "Medio"
        return "bg-red", "text-red", "Scarso"

    # B24: MEDIA ORE SONNO PROFONDO
    if "media ore sonno profondo" in lbl:
        if val_num is not None:
            if val_num >= 1.5: return "bg-green", "text-green", "Ottimale"
            if val_num >= 1.0: return "bg-yellow", "text-yellow", "Sufficiente"
        return "bg-red", "text-red", "Scarso"

    # B25: FREQUENZA RESPIRATORIA MEDIA NOTTURNA
    if "frequenza respiratoria media notturna" in lbl:
        if val_num is not None:
            if 12 <= val_num <= 18: return "bg-green", "text-green", "Regolare"
        return "bg-yellow", "text-yellow", "Alterata"

    # B26: RAPPORTO RECUPERO HRV
    if "rapporto recupero hrv" in lbl:
        if val_num is not None:
            if val_num >= 1.05: return "bg-green", "text-green", "Buono"
            if val_num >= 0.95: return "bg-yellow", "text-yellow", "Stabile"
        return "bg-red", "text-red", "Ridotto"

    # B27 & B28: RECUPERO FISICO E MENTALE
    if "punteggio di recupero" in lbl:
        if val_num is not None:
            if val_num >= 70: return "bg-green", "text-green", "Ottimo"
            if val_num >= 50: return "bg-yellow", "text-yellow", "Moderato"
        return "bg-red", "text-red", "Basso"

    # B29: MONITORAGGIO RISCHIO APNEA NOTTURNA
    if "apnea" in lbl:
        if "basso" in val_str or "assente" in val_str: return "bg-green", "text-green", "Rischio Basso / Assente"
        return "bg-yellow", "text-yellow", "Rischio Moderato"

    # B30: ANALISI FC MASSIMA E MINIMA
    if "analisi fc massima e minima" in lbl:
        return "bg-red", "text-red", "Ampia Escursione (38 - 155)"

    # B31: MEDIA ORE UTILIZZO CPAP
    if "cpap" in lbl:
        if val_num is not None:
            if val_num >= 6.0: return "bg-green", "text-green", "Aderenza Buona (≥6h)"
            if val_num >= 4.0: return "bg-yellow", "text-yellow", "Aderenza Parziale"
        return "bg-red", "text-red", "Aderenza Insufficiente (<4h)"

    # B32: RAGGIUNGIMENTO OBIETTIVI ATTIVITÀ
    if "raggiungimento obiettivi attività" in lbl:
        if "target raggiunto" in val_str: return "bg-green", "text-green", "Target Raggiunto"
        return "bg-yellow", "text-yellow", "In Corso"

    # B33 & B34: FREQUENZA RESPIRATORIA MINIMA SONNO
    if "frequenza respiratoria minima sonno" in lbl:
        if "media 7" in lbl:
            if val_num is not None and val_num >= 12: return "bg-green", "text-green", "Media 7gg Regolare"
            return "bg-yellow", "text-yellow", "Media 7gg Bassa"
        else:
            if val_num is not None and val_num >= 10: return "bg-green", "text-green", "Giornaliera Regolare"
            return "bg-red", "text-red", "Giornaliera Bassa"

    # DEFAULT
    return "bg-blue", "text-blue", "Valore Registrato"

# CARICAMENTO DATI
df_p = carica_dati(URL_PANNELLO)
df_w = carica_dati(URL_WITHINGS)

st.title("🩺 Scheda Clinica e Monitoraggio")

st.markdown("""
    <div class="profile-card">
        <strong>PROFILO PAZIENTE (68 anni):</strong> Monitoraggio Terapia Anti-ipertensiva, Betabloccante (Bradicardia), Prostata/Nicturia e Terapia Ventilatoria CPAP.
    </div>
""", unsafe_allow_html=True)

# RENDERING DINAMICO CON UNIFICAZIONE PRESSIONE
if df_p is not None:
    items_salute = []
    items_sonno = []
    items_attivita = []

    sistole_val = None
    diastole_val = None

    for idx, row in df_p.iterrows():
        if len(row) >= 2 and pd.notna(row[0]) and str(row[0]).strip() != "":
            label = str(row[0]).strip()
            valore = str(row[1]).strip() if pd.notna(row[1]) else "--"

            lbl_lower = label.lower()

            if label.lower() in ["stile di vita e attività", "salute del cuore (medie storiche)", "qualità del sonno e recupero", "pannello di controllo generale", "date (data)"]:
                continue

            # INTERCETTA SISTOLE E DIASTOLE PER UNIRLE
            if "sistole" in lbl_lower:
                sistole_val = valore
                continue
            if "diastolica" in lbl_lower:
                diastole_val = valore
                continue

            bg_class, text_class, note = calcola_formattazione_condizionale(label, valore)
            item_tuple = (label, valore, bg_class, text_class, note)

            if "fc tempo medio" in lbl_lower or "ecg" in lbl_lower or "salute" in lbl_lower or "stress" in lbl_lower or "apnea" in lbl_lower:
                items_salute.append(item_tuple)
            elif "sonno" in lbl_lower or "risvegli" in lbl_lower or "temperatura" in lbl_lower or "respirat" in lbl_lower or "recupero" in lbl_lower or "cpap" in lbl_lower or "hrv" in lbl_lower:
                items_sonno.append(item_tuple)
            else:
                items_attivita.append(item_tuple)

    # SE PRESENTI SISTOLE E DIASTOLE, CREA LA CARD PRESSIONE UNIFICATA IN CIMA A SALUTE
    if sistole_val and diastole_val:
        press_val = f"{sistole_val} / {diastole_val} mmHg"
        bg_class, text_class, note = calcola_formattazione_condizionale("Pressione Arteriosa", press_val)
        items_salute.insert(0, ("Pressione Arteriosa (Media 7gg)", press_val, bg_class, text_class, note))

    # SEZIONE 1: SALUTE E VITALI
    if items_salute:
        st.markdown('<div class="section-header">🚨 SALUTE DEL CUORE E PARAMETRI VITALI</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for index, (lbl, val, bg_c, txt_c, note) in enumerate(items_salute):
            with cols[index % 3]:
                st.markdown(f'''
                    <div class="card-container {bg_c}">
                        <div class="card-title">{lbl}</div>
                        <div class="card-value">{val}</div>
                        <div class="card-subtitle {txt_c}">{note}</div>
                    </div>
                ''', unsafe_allow_html=True)

    # SEZIONE 2: SONNO E RECUPERO
    if items_sonno:
        st.markdown('<div class="section-header">🌙 QUALITÀ DEL SONNO E RECUPERO</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for index, (lbl, val, bg_c, txt_c, note) in enumerate(items_sonno):
            with cols[index % 3]:
                st.markdown(f'''
                    <div class="card-container {bg_c}">
                        <div class="card-title">{lbl}</div>
                        <div class="card-value">{val}</div>
                        <div class="card-subtitle {txt_c}">{note}</div>
                    </div>
                ''', unsafe_allow_html=True)

    # SEZIONE 3: STILE DI VITA ED ATTIVITÀ
    if items_attivita:
        st.markdown('<div class="section-header">🏃 STILE DI VITA ED ATTIVITÀ</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for index, (lbl, val, bg_c, txt_c, note) in enumerate(items_attivita):
            with cols[index % 3]:
                st.markdown(f'''
                    <div class="card-container {bg_c}">
                        <div class="card-title">{lbl}</div>
                        <div class="card-value">{val}</div>
                        <div class="card-subtitle {txt_c}">{note}</div>
                    </div>
                ''', unsafe_allow_html=True)

# SEZIONE GRAFICO CON MENU A TENDINA (STORICO DATI_WITHINGS)
st.markdown('<div class="section-header">📈 GRAFICI DI TENDENZA CLINICA</div>', unsafe_allow_html=True)

if df_w is not None and len(df_w) > 1:
    try:
        df_plot = df_w.copy()
        df_plot.columns = df_plot.iloc[0]
        df_plot = df_plot[1:]
        
        col_x = df_plot.columns[0]
        df_plot[col_x] = pd.to_datetime(df_plot[col_x], dayfirst=True, errors='coerce')
        
        opzioni_grafico = [col for col in df_plot.columns[1:] if str(col).strip() != "" and str(col).strip().lower() != "nan"]
        
        parametro_scelto = st.selectbox(
            "Seleziona il parametro da analizzare nel tempo:", 
            options=opzioni_grafico
        )
        
        if parametro_scelto:
            df_plot[parametro_scelto] = pd.to_numeric(
                df_plot[parametro_scelto].astype(str).str.replace('%', '').str.replace(',', '.'), 
                errors='coerce'
            )
            
            df_clean = df_plot.dropna(subset=[col_x, parametro_scelto]).sort_values(by=col_x)
            
            if not df_clean.empty:
                fig = px.line(
                    df_clean, 
                    x=col_x, 
                    y=parametro_scelto, 
                    markers=True, 
                    title=f"Andamento Storico: {parametro_scelto}",
                    labels={col_x: "Data", parametro_scelto: "Valore"}
                )
                fig.update_traces(line_color='#2980B9', line_width=3, marker_size=6)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Nessun dato numerico valido trovato per il parametro selezionato.")
                
    except Exception:
        st.info("Impossibile caricare il grafico dei dati storici.")
