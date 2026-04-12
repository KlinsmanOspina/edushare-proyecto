import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de Identidad Visual
st.set_page_config(page_title="EduShare | Plataforma Académica", page_icon="📚")

# Estilo personalizado (CSS simple)
st.markdown("""
    <style>
    .main { background-color: #fdfcfb; }
    .stButton>button { background-color: #c2410c; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Base de Datos de Materias (Requerimiento de Organización)
materias_por_semestre = {
    1: ["Cálculo I", "Álgebra Lineal", "Introducción a la Ingeniería"],
    2: ["Cálculo II", "Física I", "Programación I"],
    3: ["Cálculo III", "Física II", "Estructuras de Datos"]
}

# 3. Lógica del Calendario Académico (Requerimiento de Control)
# Simulamos que del 15 al 20 de cada mes es semana de parciales
dia_actual = datetime.now().day
es_semana_parciales = 15 <= dia_actual <= 20

# --- INTERFAZ DE USUARIO ---
st.title("📚 EduShare")
st.subheader("Plataforma Colaborativa de Apuntes")

# Sidebar para Navegación
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3413/3413535.png", width=100)
st.sidebar.title("Navegación")
semestre = st.sidebar.selectbox("Seleccione su Semestre", [1, 2, 3])

# Alerta de Control de Acceso (Tu propuesta innovadora)
if es_semana_parciales:
    st.warning("⚠️ **CONTROL DE INTEGRIDAD ACTIVO**: Debido a la semana de parciales, las descargas están limitadas.")
else:
    st.info("✅ **ACCESO LIBRE**: El repositorio está abierto para intercambio de material.")

# Cuerpo Principal: Materias y Apuntes
st.divider()
st.header(f"Materias de {semestre}° Semestre")

cols = st.columns(len(materias_por_semestre[semestre]))

for i, materia in enumerate(materias_por_semestre[semestre]):
    with cols[i]:
        st.markdown(f"### {materia}")
        if st.button(f"Ver apuntes", key=materia):
            st.write(f"Cargando archivos de {materia}...")
            if es_semana_parciales:
                st.error("Archivo bloqueado por parciales.")
            else:
                st.success("Archivo listo para descarga.")

# Pie de página técnico para Metodologías
st.sidebar.divider()
st.sidebar.caption(f"Versión: Prototipo Sprint 1 | Fecha: {datetime.now().strftime('%d/%m/%Y')}")

# Sprint 2: Estructura de Materias Real
materias_por_semestre = {
    1: ["Metodología de la Investigación", "Cálculo I", "Cátedra Universitaria"],
    2: ["Programación I", "Física I", "Cálculo II"],
    3: ["Estructuras de Datos", "Sistemas Operativos", "Estadística"],
    4: ["Bases de Datos", "Redes I", "Análisis Numérico"]
}

# Nueva sección de búsqueda (Requerimiento 2.1)
st.sidebar.divider()
busqueda = st.sidebar.text_input("🔍 Buscar material...")

if busqueda:
    st.write(f"Resultados para: **{busqueda}**")
    # Aquí luego conectaremos con la base de datos
