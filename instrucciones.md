# Manual de instrucciones para poder replicar el repositorio.
---

## 1. Estructura del Directorio de Trabajo

Para asegurar la correcta resolución de rutas relativas por parte del intérprete de Python, el espacio de trabajo debe mantener estrictamente la siguiente jerarquía de archivos y carpetas:

```text
taller08/
├── data/
│   └── jugadores_futbol.csv   # Archivo fuente de datos provisto
├── .gitignore                 # Exclusión de artefactos de compilación y BD locales
├── requirements.txt           # Declaración fija de dependencias y versiones
├── config.py                  # Infraestructura de conexión centralizada
├── base_orm.py                # Definición de entidades y mapeo relacional (ORM)
├── migrar_datos.py            # Pipeline de extracción, transformación y carga (ETL)
├── app_frontend.py            # Interfaz de usuario analítica (Streamlit)
├── instrucciones.md           # Manual técnico de despliegue
└── evidencias.md              # Registro de sustentación de resultados
```
## 2. Activacion de un entorno en python

Entorno para hacer la instalacion de las dependencias necesarias.

```python
# Inicialización del entorno virtual indexado
python3 -m venv venv

# Activación del entorno en sistemas basados en Linux / macOS:
source venv/bin/activate
```

## 3. Instalacion de dependencias

Instalacion de dependencias.

```python
pip install --upgrade pip
pip install -r requirements.txt
```
## 4. Corregir el archivo config.py para hacer uso del puerto, usuario,  contraseña y direccion de la base de datos que usamos dependiendo de que se quiera usar (SQLite, MariaDB, MYSQL, etc.)



## 5. Ejecucion migrar_datos.py

Hacer una revision previa en la carpeta de data para asegurarnos que el archivo .csv se encuentra correcto y listo para usar.

Ejecutar la siguiente instruccion:

```python
python3 migrar_datos.py
```

El archivo nos creara la informacion necesaria, tanto el la base de datos como la insercion de informacion del .csv

## 6. Visualizacion con streamlit

Dentro del apartado de frontend, hacer uso del siguiente comando, visualizara la informacion en formato tabla basada en 3 consultas.
```Bash
streamlit run app_frontend.py
```
