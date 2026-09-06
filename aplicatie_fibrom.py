import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# --- 1. CONFIGURARE BAZĂ DE DATE ---
DB_NAME = "studiu_fibrom_suprem.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pacienti_suprem (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cod_pacient TEXT UNIQUE,
            varsta INTEGER, greutate REAL, inaltime REAL,
            etnie TEXT, mediu TEXT, 
            fumator TEXT, alcool TEXT, dieta TEXT,
            menopauza TEXT, varsta_menarha INTEGER, 
            anticonceptionale TEXT, numar_sarcini INTEGER, istoric_familiar TEXT,
            hta TEXT, vitamina_d TEXT, hemoglobina REAL, 
            simptom TEXT, tip_fibrom TEXT, dimensiune REAL, 
            tratament TEXT, zile_spitalizare INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_idx(val, lst):
    return lst.index(val) if val in lst else 0

# --- 2. SETĂRI INTERFAȚĂ ---
st.set_page_config(page_title="Studiu Clinic Integrat - Fibrom Uterin", layout="wide")
st.title("🏆 Studiu Clinic Integrat - Analiza Fibromului Uterin")
st.markdown("Cercetare amplă: Date demografice, factori metabolici, de mediu, asocieri cardiovasculare (HTA) și hormonale.")

tab1, tab2, tab3, tab4 = st.tabs(["➕ Adăugare Pacient", "📂 Baza de Date", "📊 Dashboard Statistic Suprem", "✏️ Editare Date"])

