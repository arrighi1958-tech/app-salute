import streamlit as st

# Configurazione della pagina per il Samsung A17
st.set_page_config(page_title="Pannello Salute Renato", page_icon="🩺", layout="centered")

st.markdown("""
    <style>
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.06);
        margin-bottom: 15px;
        border-left: 12px solid #cccccc;
    }
    .metric-title {
        font-size: 20px;
        font-weight: bold;
        color: #333333;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 38px;
        font-weight: 800;
        color: #111111;
    }
    .metric-status {
        font-size: 16px;
        font-weight: 600;
        margin-top: 4px;
    }
    .section-header {
        font-size: 24px;
        font-weight: bold;
        color: #1A5276;
        margin-top: 25px;
        margin-bottom: 15px;
        border-bottom: 2px solid #1A5276;
        padding-bottom: 5px;
    }
    .bg-verde { border-left-color: #2ECC71 !important; color: #27AE60; }
    .bg-giallo { border-left-color: #F1C40F !important; color: #D4AC0D; }
    .bg-rosso { border-left-color: #E74C3C !important; color: #C0392B; }
    </style>
""", unsafe_allow_html=True)

st.title("🩺 Cruscotto Salute Renato")
st.write("Visualizzazione ottimizzata per lo schermo del telefono")

tab_oggi, tab_medie, tab_trend = st.tabs(["Oggi (Pannello)", "Medie Storiche", "Trend"])

with tab_oggi:
    # === STILE DI VITA E ATTIVITÀ ===
    st.markdown('<div class="section-header">🏃 Stile di Vita e Attività</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Passi Settimanali</div>
            <div class="metric-value">5.782</div>
            <div class="metric-status">🟢 Obiettivo Minimo Raggiunto</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Giorni Totali Monitorati</div>
            <div class="metric-value">12 giorni</div>
            <div class="metric-status">🟢 Storico Attivo</div>
        </div>
    """, unsafe_allow_html=True)
    
    # === SALUTE DEL CUORE ===
    st.markdown('<div class="section-header">❤️ Salute del Cuore</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Frequenza Cardiaca Diurna</div>
            <div class="metric-value">67 bpm</div>
            <div class="metric-status">🟢 Regolare (ok)</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Frequenza Battiti a Riposo (7gg)</div>
            <div class="metric-value">53 bpm</div>
            <div class="metric-status">🟢 Eccellente Recupero (OK)</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Variabilità Cardiaca (HRV) (7gg)</div>
            <div class="metric-value">17 ms</div>
            <div class="metric-status">🟢 Bilanciato (ok)</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Ossigeno nel Sangue (SpO2)</div>
            <div class="metric-value">96,4 %</div>
            <div class="metric-status">🟢 Ottimale</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-giallo">
            <div class="metric-title">Media Pressione Sistolica (Massima)</div>
            <div class="metric-value">103 mmHg</div>
            <div class="metric-status">🟡 Attenzione (Leggermente Bassa)</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Pressione Diastolica (Minima)</div>
            <div class="metric-value">75 mmHg</div>
            <div class="metric-status">🟢 Ottimale</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Ultimo Esito ECG Registrato</div>
            <div class="metric-value">SINUSALE</div>
            <div class="metric-status">🟢 Regolare</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Livello di Stress Stimato (da HRV)</div>
            <div class="metric-value">Ottimale</div>
            <div class="metric-status">🟢 Stato di Riposo Ottimo</div>
        </div>
    """, unsafe_allow_html=True)
    # === QUALITÀ DEL SONNO E RECUPERO ===
    st.markdown('<div class="section-header">🌙 Qualità del Sonno e Recupero</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-rosso">
            <div class="metric-title">Media Ore di Sonno (7gg)</div>
            <div class="metric-value">5,97 ore</div>
            <div class="metric-status">🔴 Carenza Sonno (Sotto 6 ore)</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-giallo">
            <div class="metric-title">Media Punteggio Sonno Storico</div>
            <div class="metric-value">65 / 100</div>
            <div class="metric-status">🟡 Moderato</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Risvegli Notturni (7gg)</div>
            <div class="metric-value">3,1</div>
            <div class="metric-status">🟢 Nella Norma</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-giallo">
            <div class="metric-title">Efficienza del Sonno Media (7gg)</div>
            <div class="metric-value">64,69 %</div>
            <div class="metric-status">🟡 Monitorare Continuità</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Temperatura Corporea Storica</div>
            <div class="metric-value">36,45 °C</div>
            <div class="metric-status">🟢 Regolare</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Valutazione della Qualità Respiratoria</div>
            <div class="metric-value">Ottimale</div>
            <div class="metric-status">🟢 Assenza di Disturbi</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Stato Regolarità Ritmo Circadiano</div>
            <div class="metric-value">Buono</div>
            <div class="metric-status">🟢 Sonno Stabile</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Ore Sonno Profondo (7gg)</div>
            <div class="metric-value">1,6 ore</div>
            <div class="metric-status">🟢 Sbloccato</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Frequenza Respiratoria Notturna</div>
            <div class="metric-value">16 bpm</div>
            <div class="metric-status">🟢 Regolare</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Rapporto Recupero HRV (Fine vs Inizio)</div>
            <div class="metric-value">3,5</div>
            <div class="metric-status">🟢 Cuore Recuperato e Rilassato</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Punteggio di Recupero Fisico (PAI)</div>
            <div class="metric-value">73,0</div>
            <div class="metric-status">🟢 Buono Stato Fisico</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Punteggio di Recupero Mentale</div>
            <div class="metric-value">85 / 100</div>
            <div class="metric-status">🟢 Ottimo Stato Mentale</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Monitoraggio Rischio Apnea Notturna</div>
            <div class="metric-value">Basso</div>
            <div class="metric-status">🟢 Sicuro</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-rosso">
            <div class="metric-title">Picco Frequenza Cardiaca Massima (7gg)</div>
            <div class="metric-value">137 bpm</div>
            <div class="metric-status">🔴 Picco Elevato</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Ore Utilizzo CPAP (7gg)</div>
            <div class="metric-value">7h 31m</div>
            <div class="metric-status">🟢 Terapia Perfetta</div>
        </div>
    """, unsafe_allow_html=True)

with tab_medie:
    st.info("📊 Sezione Medie Storiche attiva.")
with tab_trend:
    st.info("📈 Grafici di andamento settimanale pronti.")
