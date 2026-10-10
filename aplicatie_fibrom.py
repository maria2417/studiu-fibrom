import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# --- 1. CONFIGURARE BAZĂ DE DATE ---
DB_NAME = "studiu_chist_ovarian.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pacienti_chist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cod_pacient TEXT UNIQUE,
            varsta INTEGER, greutate REAL, inaltime REAL,
            etnie TEXT, mediu TEXT, 
            fumator TEXT, alcool TEXT, dieta TEXT,
            menopauza TEXT, varsta_menarha INTEGER, 
            anticonceptionale TEXT, numar_sarcini INTEGER, istoric_chist TEXT,
            hta TEXT, vitamina_d TEXT, 
            simptom TEXT, tip_chist TEXT, localizare TEXT, aspect_eco TEXT,
            ca125 REAL, lichid_douglas TEXT, complicatii TEXT,
            dimensiune REAL, tratament TEXT, zile_spitalizare INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_idx(val, lst):
    return lst.index(val) if val in lst else 0

# --- 2. SETĂRI INTERFAȚĂ ---
st.set_page_config(page_title="Studiu Clinic - Chist Ovarian", layout="wide")
st.title("🏆 Studiu Clinic Integrat - Analiza Chistului Ovarian")
st.markdown("Cercetare amplă: Date demografice, markeri tumorali (CA-125), aspect ecografic, complicații acute și tratament.")

tab1, tab2, tab3, tab4 = st.tabs(["➕ Adăugare Pacient", "📂 Baza de Date", "📊 Dashboard Statistic", "✏️ Editare Date"])

