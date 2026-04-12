import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="EduShare | Proyecto de Grado", page_icon="🎓", layout="wide")

# 2. CONEXIÓN A SUPABASE (RELLENA TUS DATOS AQUÍ)
URL_SUPABASE = "https://cofdpzmpkwiybeffqntk.supabase.co"
KEY_SUPABASE = "sb_publishable_zzPPoqndQZyUpwrnJ45ifg_vT0sfy6S"

@st.cache_resource
def init_connection():
    return create_client(URL_SUPABASE, KEY_SUPABASE)

supabase = init_connection()

# --- FUNCIONES DE BASE DE DATOS ---
def obtener_datos():
    # Trae la información de la nube
    try:
        response = supabase.table("repositorio").select("*").execute()
        return response.data
    except:
        return []

def actualizar_likes(id_registro, likes_actuales):
    # Suma un reconocimiento en la nube
    supabase.table("repositorio").update({"likes": likes_actuales + 1}).eq("id", id_registro).execute()

def insertar_material(titulo, materia, semestre):
    # Guarda el registro permanente
    nuevo = {
        "titulo": titulo, 
        "materia": materia, 
        "semestre": semestre, 
        "autor": "Estudiante_U", 
        "likes": 0
    }
    supabase.table("repositorio").insert(nuevo).execute()

# --- LÓGICA DE CONTROL ---
dia_hoy = datetime.now().day
bloqueo_activo = 15 <= dia_hoy <= 20

# --- INTERFAZ LATERAL ---
with st.sidebar:
    st.title("🎓 EduShare")
    menu = st.radio("Secciones", ["Explorar Material", "Subir Material", "Estadísticas"])
    st.divider()
    sem_filtro = st.selectbox("Filtrar Semestre", list(range(1, 11)))
    st.info("Prototipo para Metodología de la Investigación")

# --- VISTA: EXPLORAR ---
if menu == "Explorar Material":
    st.header(f"📂 Repositorio - Semestre {sem_filtro}")
    
    if bloqueo_activo:
        st.error("⚠️ Acceso restringido por periodo de exámenes (Integridad Académica).")
    
    busqueda = st.text_input("🔍 Buscar por título...")
    
    datos = obtener_datos()
    
    if datos:
        # Filtramos por semestre y búsqueda
        items_filtrados = [d for d in datos if d['semestre'] == sem_filtro and busqueda.lower() in d['titulo'].lower()]
        
        if items_filtrados:
            for item in items_filtrados:
                with st.container(border=True):
                    c1, c2, c3 = st.columns([3, 1, 1])
                    with c1:
                        st.subheader(item['titulo'])
                        st.caption(f"Materia: {item['materia']} | Autor: {item['autor']}")
                    with c2:
                        st.write(f"⭐ {item['likes']} Likes")
                        # Controlamos un poco los likes infinitos con session_state
                        if st.button("Valorar", key=f"lk_{item['id']}"):
                            actualizar_likes(item['id'], item['likes'])
                            st.rerun()
                    with c3:
                        if bloqueo_activo:
                            st.button("🔒 Bloqueado", disabled=True, key=f"lock_{item['id']}")
                        else:
                            # Simulamos la descarga de un PDF para evitar el error de archivo vacío
                            st.download_button(
                                label="📥 Descargar",
                                data=f"Contenido del apunte: {item['titulo']}\nEste es un archivo generado por EduShare.",
                                file_name=f"{item['titulo']}.txt",
                                key=f"dl_{item['id']}"
                            )
        else:
            st.info("No se encontró material para este semestre.")
    else:
        st.warning("No hay conexión con la base de datos o la tabla está vacía.")

# --- VISTA: SUBIR ---
elif menu == "Subir Material":
    st.header("📤 Compartir Material")
    with st.form("form_subida", clear_on_submit=True):
        t = st.text_input("Título del documento")
        m = st.text_input("Asignatura")
        s = st.number_input("Semestre", 1, 10, sem_filtro)
        arch = st.file_uploader("Adjuntar archivo")
        
        if st.form_submit_button("Publicar Permanentemente"):
            if t and m and arch:
                insertar_material(t, m, s)
                st.success("✅ ¡Guardado en la nube! Ya puedes verlo en la sección Explorar.")
            else:
                st.error("Completa todos los campos.")

# --- VISTA: ESTADÍSTICAS ---
else:
    st.header("📊 Impacto Académico")
    datos = obtener_datos()
    if datos:
        df = pd.DataFrame(datos)
        st.subheader("Materias con más aportes")
        # Gráfica de barras
        materia_count = df['materia'].value_counts()
        st.bar_chart(materia_count)
        
        st.subheader("Ranking de Calidad (Likes)")
        st.dataframe(df[['titulo', 'materia', 'likes']].sort_values('likes', ascending=False), use_container_width=True)
