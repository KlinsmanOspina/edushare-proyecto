import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de la Página
st.set_page_config(page_title="EduShare | Proyecto de Grado", layout="wide")

# 2. Inicialización Blindada de Datos
if 'repositorio' not in st.session_state or not st.session_state.repositorio:
    st.session_state.repositorio = [
        {"titulo": "Guía de Metodología", "materia": "Investigación", "semestre": 1, "autor": "Sistema", "likes": 5},
        {"titulo": "Apuntes de Cálculo", "materia": "Cálculo I", "semestre": 1, "autor": "Admin", "likes": 3}
    ]

# 3. Lógica de Calendario
dia_hoy = datetime.now().day
bloqueo_activo = 15 <= dia_hoy <= 20

# --- INTERFAZ ---
st.title("🎓 EduShare: Plataforma Académica")

# Sidebar
with st.sidebar:
    st.header("Menú")
    opcion = st.radio("Ir a:", ["Explorar", "Subir", "Ranking"])
    st.divider()
    sem_busqueda = st.selectbox("Semestre", list(range(1, 11)))
    
    # BOTÓN DE EMERGENCIA: Por si algo se pone en blanco
    if st.button("🔄 Forzar Recarga de Datos"):
        st.session_state.repositorio = [
            {"titulo": "Guía de Metodología", "materia": "Investigación", "semestre": 1, "autor": "Sistema", "likes": 5},
            {"titulo": "Apuntes de Cálculo", "materia": "Cálculo I", "semestre": 1, "autor": "Admin", "likes": 3}
        ]
        st.rerun()

# --- VISTA: EXPLORAR ---
if opcion == "Explorar":
    st.subheader(f"📂 Archivos del Semestre {sem_busqueda}")
    
    if bloqueo_activo:
        st.warning("⚠️ Acceso restringido por semana de exámenes.")

    # Filtramos los datos
    for i, item in enumerate(st.session_state.repositorio):
        if item['semestre'] == sem_busqueda:
            with st.expander(f"📄 {item['titulo']} ({item['materia']})", expanded=True):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.write(f"Autor: {item['autor']} | 👍 {item['likes']} Likes")
                with c2:
                    if st.button("Dar Like", key=f"lk_{i}"):
                        st.session_state.repositorio[i]['likes'] += 1
                        st.rerun()
                    
                    if not bloqueo_activo:
                        st.download_button("⬇️ Descargar", data="Contenido", file_name="archivo.pdf", key=f"dl_{i}")

# --- VISTA: SUBIR ---
elif opcion == "Subir":
    st.subheader("📤 Subir Material")
    with st.form("subida"):
        t = st.text_input("Título")
        m = st.text_input("Materia")
        s = st.number_input("Semestre", 1, 10, sem_busqueda)
        f = st.file_uploader("Archivo")
        if st.form_submit_button("Publicar"):
            if t and m and f:
                st.session_state.repositorio.append({"titulo": t, "materia": m, "semestre": s, "autor": "Estudiante", "likes": 0})
                st.success("¡Subido! Ve a la pestaña Explorar.")
            else:
                st.error("Faltan datos.")

# --- VISTA: RANKING ---
else:
    st.subheader("📊 Ranking de Materias")
    df = pd.DataFrame(st.session_state.repositorio)
    if not df.empty:
        # Gráfica simple
        stats = df.groupby('materia')['likes'].sum().reset_index()
        st.bar_chart(data=stats, x='materia', y='likes')
        st.table(df)
