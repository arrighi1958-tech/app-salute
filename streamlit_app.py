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
            return ultimo_grezzo if ultimo_grezzo not in ["nan", "", "None", "#DIV/0!"] else "--"
            
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

press_sist = ottieni_valore(df_riep, ["sistole", "sistolica"], media_7gg=True)
press_diast = ottieni_valore(df_riep, ["diastole", "diastolica"], media_7gg=True)
fc_sonno = ottieni_valore(df_riep, ["fc sonno", "sonno", "riposo", "bpm sonno"], media_7gg=True)
fc_diurna = ottieni_valore(df_riep, ["fc diurna", "veglia", "diurna", "bpm diurna"], media_7gg=True)
fc_min_max = ottieni_valore(df_riep, ["range", "min", "max", "analisi"], e_testo=True)
ecg = ottieni_valore(df_riep, ["ecg", "tracciato"], e_testo=True)
spo2 = ottieni_valore(df_riep, ["spo2", "saturazione"], media_7gg=True)
ore_cpap = ottieni_valore(df_riep, ["cpap", "ore"], media_7gg=True)
risvegli = ottieni_valore(df_riep, ["risvegli", "nicturia"], media_7gg=True)