# --- TAB 1: FORMULAR INTRODUCERE DATE ---
with tab1:
    with st.form("form_pacient", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.markdown("👤 **Demografic & Metabolic**")
            cod = st.text_input("Cod Pacient (ex: P-001)")
            varsta = st.number_input("Vârstă (ani)", min_value=15, max_value=85, value=40)
            etnie = st.selectbox("Etnie", ["Caucaziană", "Romă", "Afro-americană", "Asiatică", "Alta"])
            mediu = st.selectbox("Mediu", ["Urban", "Rural"])
            greutate = st.number_input("Greutate (kg)", min_value=30.0, max_value=180.0, value=65.0)
            inaltime = st.number_input("Înălțime (m)", min_value=1.30, max_value=2.00, value=1.65, step=0.01)
            
        with c2:
            st.markdown("🍷 **Stil de Viață & Vicii**")
            fumator = st.selectbox("Fumat?", ["Nu", "Da, ocazional", "Da, zilnic"])
            alcool = st.selectbox("Consum Alcool?", ["Nu", "Ocazional", "Frecvent (bere)", "Frecvent (altele)"])
            dieta = st.selectbox("Alimentație dominantă", ["Echilibrată", "Bogată în carne roșie", "Vegetariană/Vegană", "Bogată în zaharuri"])
            hta = st.selectbox("Hipertensiune (HTA)?", ["Nu", "Da, controlată cu tratament", "Da, netratată"])
            vit_d = st.selectbox("Nivel Vitamina D", ["Normal (>30 ng/mL)", "Insuficiență (20-30 ng/mL)", "Deficit sever (<20 ng/mL)", "Nu a testat"])
            
        with c3:
            st.markdown("🧬 **Istoric Ginecologic**")
            varsta_menarha = st.number_input("Vârsta la menarhă", min_value=8, max_value=20, value=12)
            menopauza = st.selectbox("Status Hormonal", ["Pre-menopauză", "Peri-menopauză", "Post-menopauză"])
            anti = st.selectbox("Anticoncepționale?", ["Nu", "Da, sub 5 ani", "Da, peste 5 ani"])
            sarcini = st.number_input("Sarcini", min_value=0, max_value=15, value=0)
            istoric = st.selectbox("Ereditate fibrom?", ["Nu", "Da"])
            
        with c4:
            st.markdown("🏥 **Clinic & Tratament**")
            simptom = st.selectbox("Simptom Principal", ["Menoragie", "Durere pelvină", "Compresie", "Asimptomatic"])
            hb = st.number_input("Hemoglobina (g/dL)", min_value=4.0, max_value=16.0, value=12.5, step=0.1)
            tip_fibrom = st.selectbox("Tip Fibrom", ["Intramural", "Subseros", "Submucos", "Pediculat", "Mixt"])
            dimensiune = st.number_input("Dimensiune max (cm)", min_value=0.5, max_value=30.0, value=5.0)
            tratament = st.selectbox("Tratament", ["Medicamentos", "Miomectomie", "Histerectomie totală", "Histerectomie subtotală", "Embolizare", "Expectativă"])
            zile = st.number_input("Spitalizare (zile)", min_value=0, max_value=30, value=3)

        btn_salveaza = st.form_submit_button("💾 Salvează Fișa Pacientului")

        if btn_salveaza:
            if not cod:
                st.error("Codul pacientului este obligatoriu!")
            else:
                try:
                    conn = sqlite3.connect(DB_NAME)
                    c = conn.cursor()
                    c.execute('''
                        INSERT INTO pacienti_suprem (cod_pacient, varsta, greutate, inaltime, etnie, mediu, fumator, alcool, dieta, menopauza, varsta_menarha, anticonceptionale, numar_sarcini, istoric_familiar, hta, vitamina_d, hemoglobina, simptom, tip_fibrom, dimensiune, tratament, zile_spitalizare)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (cod, varsta, greutate, inaltime, etnie, mediu, fumator, alcool, dieta, menopauza, varsta_menarha, anti, sarcini, istoric, hta, vit_d, hb, simptom, tip_fibrom, dimensiune, tratament, zile))
                    conn.commit()
                    conn.close()
                    st.success(f"Pacientul {cod} a fost înregistrat cu succes!")
                except sqlite3.IntegrityError:
                    st.error("Acest cod există deja!")

# --- TAB 2: VIZUALIZARE BAZĂ DE DATE ---
with tab2:
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM pacienti_suprem", conn)
    conn.close()

    if not df.empty:
        df['IMC'] = (df['greutate'] / (df['inaltime'] ** 2)).round(2)
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descarcă Tabelul Master (CSV)", data=csv, file_name="studiu_fibrom_suprem.csv", mime="text/csv")
    else:
        st.info("Baza de date este goală.")

# --- TAB 3: DASHBOARD STATISTIC SUPREM ---
with tab3:
    if not df.empty:
        df['IMC'] = (df['greutate'] / (df['inaltime'] ** 2))
        
        # Metrici Top
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("Volum Eșantion", len(df))
        m2.metric("Vârstă Medie", f"{df['varsta'].mean():.1f} ani")
        m3.metric("Menarhă (Medie)", f"{df['varsta_menarha'].mean():.1f} ani")
        m4.metric("IMC Mediu", f"{df['IMC'].mean():.1f}")
        m5.metric("Hb Medie", f"{df['hemoglobina'].mean():.1f}")
        m6.metric("Dimensiune Medie", f"{df['dimensiune'].mean():.1f} cm")
        
        st.divider()

        # Rând 1: Factorii Noi (Vitamina D, Dietă, HTA)
        col1, col2, col3 = st.columns(3)
        with col1:
            fig_vitd = px.box(df, x="vitamina_d", y="dimensiune", color="vitamina_d", title="Deficitul Vit. D vs. Dimensiune Fibrom")
            st.plotly_chart(fig_vitd, use_container_width=True)
        with col2:
            fig_hta = px.box(df, x="hta", y="dimensiune", color="hta", title="Impactul Hipertensiunii (HTA) asupra mărimii")
            st.plotly_chart(fig_hta, use_container_width=True)
        with col3:
            fig_dieta = px.histogram(df, x="dieta", color="simptom", barmode="stack", title="Tiparul Alimentar vs. Simptomatologie")
            st.plotly_chart(fig_dieta, use_container_width=True)

        st.divider()

        # Rând 2: Profil Hormonal extins (Menarhă + Menopauză)
        col4, col5 = st.columns(2)
        with col4:
            fig_menarha = px.scatter(df, x="varsta_menarha", y="dimensiune", color="istoric_familiar", size="dimensiune",
                                     title="Expunere Estrogenică: Menarha Precoce vs Dimensiune",
                                     labels={"varsta_menarha": "Vârsta la prima menstruație (ani)"})
            st.plotly_chart(fig_menarha, use_container_width=True)
            
        with col5:
            fig_alcool = px.box(df, x="alcool", y="dimensiune", color="alcool",
                               title="Impactul Consumului de Alcool asupra dezvoltării tumorale")
            st.plotly_chart(fig_alcool, use_container_width=True)

        st.divider()
        
        # Rând 3: Parametri Medicali Standard (Anemie & Tratament)
        col6, col7 = st.columns(2)
        with col6:
            fig_hb = px.box(df, x="simptom", y="hemoglobina", color="simptom", title="Sindromul Anemic (Linie limită Hb=12)")
            fig_hb.add_hline(y=12, line_dash="dot", line_color="red")
            st.plotly_chart(fig_hb, use_container_width=True)
        with col7:
            fig_recup = px.box(df, x="tratament", y="zile_spitalizare", color="tratament", title="Timp de Recuperare post-intervenție")
            st.plotly_chart(fig_recup, use_container_width=True)

    else:
        st.warning("Te rog introdu pacienți pentru a popula graficele de cercetare.")

# --- TAB 4: MODIFICARE / ȘTERGERE ---
with tab4:
    conn = sqlite3.connect(DB_NAME)
    df_coduri = pd.read_sql_query("SELECT cod_pacient FROM pacienti_suprem", conn)
    conn.close()

    if not df_coduri.empty:
        cod_ales = st.selectbox("🔍 Selectează pacientul pentru editare:", df_coduri['cod_pacient'])
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''SELECT varsta, greutate, inaltime, etnie, mediu, fumator, alcool, dieta, menopauza, varsta_menarha, anticonceptionale, numar_sarcini, istoric_familiar, hta, vitamina_d, hemoglobina, simptom, tip_fibrom, dimensiune, tratament, zile_spitalizare 
                     FROM pacienti_suprem WHERE cod_pacient=?''', (cod_ales,))
        row = c.fetchone()
        conn.close()
        
        if row:
            with st.form("form_update_suprem"):
                st.write(f"Modifici: **{cod_ales}**")
                c1, c2, c3, c4 = st.columns(4)
                
                with c1:
                    nou_varsta = st.number_input("Vârstă", min_value=15, max_value=85, value=row[0])
                    nou_etnie = st.selectbox("Etnie", ["Caucaziană", "Romă", "Afro-americană", "Asiatică", "Alta"], index=get_idx(row[3], ["Caucaziană", "Romă", "Afro-americană", "Asiatică", "Alta"]))
                    nou_mediu = st.selectbox("Mediu", ["Urban", "Rural"], index=get_idx(row[4], ["Urban", "Rural"]))
                    nou_greutate = st.number_input("Greutate (kg)", min_value=30.0, max_value=180.0, value=float(row[1]))
                    nou_inaltime = st.number_input("Înălțime (m)", min_value=1.30, max_value=2.00, value=float(row[2]), step=0.01)
                    
                with c2:
                    nou_fumator = st.selectbox("Fumat?", ["Nu", "Da, ocazional", "Da, zilnic"], index=get_idx(row[5], ["Nu", "Da, ocazional", "Da, zilnic"]))
                    nou_alcool = st.selectbox("Alcool?", ["Nu", "Ocazional", "Frecvent (bere)", "Frecvent (altele)"], index=get_idx(row[6], ["Nu", "Ocazional", "Frecvent (bere)", "Frecvent (altele)"]))
                    nou_dieta = st.selectbox("Alimentație", ["Echilibrată", "Bogată în carne roșie", "Vegetariană/Vegană", "Bogată în zaharuri"], index=get_idx(row[7], ["Echilibrată", "Bogată în carne roșie", "Vegetariană/Vegană", "Bogată în zaharuri"]))
                    nou_hta = st.selectbox("HTA?", ["Nu", "Da, controlată cu tratament", "Da, netratată"], index=get_idx(row[13], ["Nu", "Da, controlată cu tratament", "Da, netratată"]))
                    nou_vitd = st.selectbox("Vitamina D", ["Normal (>30 ng/mL)", "Insuficiență (20-30 ng/mL)", "Deficit sever (<20 ng/mL)", "Nu a testat"], index=get_idx(row[14], ["Normal (>30 ng/mL)", "Insuficiență (20-30 ng/mL)", "Deficit sever (<20 ng/mL)", "Nu a testat"]))
                    
                with c3:
                    nou_menarha = st.number_input("Vârsta Menarhă", min_value=8, max_value=20, value=row[9])
                    nou_menopauza = st.selectbox("Status Hormonal", ["Pre-menopauză", "Peri-menopauză", "Post-menopauză"], index=get_idx(row[8], ["Pre-menopauză", "Peri-menopauză", "Post-menopauză"]))
                    nou_anti = st.selectbox("Anticoncepționale?", ["Nu", "Da, sub 5 ani", "Da, peste 5 ani"], index=get_idx(row[10], ["Nu", "Da, sub 5 ani", "Da, peste 5 ani"]))
                    nou_sarcini = st.number_input("Sarcini", min_value=0, max_value=15, value=row[11])
                    nou_istoric = st.selectbox("Ereditate?", ["Nu", "Da"], index=get_idx(row[12], ["Nu", "Da"]))
                    
                with c4:
                    nou_simptom = st.selectbox("Simptom", ["Menoragie", "Durere pelvină", "Compresie", "Asimptomatic"], index=get_idx(row[15], ["Menoragie", "Durere pel pelvină", "Compresie", "Asimptomatic"]))
                    nou_hb = st.number_input("Hemoglobina (g/dL)", min_value=4.0, max_value=16.0, value=float(row[16]), step=0.1)
                    nou_tip = st.selectbox("Tip Fibrom", ["Intramural", "Subseros", "Submucos", "Pediculat", "Mixt"], index=get_idx(row[17], ["Intramural", "Subseros", "Submucos", "Pediculat", "Mixt"]))
                    nou_dim = st.number_input("Dimensiune max (cm)", min_value=0.5, max_value=30.0, value=float(row[18]), step=0.5)
                    nou_trat = st.selectbox("Tratament", ["Medicamentos", "Miomectomie", "Histerectomie totală", "Histerectomie subtotală", "Embolizare", "Expectativă"], index=get_idx(row[19], ["Medicamentos", "Miomectomie", "Histerectomie totală", "Histerectomie subtotală", "Embolizare", "Expectativă"]))
                    nou_zile = st.number_input("Spitalizare (zile)", min_value=0, max_value=30, value=row[20])

                btn_update = st.form_submit_button("✅ Actualizează Modificările")
            
            btn_delete = st.button("❌ Șterge pacientul")

            if btn_update:
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute('''
                    UPDATE pacienti_suprem 
                    SET varsta=?, greutate=?, inaltime=?, etnie=?, mediu=?, fumator=?, alcool=?, dieta=?, menopauza=?, varsta_menarha=?, anticonceptionale=?, numar_sarcini=?, istoric_familiar=?, hta=?, vitamina_d=?, hemoglobina=?, simptom=?, tip_fibrom=?, dimensiune=?, tratament=?, zile_spitalizare=?
                    WHERE cod_pacient=?
                ''', (nou_varsta, nou_greutate, nou_inaltime, nou_etnie, nou_mediu, nou_fumator, nou_alcool, nou_dieta, nou_menopauza, nou_menarha, nou_anti, nou_sarcini, nou_istoric, nou_hta, nou_vitd, nou_hb, nou_simptom, nou_tip, nou_dim, nou_trat, nou_zile, cod_ales))
                conn.commit()
                conn.close()
                st.success("Datele au fost actualizate cu succes!")
                st.rerun()
                
            if btn_delete:
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("DELETE FROM pacienti_suprem WHERE cod_pacient=?", (cod_ales,))
                conn.commit()
                conn.close()
                st.error("Pacientul a fost șters din studiu.")
                st.rerun()