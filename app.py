import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de la Página
st.set_page_config(page_title="EduShare | Gamificación", page_icon="📚", layout="wide")

# 2. Inicialización del Estado con Protección contra KeyError
if 'repositorio' not in st.session_state:
    st.session_state.repositorio = [
        {"titulo": "Guía de Metodología", "materia": "Metodología", "semestre": 1, "autor": "Sistema", "fecha": "2024-05-01", "likes": 5},
        {"titulo": "Apuntes de Cálculo", "materia": "Cálculo I", "semestre": 1, "autor": "Admin", "fecha": "2024-05-02", "likes": 3}
    ]

# 3. Lógica de Control de Acceso
dias_parciales = [15, 16, 17, 18, 19, 20] 
dia_actual = datetime.now().day
bloqueo_activo = dia_actual in dias_parciales

# --- SIDEBAR ---
st.sidebar.title("🚀 EduShare")
menu = st.sidebar.radio("Menú Principal", ["Explorar Material", "Subir Apuntes", "Ranking de Colaboradores"])

st.sidebar.divider()
filtro_semestre = st.sidebar.selectbox("Filtrar por Semestre", [1, 2, 3, 4, 5])

# --- VISTA 1: EXPLORAR ---
if menu == "Explorar Material":
    st.title("📂 Repositorio Académico")
    
    if bloqueo_activo:
        st.error("⚠️ Modo parciales: Descargas bloqueadas por integridad académica.")
    
    busqueda = st.text_input("🔍 Buscar material...")
    
    # Filtrar y asegurar que existan los likes
    for i, item in enumerate(st.session_state.repositorio):
        # Solución al KeyError: Si no existe la llave 'likes', la creamos en 0
        if 'likes' not in item:
            st.session_state.repositorio[i]['likes'] = 0
            
        if item['semestre'] == filtro_semestre and (busqueda.lower() in item['titulo'].lower() or busqueda.lower() in item['materia'].lower()):
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 1, 1])
                with c1:
                    st.subheader(item['titulo'])
                    st.caption(f"Materia: {item['materia']} | Autor: {item['autor']}")
                with c2:
                    # Usamos .get() para evitar errores si la llave desaparece
                    likes_actuales = item.get('likes', 0)
                    st.write(f"👍 {likes_actuales} Reconocimientos")
                    if st.button(f"Valorar", key=f"lk_{i}"):
                        st.session_state.repositorio[i]['likes'] += 1
                        st.rerun()
                with c3:
                    if bloqueo_activo:
                        st.button("🔒 Bloqueado", disabled=True, key=f"dl_{i}")
                    else:
                        st.download_button("⬇️ Descargar", data="PDF", file_name=f"{item['titulo']}.pdf", key=f"dl_{i}")

# --- VISTA 2: SUBIR ---
elif menu == "Subir Apuntes":
    st.title("📤 Subir Material")
    with st.form("form_subida", clear_on_submit=True):
        t = st.text_input("Título del apunte")
        m = st.text_input("Materia")
        s = st.slider("Semestre", 1, 5, filtro_semestre)
        arch = st.file_uploader("Archivo")
        if st.form_submit_button("Publicar"):
            if t and m and arch:
                st.session_state.repositorio.append({
                    "titulo": t, "materia": m, "semestre": s, 
                    "autor": "Estudiante", "fecha": datetime.now().strftime("%Y-%m-%d"), "likes": 0
                })
                st.success("¡Material publicado con éxito!")
                st.rerun()

# --- VISTA 3: RANKING (GAMIFICACIÓN) ---
else:
    st.title("🏆 Ranking de Colaboradores")
    st.write("Estudiantes que más han aportado a la comunidad.")
    
    df = pd.DataFrame(st.session_state.repositorio)
    
    if not df.empty:
        # Aseguramos que la columna likes exista en el DataFrame para evitar el segundo error
        if 'likes' not in df.columns:
            df['likes'] = 0
            
        # Agrupar por materia para ver cuáles son las más apoyadas
        materia_stats = df.groupby('materia')['likes'].sum().reset_index()
        st.bar_chart(data=materia_stats, x='materia', y='likes')
        
        # Tabla de líderes
        st.table(df[['titulo', 'autor', 'likes']].sort_values(by='likes', ascending=False))
    else:
        st.info("Aún no hay datos para mostrar el ranking.")
