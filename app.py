import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de la Página
st.set_page_config(page_title="EduShare | Repositorio Académico", page_icon="📚", layout="wide")

# 2. Inicialización del Estado (Base de datos temporal)
if 'repositorio' not in st.session_state:
    # Datos iniciales de ejemplo basados en tu propuesta [cite: 103, 111]
    st.session_state.repositorio = [
        {"titulo": "Guía de Metodología", "materia": "Metodología", "semestre": 1, "autor": "Sistema", "fecha": "2024-05-01"},
        {"titulo": "Apuntes de Cálculo", "materia": "Cálculo I", "semestre": 1, "autor": "Admin", "fecha": "2024-05-02"}
    ]

# 3. Lógica de Control (Calendario Académico) [cite: 100, 120]
dia_actual = datetime.now().day
# Simulamos semana de parciales si el día está entre 15 y 20
es_semana_parciales = 15 <= dia_actual <= 20 

# --- INTERFAZ LATERAL (SIDEBAR) ---
st.sidebar.title("🚀 EduShare")
menu = st.sidebar.radio("Menú", ["Explorar Material", "Subir Apuntes"])

st.sidebar.divider()
filtro_semestre = st.sidebar.selectbox("Filtrar por Semestre", [1, 2, 3, 4, 5])

# --- VISTA 1: EXPLORAR MATERIAL ---
if menu == "Explorar Material":
    st.title("📂 Repositorio de Apuntes")
    st.write("Accede al material compartido por tus compañeros[cite: 117].")
    
    if es_semana_parciales:
        st.warning("⚠️ **Control de Acceso**: Las descargas están restringidas por periodo de exámenes[cite: 100, 110].")

    # Buscador dinámico
    busqueda = st.text_input("🔍 Buscar por título o materia...")
    
    # Convertir a DataFrame para filtrar
    df = pd.DataFrame(st.session_state.repositorio)
    
    # Aplicar filtros
    resultado = df[df['semestre'] == filtro_semestre]
    if busqueda:
        resultado = resultado[resultado['titulo'].str.contains(busqueda, case=False) | 
                              resultado['materia'].str.contains(busqueda, case=False)]

    if not resultado.empty:
        for i, row in resultado.iterrows():
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### {row['titulo']}")
                    st.caption(f"Materia: {row['materia']} | Autor: {row['autor']}")
                with col2:
                    if es_semana_parciales:
                        st.button("🔒 Bloqueado", key=f"lock_{i}", disabled=True)
                    else:
                        st.download_button("⬇️ Descargar", data="Contenido", file_name=f"{row['titulo']}.pdf", key=f"dl_{i}")
    else:
        st.info("No hay material disponible para los criterios seleccionados.")

# --- VISTA 2: SUBIR APUNTES ---
else:
    st.title("📤 Compartir Material")
    st.write("Ayuda a fortalecer el acceso equitativo al estudio[cite: 96, 119].")
    
    with st.form("form_subida", clear_on_submit=True):
        titulo = st.text_input("Título del documento")
        materia = st.text_input("Nombre de la materia")
        semestre_doc = st.number_input("Semestre", min_value=1, max_value=10, value=filtro_semestre)
        archivo = st.file_uploader("Selecciona el archivo", type=['pdf', 'docx', 'jpg', 'png'])
        
        boton_subir = st.form_submit_button("Publicar en la Plataforma")
        
        if boton_subir:
            if titulo and materia and archivo:
                nuevo_apunte = {
                    "titulo": titulo,
                    "materia": materia,
                    "semestre": semestre_doc,
                    "autor": "Estudiante",
                    "fecha": datetime.now().strftime("%Y-%m-%d")
                }
                st.session_state.repositorio.append(nuevo_apunte)
                st.success("✅ ¡Material compartido con éxito!")
            else:
                st.error("Por favor completa todos los campos y sube un archivo.")
