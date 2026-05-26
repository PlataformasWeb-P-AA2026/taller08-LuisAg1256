# config.py
import os
from sqlalchemy import create_engine

def obtener_engine():
    """
    Factoría de conexiones (Engine Factory).
    Evalúa la variable de entorno 'DB_CONNECTION' para conmutar el motor.
    """
    db_env = os.getenv("DB_CONNECTION", "sqlite")
    
    if db_env == "mysql":
        USUARIO = "tu_usuario_aquí"
        PASSWORD = "tu_password_aquí"
        HOST = "localhost"
        PUERTO = "3306"
        BASE_DATOS = "tu_base_datos_aquí"
        
        url_conexion = f"mysql+pymysql://{USUARIO}:{PASSWORD}@{HOST}:{PUERTO}/{BASE_DATOS}"
        return create_engine(url_conexion, echo=False)
        
    else:
        url_conexion = "sqlite:///paises.db"
        return create_engine(url_conexion, echo=False)