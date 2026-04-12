import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de Estilo Profesional
st.set_page_config(page_title="EduShare | Proyecto de Grado", page_icon="🎓", layout="wide")

# Estilos CSS para que no parezca una página básica
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    div.stButton > button { border-radius: 5px; height: 3em; width: 100%; }
    .reportview-container .main { color: #2c3e50; }
    </style>
    """, unsafe_allow_html=True)

# 2. Base de datos con "Seguro" de inicialización
if 'repositorio' not in st.session_state:
    st.session_state.repositorio = [
        {"titulo": "Guía de Metodología", "materia": "Metodología", "semestre": 1, "autor": "Sistema", "fecha": "2024-05-01", "likes": 5},
        {"titulo": "Apuntes de Cálculo", "materia": "Cálculo I", "semestre": 1, "autor": "Admin", "fecha": "2024-05-02", "likes": 3}
    ]

# 3. Control de Acceso por Calendario (Objetivo Específico 3)
dias_parciales = [15, 16, 17, 18, 19, 20] 
bloqueo_activo = datetime.now().day in dias_parciales

# --- NAVEGACIÓN ---
with st.sidebar:
    st.title("🎓 EduShare")
    st.write("Plataforma Colaborativa")
    menu = st.radio("Secciones", ["Explorar Repositorio", "Subir Material", "Panel de Impacto"])
    st.divider()
    sem_filtro = st.selectbox("Semestre Actual", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# --- VISTA: EXPLORAR ---
if menu == "Explorar Repositorio":
    st.header(f"📂 Material de {sem_filtro}° Semestre")
    
    if bloqueo_activo:
        st.warning("⚠️ **Sincronización con Calendario:** Acceso restringido por periodo evaluativo[cite: 100].")
    
    busqueda = st.text_input("🔍 Filtrar por nombre o asignatura...")
    
    # Procesar datos con seguridad
    df = pd.DataFrame(st.session_state.repositorio)
    if 'likes' not in df.columns: df['likes'] = 0
    
    # Lógica de visualización
    for i, item in enumerate(st.session_state.repositorio):
        if item['semestre'] == sem_filtro and (busqueda.lower() in item['titulo'].lower() or busqueda.lower() in item['materia'].lower()):
            with st.container(border=True):
                col_text, col_stats, col_action = st.columns([3, 1, 1])
                with col_text:
                    st.subheader(item['titulo'])
                    st.write(f"📖 **{item['materia']}** | 👤 {item['autor']}")
                with col_stats:
                    st.write(f"⭐ {item.get('likes', 0)} Validados")
                    # Pequeño truco para que no den likes tan rápido
                    if st.button("Validar", key=f"lk_{i}"):
                        st.session_state.repositorio[i]['likes'] += 1
                        st.rerun()
                with col_action:
                    if bloqueo_activo:
                        st.button("🔒 Bloqueado", disabled=True, key=f"lock_{i}")
                    else:
                        st.download_button("📥 Descargar", data="DATA", file_name=f"{item['titulo']}.pdf", key=f"dl_{i}")

# --- VISTA: SUBIR ---
elif menu == "Subir Material":
    st.header("📤 Carga de Material Académico")
    st.info("Asegúrate de que el material sea de autoría propia o libre de derechos[cite: 101].")
    
    with st.form("upload", clear_on_submit=True):
        t = st.text_input("Título del Apunte")
        m = st.text_input("Asignatura")
        s = st.number_input("Semestre correspondiente", 1, 10, sem_filtro)
        a = st.file_uploader("Documento (PDF/Imagen)", type=['pdf', 'jpg', 'png'])
        
        if st.form_submit_button("Publicar en la red"):
            if t and m and a:
                st.session_state.repositorio.append({
                    "titulo": t, "materia": m, "semestre": s, 
                    "autor": "Estudiante_Colab", "fecha": datetime.now().strftime("%d/%m/%Y"), "likes": 0
                })
                st.success("✅ Material cargado. Aparecerá en el repositorio mientras la sesión esté activa.")
            else:
                st.error("Campos incompletos.")

# --- VISTA: IMPACTO ---
else:
    st.header("📊 Estadísticas de la Comunidad")
    df_stats = pd.DataFrame(st.session_state.repositorio)
    if not df_stats.empty:
        st.subheader("Materias con mayor colaboración")
        stats = df_stats.groupby('materia')['likes'].sum().reset_index()
        st.bar_chart(data=stats, x='materia', y='likes', color="#c2410c")
        
        st.subheader("Ranking de Calidad [cite: 99]")
        st.dataframe(df_stats[['titulo', 'materia', 'likes']].sort_values('likes', ascending=False), use_container_width=True)
