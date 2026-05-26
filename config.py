# config.py
import os
from sqlalchemy import create_engine

def obtener_engine():
    """
    Factoría de conexiones (Engine Factory).
    Centraliza la configuración de los entornos de bases de datos.
    Evalúa la variable de entorno 'DB_CONNECTION' para conmutar el motor.
    """
    db_env = os.getenv("DB_CONNECTION", "sqlite")
    
    if db_env == "mysql":
        # PArametros para MariaDB o MYSQL
        USUARIO = "root"
        PASSWORD = "password"
        HOST = "localhost"
        PUERTO = "3306"
        BASE_DATOS = "paises_db"
        
        url_conexion = f"mysql+pymysql://{USUARIO}:{PASSWORD}@{HOST}:{PUERTO}/{BASE_DATOS}"
        return create_engine(url_conexion, echo=False)
        
    else:
        url_conexion = "sqlite:///paises.db"
        return create_engine(url_conexion, echo=False)