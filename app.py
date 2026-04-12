import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client

# 1. Configuración de la Página
st.set_page_config(page_title="EduShare | Base de Datos Real", layout="wide")

# 2. CONEXIÓN A SUPABASE
# IMPORTANTE: Reemplaza estos valores con los de tu proyecto en Supabase (Settings -> API)
URL_SUPABASE = "https://cofdpzmpkwiybeffqntk.supabase.co"
KEY_SUPABASE = "sb_publishable_zzPPoqndQZyUpwrnJ45ifg_vT0sfy6S"

@st.cache_resource
def init_connection():
    return create_client(URL_SUPABASE, KEY_SUPABASE)

try:
    supabase = init_connection()
except Exception as e:
    st.error("Error de conexión a la base de datos. Verifica tus llaves.")

# Funciones de base de datos
def obtener_datos():
    # Trae todos los registros de la tabla 'repositorio'
    response = supabase.table("repositorio").select("*").execute()
    return response.data

def actualizar_likes(id_registro, likes_actuales):
    supabase.table("repositorio").update({"likes": likes_actuales + 1}).eq("id", id_registro).execute()

def insertar_material(titulo, materia, semestre):
    nuevo = {
        "titulo": titulo, 
        "materia": materia, 
        "semestre": semestre, 
        "autor": "Estudiante", 
        "likes": 0
    }
    supabase.table("repositorio").insert(nuevo).execute()

# 3. Lógica de Calendario
dia_hoy = datetime.now().day
bloqueo_activo = 15 <= dia_hoy <= 20

# --- INTERFAZ ---
st.title("🎓 EduShare: Repositorio Permanente")

with st.sidebar:
    st.header("Menú Principal")
    opcion = st.radio("Secciones", ["Explorar Material", "Subir Material", "Ranking y Estadísticas"])
    st.divider()
    sem_busqueda = st.selectbox("Filtrar por Semestre", list(range(1, 11)))

# --- VISTA: EXPLORAR ---
if opcion == "Explorar Material":
    st.subheader(f"📂 Archivos del Semestre {sem_busqueda}")
    
    if bloqueo_activo:
        st.warning("⚠️ Modo Exámenes: Descargas deshabilitadas por política de integridad.")

    # Obtenemos datos de la nube
    datos_nube = obtener_datos()
    
    if datos_nube:
        hay_material = False
        for item in datos_nube:
            if item['semestre'] == sem_busqueda:
                hay_material = True
                with st.container(border=True):
                    c1, c2, c3 = st.columns([3, 1, 1])
                    with c1:
                        st.markdown(f"### {item['titulo']}")
                        st.caption(f"Materia: {item['materia']} | Autor: {item['autor']}")
                    with c2:
                        st.write(f"⭐ {item['likes']} Reconocimientos")
                        if st.button("Valorar", key=f"lk_{item['id']}"):
                            actualizar_likes(item['id'], item['likes'])
                            st.rerun()
                    with c3:
                        if not bloqueo_activo:
                            st.download_button("📥 Descargar", data="PDF", file_name=f"{item['titulo']}.pdf", key=f"dl_{item['id']}")
                        else:
                            st.button("🔒 Bloqueado", disabled=True, key=f"lock_{item['id']}")
        
        if not hay_material:
            st.info("No hay material registrado para este semestre.")
    else:
        st.info("La base de datos está vacía.")

# --- VISTA: SUBIR ---
elif opcion == "Subir Material":
    st.subheader("📤 Cargar Nuevo Material a la Nube")
    with st.form("form_registro", clear_on_submit=True):
        t = st.text_input("Título del Documento")
        m = st.text_input("Asignatura")
        s = st.number_input("Semestre", 1, 10, sem_busqueda)
        f = st.file_uploader("Adjuntar Archivo (PDF/Imagen)")
        
        if st.form_submit_button("Subir Permanentemente"):
            if t and m and f:
                insertar_material(t, m, s)
                st.success("✅ ¡El material ha sido guardado en la base de datos!")
            else:
                st.error("Por favor completa todos los campos.")

# --- VISTA: RANKING ---
else:
    st.subheader("📊 Análisis de Colaboración")
    datos = obtener_datos()
    if datos:
        df = pd.DataFrame(datos)
        # Gráfica de barras por materia
        stats = df.groupby('materia')['likes'].sum().reset_index()
        st.bar_chart(data=stats, x='materia', y='likes')
        # Tabla completa
        st.dataframe(df[['titulo', 'materia', 'likes', 'autor']], use_container_width=True)
