# FUNZIONE ESTRAZIONE DATI MIGLIORATA PER GESTIRE PUNTI E FORMATI TESTO/NUMERO
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
            
        # Pulisce la stringa rimuovendo punti delle migliaia e convertendo virgole
        serie_pulita = df[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
        serie_num = pd.to_numeric(serie_pulita, errors='coerce').dropna()
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
