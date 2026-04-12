import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client

# 1. CONFIGURACIÓN
st.set_page_config(page_title="EduShare | Proyecto de Grado", page_icon="🎓", layout="wide")

# 2. CONEXIÓN A SUPABASE (Rellena con tus datos)
URL_SUPABASE = "https://cofdpzmpkwiybeffqntk.supabase.co"
KEY_SUPABASE = "sb_publishable_zzPPoqndQZyUpwrnJ45ifg_vT0sfy6S"

@st.cache_resource
def init_connection():
    return create_client(URL_SUPABASE, KEY_SUPABASE)

supabase = init_connection()

# --- FUNCIONES ---
def obtener_datos():
    try:
        response = supabase.table("repositorio").select("*").execute()
        return response.data
    except:
        return []

def actualizar_likes(id_reg, likes_actuales):
    supabase.table("repositorio").update({"likes": likes_actuales + 1}).eq("id", id_reg).execute()

def insertar_material(titulo, materia, semestre, autor):
    nuevo = {
        "titulo": titulo, 
        "materia": materia, 
        "semestre": semestre, 
        "autor": autor, # Ahora recibe el nombre real
        "likes": 0
    }
    supabase.table("repositorio").insert(nuevo).execute()

# --- INTERFAZ ---
with st.sidebar:
    st.title("🎓 EduShare")
    menu = st.radio("Secciones", ["Explorar Material", "Subir Material", "Estadísticas"])
    st.divider()
    sem_filtro = st.selectbox("Filtrar Semestre", list(range(1, 11)))

# --- VISTA: EXPLORAR ---
if menu == "Explorar Material":
    st.header(f"📂 Repositorio - Semestre {sem_filtro}")
    busqueda = st.text_input("🔍 Buscar por título o autor...")
    
    datos = obtener_datos()
    if datos:
        # Filtro avanzado: Semestre + (Título o Autor)
        items = [d for d in datos if d['semestre'] == sem_filtro and 
                 (busqueda.lower() in d['titulo'].lower() or busqueda.lower() in d['autor'].lower())]
        
        if items:
            for item in items:
                with st.container(border=True):
                    c1, c2, c3 = st.columns([3, 1, 1])
                    with c1:
                        st.subheader(item['titulo'])
                        # AQUÍ YA SE VE EL AUTOR REAL
                        st.markdown(f"**Asignatura:** {item['materia']}  \n**Publicado por:** {item['autor']}")
                    with c2:
                        st.write(f"⭐ {item['likes']} Likes")
                        if st.button("Valorar", key=f"lk_{item['id']}"):
                            actualizar_likes(item['id'], item['likes'])
                            st.rerun()
                    with c3:
                        # Descarga simulada que mantiene el nombre del título
                        st.download_button(
                            label="📥 Descargar",
                            data=f"Contenido del archivo: {item['titulo']}\nAutor: {item['autor']}",
                            file_name=f"{item['titulo']}.pdf", # Le pone la extensión PDF automáticamente
                            key=f"dl_{item['id']}"
                        )
        else:
            st.info("No hay material para mostrar.")

# --- VISTA: SUBIR ---
elif menu == "Subir Material":
    st.header("📤 Compartir Material")
    with st.form("form_subida", clear_on_submit=True):
        nombre_estudiante = st.text_input("Tu Nombre Completo") # NUEVO CAMPO
        titulo_doc = st.text_input("Título del documento")
        materia_doc = st.text_input("Asignatura")
        sem_doc = st.number_input("Semestre", 1, 10, sem_filtro)
        archivo = st.file_uploader("Adjuntar archivo (Cualquier formato)")
        
        if st.form_submit_button("Publicar en EduShare"):
            if nombre_estudiante and titulo_doc and materia_doc and archivo:
                insertar_material(titulo_doc, materia_doc, sem_doc, nombre_estudiante)
                st.success(f"✅ ¡Gracias {nombre_estudiante}! Material guardado con éxito.")
            else:
                st.error("Por favor, llena todos los campos incluyendo tu nombre.")

# --- VISTA: ESTADÍSTICAS ---
else:
    st.header("📊 Ranking de Colaboradores")
    datos = obtener_datos()
    if datos:
        df = pd.DataFrame(datos)
        # Mostrar quién ha aportado más
        st.subheader("Top Autores")
        autor_count = df['autor'].value_counts().reset_index()
        st.table(autor_count.rename(columns={'index': 'Autor', 'autor': 'Aportes'}))
        
        st.subheader("Popularidad por Materia")
        st.bar_chart(df.groupby('materia')['likes'].sum())
