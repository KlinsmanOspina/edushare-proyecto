import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de la Página
st.set_page_config(page_title="EduShare | Calidad y Control", page_icon="📚", layout="wide")

# 2. Inicialización del Estado (Añadimos 'likes')
if 'repositorio' not in st.session_state:
    st.session_state.repositorio = [
        {"titulo": "Guía de Metodología", "materia": "Metodología", "semestre": 1, "autor": "Sistema", "fecha": "2024-05-01", "likes": 5},
        {"titulo": "Apuntes de Cálculo", "materia": "Cálculo I", "semestre": 1, "autor": "Admin", "fecha": "2024-05-02", "likes": 3}
    ]

# 3. Lógica de Control de Acceso (Sprint 5)
# Aquí puedes definir los días exactos de parciales de tu universidad
dias_parciales = [15, 16, 17, 18, 19, 20] 
dia_actual = datetime.now().day
bloqueo_activo = dia_actual in dias_parciales

# --- INTERFAZ LATERAL ---
st.sidebar.title("🚀 EduShare")
menu = st.sidebar.radio("Navegación", ["Explorar Material", "Subir Apuntes", "Estadísticas"])

st.sidebar.divider()
filtro_semestre = st.sidebar.selectbox("Filtrar por Semestre", [1, 2, 3, 4, 5])

# --- VISTA 1: EXPLORAR MATERIAL ---
if menu == "Explorar Material":
    st.title("📂 Repositorio Académico")
    
    if bloqueo_activo:
        st.error("⚠️ **MODO INTEGRIDAD ACADÉMICA**: Las descargas están deshabilitadas temporalmente por periodo de exámenes.")
    
    busqueda = st.text_input("🔍 Buscar material...")
    
    # Mostrar resultados
    for i, item in enumerate(st.session_state.repositorio):
        # Filtro por semestre y búsqueda
        if item['semestre'] == filtro_semestre and (busqueda.lower() in item['titulo'].lower() or busqueda.lower() in item['materia'].lower()):
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 1, 1])
                with c1:
                    st.subheader(item['titulo'])
                    st.caption(f"Materia: {item['materia']} | Autor: {item['autor']}")
                with c2:
                    st.write(f"👍 {item['likes']} Likes")
                    if st.button("Dar Like", key=f"like_{i}"):
                        st.session_state.repositorio[i]['likes'] += 1
                        st.rerun()
                with c3:
                    if bloqueo_activo:
                        st.button("🔒 Bloqueado", disabled=True, key=f"btn_{i}")
                    else:
                        st.download_button("⬇️ Descargar", data="PDF Simulado", file_name=f"{item['titulo']}.pdf", key=f"btn_{i}")

# --- VISTA 2: SUBIR APUNTES ---
elif menu == "Subir Apuntes":
    st.title("📤 Subir Material")
    with st.form("subida", clear_on_submit=True):
        t = st.text_input("Título")
        m = st.text_input("Materia")
        s = st.slider("Semestre", 1, 10, filtro_semestre)
        f = st.file_uploader("Archivo")
        if st.form_submit_button("Publicar"):
            if t and m and f:
                st.session_state.repositorio.append({
                    "titulo": t, "materia": m, "semestre": s, 
                    "autor": "Estudiante", "fecha": "2024-05-20", "likes": 0
                })
                st.success("¡Publicado!")
                st.rerun()

# --- VISTA 3: ESTADÍSTICAS (Sprint 6 adelantado) ---
else:
    st.title("📊 Impacto de la Plataforma")
    df = pd.DataFrame(st.session_state.repositorio)
    if not df.empty:
        st.bar_chart(df.set_index('materia')['likes'])
        st.write("Esta gráfica muestra las materias con apuntes más valorados por la comunidad.")