# --- TAB 1: FORMULAR INTRODUCERE DATE ---
with tab1:
    with st.form("form_pacient", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.markdown("👤 **Demografic & Metabolic**")
            cod = st.text_input("Cod Pacient (ex: P-001)")
            varsta = st.number_input("Vârstă (ani)", min_value=15, max_value=85, value=35)
            etnie = st.selectbox("Etnie", ["Caucaziană", "Romă", "Afro-americană", "Asiatică", "Alta"])
            mediu = st.selectbox("Mediu", ["Urban", "Rural"])
            greutate = st.number_input("Greutate (kg)", min_value=30.0, max_value=180.0, value=60.0)
            inaltime = st.number_input("Înălțime (m)", min_value=1.30, max_value=2.00, value=1.65, step=0.01)
            
        with c2:
            st.markdown("🍷 **Stil de Viață & Vicii**")
            fumator = st.selectbox("Fumat?", ["Nu", "Da, ocazional", "Da, zilnic"])
            alcool = st.selectbox("Consum Alcool?", ["Nu", "Ocazional", "Frecvent"])
            dieta = st.selectbox("Alimentație dominantă", ["Echilibrată", "Bogată în carne roșie", "Vegetariană/Vegană", "Bogată în zaharuri"])
            hta = st.selectbox("Hipertensiune (HTA)?", ["Nu", "Da, controlată", "Da, netratată"])
            vit_d = st.selectbox("Nivel Vitamina D", ["Normal (>30 ng/mL)", "Insuficiență (20-30 ng/mL)", "Deficit sever (<20 ng/mL)", "Nu a testat"])
            
        with c3:
            st.markdown("🧬 **Istoric Ginecologic**")
            varsta_menarha = st.number_input("Vârsta la menarhă", min_value=8, max_value=20, value=12)
            menopauza = st.selectbox("Status Hormonal", ["Pre-menopauză", "Peri-menopauză", "Post-menopauză"])
            anti = st.selectbox("Anticoncepționale?", ["Nu", "Da, sub 5 ani", "Da, peste 5 ani"])
            sarcini = st.number_input("Sarcini", min_value=0, max_value=15, value=0)
            istoric = st.selectbox("Istoric chisturi ovariene?", ["Nu", "Da, recidivă"])
            simptom = st.selectbox("Simptom Principal", ["Durere pelvină", "Tulburări menstruale", "Durere acută", "Asimptomatic"])
            
        with c4:
            st.markdown("🏥 **Clinic, Eco & Tratament**")
            tip_chist = st.selectbox("Tip Chist", ["Funcțional", "Endometriozic", "Dermoid", "Seros", "Mucinos", "Malign/Suspect"])
            localizare = st.selectbox("Localizare", ["Ovar Drept", "Ovar Stâng", "Bilateral"])
            aspect_eco = st.selectbox("Aspect Ecografic", ["Unilocular clar", "Multilocular", "Aspect "sticla mata"", "Componentă solidă/Papile"])
            ca125 = st.number_input("Marker CA-125 (U/mL)", min_value=0.0, max_value=5000.0, value=15.0, step=1.0)
            lichid_douglas = st.selectbox("Lichid în Douglas?", ["Nu", "Cantitate minimă", "Cantitate medie/mare"])
            complicatii = st.selectbox("Complicații acute", ["Fără", "Torsiune de anexă", "Ruptură chist", "Hemoragie intrakistica"])
            dimensiune = st.number_input("Dimensiune max (cm)", min_value=1.0, max_value=40.0, value=5.0)
            tratament = st.selectbox("Tratament", ["Expectativă/Monitorizare", "Medicamentos (ACO)", "Chistectomie laparoscopică", "Chistectomie clasică", "Anexectomie"])
            zile = st.number_input("Spitalizare (zile)", min_value=0, max_value=30, value=2)

        btn_salveaza = st.form_submit_button("💾 Salvează Fișa Pacientului")

        if btn_salveaza:
            if not cod:
                st.error("Codul pacientului este obligatoriu!")
            else:
                try:
                    conn = sqlite3.connect(DB_NAME)
                    c = conn.cursor()
                    c.execute('''
                        INSERT INTO pacienti_chist (cod_pacient, varsta, greutate, inaltime, etnie, mediu, fumator, alcool, dieta, menopauza, varsta_menarha, anticonceptionale, numar_sarcini, istoric_chist, hta, vitamina_d, simptom, tip_chist, localizare, aspect_eco, ca125, lichid_douglas, complicatii, dimensiune, tratament, zile_spitalizare)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (cod, varsta, greutate, inaltime, etnie, mediu, fumator, alcool, dieta, menopauza, varsta_menarha, anti, sarcini, istoric, hta, vit_d, simptom, tip_chist, localizare, aspect_eco, ca125, lichid_douglas, complicatii, dimensiune, tratament, zile))
                    conn.commit()
                    conn.close()
                    st.success(f"Pacientul {cod} a fost înregistrat cu succes!")
                except sqlite3.IntegrityError:
                    st.error("Acest cod există deja!")

# --- TAB 2: VIZUALIZARE BAZĂ DE DATE ---
with tab2:
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM pacienti_chist", conn)
    conn.close()

    if not df.empty:
        df['IMC'] = (df['greutate'] / (df['inaltime'] ** 2)).round(2)
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descarcă Tabelul Master (CSV)", data=csv, file_name="studiu_chist_ovarian.csv", mime="text/csv")
    else:
        st.info("Baza de date este goală.")

# --- TAB 3: DASHBOARD STATISTIC SUPREM ---
with tab3:
    if not df.empty:
        df['IMC'] = (df['greutate'] / (df['inaltime'] ** 2))
        
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("Volum Eșantion", len(df))
        m2.metric("Vârstă Medie", f"{df['varsta'].mean():.1f} ani")
        m3.metric("IMC Mediu", f"{df['IMC'].mean():.1f}")
        m4.metric("CA-125 Mediu", f"{df['ca125'].mean():.1f} U/mL")
        m5.metric("Dimensiune Medie", f"{df['dimensiune'].mean():.1f} cm")
        m6.metric("Zile Spitalizare (Medie)", f"{df['zile_spitalizare'].mean():.1f}")
        
        st.divider()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.plotly_chart(px.box(df, x="aspect_eco", y="dimensiune", color="aspect_eco", title="Aspect Ecografic vs. Dimensiunea Chistului"), use_container_width=True)
        with col2:
            st.plotly_chart(px.histogram(df, x="tip_chist", color="complicatii", barmode="stack", title="Tipul Chistului vs. Incidența Complicațiilor"), use_container_width=True)
        with col3:
            st.plotly_chart(px.box(df, x="localizare", y="dimensiune", color="localizare", title="Localizare vs. Dimensiune"), use_container_width=True)

        st.divider()

        col4, col5 = st.columns(2)
        with col4:
            st.plotly_chart(px.scatter(df, x="ca125", y="dimensiune", color="tip_chist", size="dimensiune", hover_data=["cod_pacient"], title="Markerul CA-125 vs Dimensiune pe Tipuri de Chist"), use_container_width=True)
        with col5:
            st.plotly_chart(px.histogram(df, x="tratament", color="tip_chist", barmode="group", title="Abordarea Terapeutică în funcție de Tipul Chistului"), use_container_width=True)

        st.divider()
        
        col6, col7 = st.columns(2)
        with col6:
            fig_ca = px.box(df, x="tip_chist", y="ca125", color="tip_chist", title="Distribuția CA-125 (Linie referință = 35 U/mL)")
            fig_ca.add_hline(y=35, line_dash="dot", line_color="red")
            st.plotly_chart(fig_ca, use_container_width=True)
        with col7:
            st.plotly_chart(px.box(df, x="tratament", y="zile_spitalizare", color="tratament", title="Timp de Recuperare post-intervenție"), use_container_width=True)

    else:
        st.warning("Te rog introdu pacienți pentru a popula graficele de cercetare.")

# --- TAB 4: MODIFICARE / ȘTERGERE ---
with tab4:
    conn = sqlite3.connect(DB_NAME)
    df_coduri = pd.read_sql_query("SELECT cod_pacient FROM pacienti_chist", conn)
    conn.close()

    if not df_coduri.empty:
        cod_ales = st.selectbox("🔍 Selectează pacientul pentru editare:", df_coduri['cod_pacient'])
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''SELECT varsta, greutate, inaltime, etnie, mediu, fumator, alcool, dieta, menopauza, varsta_menarha, anticonceptionale, numar_sarcini, istoric_chist, hta, vitamina_d, simptom, tip_chist, localizare, aspect_eco, ca125, lichid_douglas, complicatii, dimensiune, tratament, zile_spitalizare 
                     FROM pacienti_chist WHERE cod_pacient=?''', (cod_ales,))
        row = c.fetchone()
        conn.close()
        
        if row:
            with st.form("form_update_chist"):
                st.write(f"Modifici: **{cod_ales}**")
                c1, c2, c3, c4 = st.columns(4)
                
                with c1:
                    nou_varsta = st.number_input("Vârstă", min_value=15, max_value=85, value=row[0])
                    nou_greutate = st.number_input("Greutate (kg)", min_value=30.0, max_value=180.0, value=float(row[1]))
                    nou_inaltime = st.number_input("Înălțime (m)", min_value=1.30, max_value=2.00, value=float(row[2]), step=0.01)
                    nou_etnie = st.selectbox("Etnie", ["Caucaziană", "Romă", "Afro-americană", "Asiatică", "Alta"], index=get_idx(row[3], ["Caucaziană", "Romă", "Afro-americană", "Asiatică", "Alta"]))
                    nou_mediu = st.selectbox("Mediu", ["Urban", "Rural"], index=get_idx(row[4], ["Urban", "Rural"]))
                    nou_fumator = st.selectbox("Fumat?", ["Nu", "Da, ocazional", "Da, zilnic"], index=get_idx(row[5], ["Nu", "Da, ocazional", "Da, zilnic"]))
                    nou_alcool = st.selectbox("Alcool?", ["Nu", "Ocazional", "Frecvent"], index=get_idx(row[6], ["Nu", "Ocazional", "Frecvent"]))
                    
                with c2:
                    nou_dieta = st.selectbox("Alimentație", ["Echilibrată", "Bogată în carne roșie", "Vegetariană/Vegană", "Bogată în zaharuri"], index=get_idx(row[7], ["Echilibrată", "Bogată în carne roșie", "Vegetariană/Vegană", "Bogată în zaharuri"]))
                    nou_menopauza = st.selectbox("Status Hormonal", ["Pre-menopauză", "Peri-menopauză", "Post-menopauză"], index=get_idx(row[8], ["Pre-menopauză", "Peri-menopauză", "Post-menopauză"]))
                    nou_menarha = st.number_input("Vârsta Menarhă", min_value=8, max_value=20, value=row[9])
                    nou_anti = st.selectbox("Anticoncepționale?", ["Nu", "Da, sub 5 ani", "Da, peste 5 ani"], index=get_idx(row[10], ["Nu", "Da, sub 5 ani", "Da, peste 5 ani"]))
                    nou_sarcini = st.number_input("Sarcini", min_value=0, max_value=15, value=row[11])
                    nou_istoric = st.selectbox("Istoric chist?", ["Nu", "Da, recidivă"], index=get_idx(row[12], ["Nu", "Da, recidivă"]))
                    
                with c3:
                    nou_hta = st.selectbox("HTA?", ["Nu", "Da, controlată", "Da, netratată"], index=get_idx(row[13], ["Nu", "Da, controlată", "Da, netratată"]))
                    nou_vitd = st.selectbox("Vitamina D", ["Normal (>30 ng/mL)", "Insuficiență (20-30 ng/mL)", "Deficit sever (<20 ng/mL)", "Nu a testat"], index=get_idx(row[14], ["Normal (>30 ng/mL)", "Insuficiență (20-30 ng/mL)", "Deficit sever (<20 ng/mL)", "Nu a testat"]))
                    nou_simptom = st.selectbox("Simptom", ["Durere pelvină", "Tulburări menstruale", "Durere acută", "Asimptomatic"], index=get_idx(row[15], ["Durere pelvină", "Tulburări menstruale", "Durere acută", "Asimptomatic"]))
                    nou_tip = st.selectbox("Tip Chist", ["Funcțional", "Endometriozic", "Dermoid", "Seros", "Mucinos", "Malign/Suspect"], index=get_idx(row[16], ["Funcțional", "Endometriozic", "Dermoid", "Seros", "Mucinos", "Malign/Suspect"]))
                    nou_localizare = st.selectbox("Localizare", ["Ovar Drept", "Ovar Stâng", "Bilateral"], index=get_idx(row[17], ["Ovar Drept", "Ovar Stâng", "Bilateral"]))
                    nou_aspect = st.selectbox("Aspect Eco", ["Unilocular clar", "Multilocular", "Aspect "sticla mata"", "Componentă solidă/Papile"], index=get_idx(row[18], ["Unilocular clar", "Multilocular", "Aspect "sticla mata"", "Componentă solidă/Papile"]))
                    
                with c4:
                    nou_ca125 = st.number_input("CA-125 (U/mL)", min_value=0.0, max_value=5000.0, value=float(row[19]), step=1.0)
                    nou_lichid = st.selectbox("Lichid Douglas?", ["Nu", "Cantitate minimă", "Cantitate medie/mare"], index=get_idx(row[20], ["Nu", "Cantitate minimă", "Cantitate medie/mare"]))
                    nou_compl = st.selectbox("Complicații", ["Fără", "Torsiune de anexă", "Ruptură chist", "Hemoragie intrakistica"], index=get_idx(row[21], ["Fără", "Torsiune de anexă", "Ruptură chist", "Hemoragie intrakistica"]))
                    nou_dim = st.number_input("Dimensiune max (cm)", min_value=1.0, max_value=40.0, value=float(row[22]), step=0.5)
                    nou_trat = st.selectbox("Tratament", ["Expectativă/Monitorizare", "Medicamentos (ACO)", "Chistectomie laparoscopică", "Chistectomie clasică", "Anexectomie"], index=get_idx(row[23], ["Expectativă/Monitorizare", "Medicamentos (ACO)", "Chistectomie laparoscopică", "Chistectomie clasică", "Anexectomie"]))
                    nou_zile = st.number_input("Spitalizare (zile)", min_value=0, max_value=30, value=row[24])

                btn_update = st.form_submit_button("✅ Actualizează Modificările")
            
            btn_delete = st.button("❌ Șterge pacientul")

            if btn_update:
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute('''
                    UPDATE pacienti_chist 
                    SET varsta=?, greutate=?, inaltime=?, etnie=?, mediu=?, fumator=?, alcool=?, dieta=?, menopauza=?, varsta_menarha=?, anticonceptionale=?, numar_sarcini=?, istoric_chist=?, hta=?, vitamina_d=?, simptom=?, tip_chist=?, localizare=?, aspect_eco=?, ca125=?, lichid_douglas=?, complicatii=?, dimensiune=?, tratament=?, zile_spitalizare=?
                    WHERE cod_pacient=?
                ''', (nou_varsta, nou_greutate, nou_inaltime, nou_etnie, nou_mediu, nou_fumator, nou_alcool, nou_dieta, nou_menopauza, nou_menarha, nou_anti, nou_sarcini, nou_istoric, nou_hta, nou_vitd, nou_simptom, nou_tip, nou_localizare, nou_aspect, nou_ca125, nou_lichid, nou_compl, nou_dim, nou_trat, nou_zile, cod_ales))
                conn.commit()
                conn.close()
                st.success("Datele au fost actualizate cu succes!")
                st.rerun()
                
            if btn_delete:
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("DELETE FROM pacienti_chist WHERE cod_pacient=?", (cod_ales,))
                conn.commit()
                conn.close()
                st.error("Pacientul a fost șters din studiu.")
                st.rerun()
