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
st.write("Pannello di Monitoraggio Personale")

tab_oggi, tab_medie, tab_trend = st.tabs(["Oggi (Pannello)", "Medie Storiche", "Trend"])

with tab_oggi:
    # === STILE DI VITA E ATTIVITÀ ===
    st.markdown('<div class="section-header">🏃 Stile di Vita e Attività</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Passi Settimanali</div>
            <div class="metric-value">8.383</div>
            <div class="metric-status">🟢 Obiettivo Minimo Raggiunto</div>
        </div>
    """, unsafe_allow_html=True)
    
    # === SALUTE DEL CUORE ===
    st.markdown('<div class="section-header">❤️ Salute del Cuore</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">ℹ️ INDICE WITHINGS COMPOSITO</div>
            <div class="metric-value">Cardio Ottimale</div>
            <div class="metric-status">🟢 Stato di Salute Eccellente</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Frequenza Cardiaca Diurna</div>
            <div class="metric-value">67 bpm</div>
            <div class="metric-status">🟢 Regolare</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Frequenza Battiti a Riposo</div>
            <div class="metric-value">52 bpm</div>
            <div class="metric-status">🟢 Eccellente Recupero</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Variabilità Cardiaca (HRV)</div>
            <div class="metric-value">18 ms</div>
            <div class="metric-status">🟢 Bilanciato</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Ossigeno nel Sangue (SpO2)</div>
            <div class="metric-value">96,2 %</div>
            <div class="metric-status">🟢 Ottimale</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-giallo">
            <div class="metric-title">Media Pressione Sistolica (Massima)</div>
            <div class="metric-value">101 mmHg</div>
            <div class="metric-status">🟡 Monitorare Massima</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Pressione Diastolica (Minima)</div>
            <div class="metric-value">70 mmHg</div>
            <div class="metric-status">🟢 Ottimale</div>
        </div>
    """, unsafe_allow_html=True)

    # === QUALITÀ DEL SONNO E RECUPERO ===
    st.markdown('<div class="section-header">🌙 Qualità del Sonno e Recupero</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-rosso">
            <div class="metric-title">Media Ore di Sonno (7gg)</div>
            <div class="metric-value">5,86 ore</div>
            <div class="metric-status">🔴 Carenza Sonno (Sotto 6 ore)</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-giallo">
            <div class="metric-title">Media Punteggio Sonno Storico</div>
            <div class="metric-value">64 / 100</div>
            <div class="metric-status">🟡 Moderato</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Ore Sonno Profondo</div>
            <div class="metric-value">1,6 ore</div>
            <div class="metric-status">🟢 Livello Ottimale</div>
        </div>
    """, unsafe_allow_html=True)

with tab_medie:
    st.info("📊 Sezione Medie Storiche attiva e al sicuro.")
with tab_trend:
    st.info("📈 Grafici di andamento settimanale pronti.")
