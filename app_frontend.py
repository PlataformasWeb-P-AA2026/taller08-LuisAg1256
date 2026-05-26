# app_frontend.py
import streamlit as st
import pandas as pd
from base_orm import SessionLocal, Jugador

st.set_page_config(page_title="Taller 08 - Analítica", layout="wide")
st.title("Consola de Integración de Datos y Análisis de Entidades")

session = SessionLocal()
try:
    jugadores = session.query(Jugador).all()
    datos_mapeados = []
    for j in jugadores:
        datos_mapeados.append({
            "nombre_jugador": j.nombre,
            "pais_nacimiento": j.pais_nacimiento.nombre,
            "pais_donde_juega": j.pais_liga.nombre,
            "posicion": j.posicion,
            "edad": j.edad,
            "numero_partidos_seleccion": j.partidos_seleccion,
            "goles_seleccion": j.goles_seleccion,
            "continente": j.pais_nacimiento.continente.nombre
        })
finally:
    session.close()

df = pd.DataFrame(datos_mapeados)

if df.empty:
    st.warning("Estructura de almacenamiento vacía. Ejecute previamente 'migrar_datos.py'.")
else:
    # REPORTE 1: Información detallada de jugadores integrados
    st.subheader("1. Vista General de Entidades ESTRUCTURADAS")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # REPORTE 2: Consolidado por Continente
        st.subheader("2. Consolidado por Continente")
        df_cont = df.groupby("continente").agg(
            numero_jugadores=("nombre_jugador", "count"),
            numero_goles=("goles_seleccion", "sum")
        ).reset_index()
        st.dataframe(df_cont, use_container_width=True, hide_index=True)
        
    with col2:
        # REPORTE 3: Consolidado por País (Etiquetado según requerimiento como 'paise')
        st.subheader("3. Consolidado por País")
        df_pais = df.groupby("pais_nacimiento").agg(
            numero_jugadores=("nombre_jugador", "count"),
            numero_goles=("goles_seleccion", "sum")
        ).reset_index().rename(columns={"pais_nacimiento": "paise"})
        st.dataframe(df_pais, use_container_width=True, hide_index=True)