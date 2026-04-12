import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración y Estilo
st.set_page_config(page_title="EduShare | Repositorio Académico", page_icon="📚", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #fdfcfb; }
    .stButton>button { width: 100%; border-radius: 8px; border: 1px solid #c2410c; }
    .css-1r6slb0 { background-color: white; padding: 2rem; border-radius: 15px; shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicialización de la "Base de Datos" en memoria (Sprint 3)
if 'repositorio' not in st.session_state:
    st.session_state.repositorio = [
        {"titulo": "Taller DHCP Ubuntu", "materia": "Redes I", "semestre": 4, "autor": "Ospina", "fecha": "2024-05-20"},
        {"titulo": "Resumen Derivadas", "materia": "Cálculo I", "semestre": 1, "autor": "Antivar", "fecha": "2024-05-18"}
    ]

# 3. Lógica de Control (Calendario)
dia_actual = datetime.now().day
es_semana_parciales = 15 <= dia_actual <= 20 # Bloqueo simulado

# --- BARRA LATERAL ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3413/3413535.png", width=80)
st.sidebar.title("EduShare Panel")

menu = st.sidebar.radio("Ir a:", ["Explorar Apuntes", "Subir Material", "Mi Perfil (Próximamente)"])

st.sidebar.divider()
filtro_semestre = st.sidebar.selectbox("Filtrar por Semestre", [1, 2, 3, 4, 5])

# --- VISTA: EXPLORAR ---
if menu == "Explorar Apuntes":
    st.title("📂 Repositorio de Material")
    
    if es_semana_parciales:
        st.warning("⚠️ **Restricción de Parciales Activa**: La descarga está deshabilitada para proteger la integridad académica.") [cite: 100, 110]
    
    # Buscador dinámico
    busqueda = st.text_input("🔍 Buscar por nombre del apunte o materia...")
    
    # Filtrar datos
    datos = pd.DataFrame(st.session_state.repositorio)
    resultado = datos[datos['semestre'] == filtro_semestre]
    
    if busqueda:
        resultado = resultado[resultado['titulo'].str.contains(busqueda, case=False) | resultado['materia'].str.contains(busqueda, case=False)]

    if not resultado.empty:
        for index, row in resultado.iterrows():
            with st.expander(f"📄 {row['titulo']} - {row['materia']}"):
                st.write(f"**Autor:** {row['autor']} | **Fecha:** {row['fecha']}")
                if es_semana_parciales:
                    st.button("🔒 Archivo Bloqueado", disabled=True, key=f"btn_{index}")
                else:
                    st.download_button("⬇️ Descargar PDF (Simulado)", data="Contenido del archivo", file_name=f"{row['titulo']}.pdf", key=f"btn_{index}")
    else:
        st.info("No se encontraron apuntes para este filtro.")

# --- VISTA: SUBIR ---
elif menu == "Subir Material":
    st.title("📤 Compartir Conocimiento")
    st.write("Tu aporte ayuda a la comunidad académica.") [cite: 119]
    
    with st.form("upload_form"):
        nuevo_titulo = st.text_input("Título del apunte")
        nueva_materia = st.selectbox("Materia", ["Cálculo I", "Redes I", "Programación", "Metodología", "Física"])
        archivo = st.file_uploader("Selecciona el archivo (PDF, DOCX)", type=['pdf', 'docx', 'png', 'jpg'])
        
        enviar = st.form_submit_button("Publicar Apunte")
        
        if enviar:
            if nuevo_titulo and archivo:
                nuevo_item = {
                    "titulo": nuevo_titulo,
                    "materia": nueva_materia,
                    "semestre": filtro_semestre,
                    "autor": "Usuario Actual",
                    "fecha": datetime.now().strftime("%Y-%m-%d")
                }
                st.session_state.repositorio.append(nuevo_item)
                st.success("✅ ¡Apunte subido con éxito al repositorio!")
            else:
                st.error("Por favor rellena todos los campos.")
