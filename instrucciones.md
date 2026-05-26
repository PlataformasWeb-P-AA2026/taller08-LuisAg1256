

# Manual de Despliegue y Replicabilidad - Taller 08

Este documento detalla el procedimiento técnico estándar para inicializar, poblar y ejecutar el ecosistema de integración de datos y presentación analítica. El proyecto implementa un patrón modular separando la capa de infraestructura (`config.py`), el modelo de datos del ORM (`base_orm.py`), la ingesta ETL (`migrar_datos.py`) y la interfaz analítica (`app_frontend.py`).

---

## 1. Estructura del Directorio de Trabajo

Para asegurar la correcta resolución de rutas relativas por parte del intérprete de Python, el espacio de trabajo debe mantener la siguiente jerarquía de archivos y carpetas:

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
---

## 2. Secuencia Estricta de Ejecución (Entorno por defecto: SQLite)

Siga los siguientes comandos en la terminal de su sistema operativo para replicar el entorno de desarrollo y evaluar los entregables.

### Paso 1: Configuración del Entorno Virtual de Aislamiento

Inicialice y active un entorno controlado ejecutor:

```bash
# Inicialización del entorno virtual indexado
python3 -m venv venv

# Activación del entorno en sistemas basados en Linux / macOS:
source venv/bin/activate

```

*Nota para sistemas Windows: Si realiza la evaluación en una consola PowerShell, ejecute en su lugar: `.\venv\Scripts\Activate.ps1*`

### Paso 2: Provisión de Dependencias

Con el entorno virtual activo en la terminal, proceda con la instalación de los paquetes mediante el gestor oficial:

```bash
pip install --upgrade pip
pip install -r requirements.txt

```

### Paso 3: Pipeline de Ingesta y Persistencia de Datos (Capa ETL)

Verifique que el archivo de datos origen se encuentre almacenado bajo la ruta `data/jugadores_futbol.csv` y ejecute el script de migración:

```bash
python3 migrar_datos.py

```

*Validación:* El script compilará de forma automática las sentencias DDL necesarias sobre el motor. Al finalizar con éxito, se visualizará un mensaje de confirmación transaccional y se creará el archivo plano local `paises.db` en la raíz.

### Paso 4: Inicialización del Servidor de Presentación (Capa Frontend)

Para desplegar el frontend analítico y renderizar las tres tablas estadísticas consolidadas solicitadas, ejecute:

```bash
streamlit run app_frontend.py

```

*Validación:* El framework de Streamlit reservará un puerto de escucha en el Host local (por defecto `http://localhost:8501`) e iniciará de manera autónoma una pestaña en el navegador web.

---

## 3. Conmutación y Evaluación en Servidores de Producción (Punto 5: MySQL / MariaDB)

Para validar el desacoplamiento de la arquitectura de la aplicación y la persistencia sobre un motor Cliente-Servidor externo, realice los siguientes pasos:

### Paso 1: Inicialización del Esquema Destino

Acceda a su gestor de bases de datos local o de red y cree un esquema vacío ejecutando la siguiente sentencia SQL:

```sql
CREATE DATABASE paises_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

```

### Paso 2: Parametrización de Credenciales

Abra el archivo `config.py` ubicado en la raíz del proyecto y modifique los valores asignados a las variables de conexión del bloque condicional de MySQL con sus accesos locales:

```python
USUARIO = "su_usuario_aquí"        # Ejemplo: "root"
PASSWORD = "su_contraseña_aquí"    # La contraseña de su servidor
HOST = "localhost"                 # IP o Host del servidor
PUERTO = "3306"                    # Puerto por defecto del motor
BASE_DATOS = "paises_db"           # Esquema creado en el Paso 1

```

### Paso 3: Definición de Variables y Ejecución del Pipeline

Con el entorno virtual activo, declare la variable de entorno para forzar al ORM a conmutar el motor físico en caliente y ejecute la secuencia de migración y renderizado:

#### En sistemas Linux / macOS:

```bash
# Activar la redirección del tráfico del ORM hacia MySQL/MariaDB
export DB_CONNECTION=mysql

# Compilar DDL e inyectar los registros procesados
python3 migrar_datos.py

# Levantar la interfaz gráfica analítica
streamlit run app_frontend.py

```

#### En sistemas Windows (PowerShell):

```powershell
# Activar la redirección del tráfico del ORM hacia MySQL/MariaDB
$env:DB_CONNECTION="mysql"

# Compilar DDL e inyectar los registros procesados
python3 .\migrar_datos.py

# Levantar la interfaz gráfica analítica
streamlit run .\app_frontend.py

```

*Validación:* Al correr `migrar_datos.py` se desplegará el mensaje del Commit transaccional exitoso. Puede comprobar la inserción física realizando un `SELECT * FROM (jugadores, continenetes, paises);` directamente en su cliente de base de datos relacional para contrastar con las estructuras en el frontend.
