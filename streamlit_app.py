        # === QUALITÀ DEL SONNO E RECUPERO ===
        st.markdown('<div class="section-header">🌙 Qualità del Sonno e Recupero</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-rosso">
                <div class="metric-title">Media Ore di Sonno (7gg)</div>
                <div class="metric-value">{prendi_dato(17, "5,86")} ore</div>
                <div class="metric-status">🔴 Carenza Sonno (Sotto 6 ore)</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-giallo">
                <div class="metric-title">Media Punteggio Sonno Storico</div>
                <div class="metric-value">{prendi_dato(18, "64")} / 100</div>
                <div class="metric-status">🟡 Valutazione Moderata</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Media Risvegli Notturni (7gg)</div>
                <div class="metric-value">{prendi_dato(19, "3,2")}</div>
                <div class="metric-status">🟢 Nella Norma</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-giallo">
                <div class="metric-title">Efficienza del Sonno Media (7gg)</div>
                <div class="metric-value">{prendi_dato(20, "63,53 %")}</div>
                <div class="metric-status">🟡 Monitorare Continuità</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Media Temperatura Corporea Storica</div>
                <div class="metric-value">{prendi_dato(21, "36,41")} °C</div>
                <div class="metric-status">🟢 Regolare</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Valutazione della Qualità Respiratoria</div>
                <div class="metric-value">{prendi_dato(22, "Ottimale")}</div>
                <div class="metric-status">🟢 Assenza di Disturbi</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-giallo">
                <div class="metric-title">Stato Regolarità Ritmo Circadiano</div>
                <div class="metric-value">{prendi_dato(23, "Cattivo")}</div>
                <div class="metric-status">🟡 Monitorare Orari Sonno</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Media Ore Sonno Profondo (7gg)</div>
                <div class="metric-value">{prendi_dato(24, "1,6")} ore</div>
                <div class="metric-status">🟢 Livello Ottimale</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Media Frequenza Respiratoria Notturna</div>
                <div class="metric-value">{prendi_dato(25, "16")} bpm</div>
                <div class="metric-status">🟢 Regolare ed Equilibrata</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Rapporto Recupero HRV (Fine vs Inizio)</div>
                <div class="metric-value">{prendi_dato(26, "2,8")}</div>
                <div class="metric-status">🟢 Cuore Recuperato</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Punteggio di Recupero Fisico (PAI)</div>
                <div class="metric-value">{prendi_dato(27, "72,7")}</div>
                <div class="metric-status">🟢 Buono Stato Fisico</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-giallo">
                <div class="metric-title">Punteggio di Recupero Mentale</div>
                <div class="metric-value">{prendi_dato(28, "54")} / 100</div>
                <div class="metric-status">🟡 Sotto la Media Settimanale</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Monitoraggio Rischio Apnea Notturna</div>
                <div class="metric-value">{prendi_dato(29, "Basso")}</div>
                <div class="metric-status">🟢 Livello Sicuro</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-rosso">
                <div class="metric-title">Picco Frequenza Cardiaca Massima (7gg)</div>
                <div class="metric-value">{prendi_dato(30, "137")} bpm</div>
                <div class="metric-status">🔴 Picco Sotto Sforzo Elevato</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="metric-card bg-verde">
                <div class="metric-title">Media Ore Utilizzo CPAP (7gg)</div>
                <div class="metric-value">{prendi_dato(31, "6,5")}</div>
                <div class="metric-status">🟢 Terapia Regolare</div>
            </div>
        """, unsafe_allow_html=True)

    # Chiusura delle schede posizionata con il perfetto rientro a 4 spazi!
    with tab_medie:
        st.info("📊 Sezione Medie Storiche attiva nella colonna Z e AA.")
    with tab_trend:
        st.info("📈 Grafici di andamento settimanale pronti.")
    # === QUALITÀ DEL SONNO E RECUPERO ===
    st.markdown('<div class="section-header">🌙 Qualità del Sonno e Recupero</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-rosso">
            <div class="metric-title">Media Ore di Sonno (7gg)</div>
            <div class="metric-value">{prendi_dato(17, "5,86")} ore</div>
            <div class="metric-status">🔴 Carenza Sonno (Sotto 6 ore)</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-giallo">
            <div class="metric-title">Media Punteggio Sonno Storico</div>
            <div class="metric-value">{prendi_dato(18, "64")} / 100</div>
            <div class="metric-status">🟡 Valutazione Moderata</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Risvegli Notturni (7gg)</div>
            <div class="metric-value">{prendi_dato(19, "3,2")}</div>
            <div class="metric-status">🟢 Nella Norma</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-giallo">
            <div class="metric-title">Efficienza del Sonno Media (7gg)</div>
            <div class="metric-value">{prendi_dato(20, "63,53 %")}</div>
            <div class="metric-status">🟡 Monitorare Continuità</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Temperatura Corporea Storica</div>
            <div class="metric-value">{prendi_dato(21, "36,41")} °C</div>
            <div class="metric-status">🟢 Regolare</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Valutazione della Qualità Respiratoria</div>
            <div class="metric-value">{prendi_dato(22, "Ottimale")}</div>
            <div class="metric-status">🟢 Assenza di Disturbi</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-giallo">
            <div class="metric-title">Stato Regolarità Ritmo Circadiano</div>
            <div class="metric-value">{prendi_dato(23, "Cattivo")}</div>
            <div class="metric-status">🟡 Monitorare Orari Sonno</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Ore Sonno Profondo (7gg)</div>
            <div class="metric-value">{prendi_dato(24, "1,6")} ore</div>
            <div class="metric-status">🟢 Livello Ottimale</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Frequenza Respiratoria Notturna</div>
            <div class="metric-value">{prendi_dato(25, "16")} bpm</div>
            <div class="metric-status">🟢 Regolare ed Equilibrata</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Rapporto Recupero HRV (Fine vs Inizio)</div>
            <div class="metric-value">{prendi_dato(26, "2,8")}</div>
            <div class="metric-status">🟢 Cuore Recuperato</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Punteggio di Recupero Fisico (PAI)</div>
            <div class="metric-value">{prendi_dato(27, "72,7")}</div>
            <div class="metric-status">🟢 Buono Stato Fisico</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-giallo">
            <div class="metric-title">Punteggio di Recupero Mentale</div>
            <div class="metric-value">{prendi_dato(28, "54")} / 100</div>
            <div class="metric-status">🟡 Sotto la Media Settimanale</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Monitoraggio Rischio Apnea Notturna</div>
            <div class="metric-value">{prendi_dato(29, "Basso")}</div>
            <div class="metric-status">🟢 Livello Sicuro</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-rosso">
            <div class="metric-title">Picco Frequenza Cardiaca Massima (7gg)</div>
            <div class="metric-value">{prendi_dato(30, "137")} bpm</div>
            <div class="metric-status">🔴 Picco Sotto Sforzo Elevato</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card bg-verde">
            <div class="metric-title">Media Ore Utilizzo CPAP (7gg)</div>
            <div class="metric-value">{prendi_dato(31, "6,5")}</div>
            <div class="metric-status">🟢 Terapia Regolare</div>
        </div>
    """, unsafe_allow_html=True)

with tab_medie:
    st.info("📊 Sezione Medie Storiche attiva nella colonna Z e AA.")
with tab_trend:
    st.info("📈 Grafici di andamento settimanale pronti.")
