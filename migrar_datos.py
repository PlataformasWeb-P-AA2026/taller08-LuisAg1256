# migrar_datos.py
import pandas as pd
from base_orm import inicializar_bd, SessionLocal, Continente, Pais, Jugador

def obtener_continente_por_pais(pais):
    """Mapeo estricto para la resolución del atributo continente ausente en origen."""
    mapeo = {
        'Ecuador': 'América del Sur', 'Argentina': 'América del Sur', 'Brasil': 'América del Sur',
        'Estados Unidos': 'América del Norte', 'México': 'América del Norte',
        'Alemania': 'Europa', 'España': 'Europa', 'Portugal': 'Europa', 'Francia': 'Europa', 'Inglaterra': 'Europa',
        'Japón': 'Asia', 'Marruecos': 'África', 'Senegal': 'África', 'Nigeria': 'África', 'Australia': 'Oceanía'
    }
    return mapeo.get(pais, 'Otros')

def migrar():
    print("[INFO] Inicializando DDL sobre el motor relacional...")
    inicializar_bd()
    session = SessionLocal()
    
    ruta_csv = "data/jugadores_futbol.csv"
    try:
        df = pd.read_csv(ruta_csv)
    except FileNotFoundError:
        print(f"[ERROR] Origen inaccesible en la ruta parametrizada: '{ruta_csv}'")
        return

    print("[INFO] Ingesta en memoria exitosa. Procesando registros a través del ORM...")
    continentes_cache = {}
    paises_cache = {}

    for idx, row in df.iterrows():
        nom_pais_nac = str(row['pais_nacimiento']).strip()
        nom_pais_liga = str(row['pais_donde_juega']).strip()
        
        nom_continente_nac = obtener_continente_por_pais(nom_pais_nac)
        nom_continente_liga = obtener_continente_por_pais(nom_pais_liga)

        # Resolución de entidades Continente
        for nom_cont in [nom_continente_nac, nom_continente_liga]:
            if nom_cont not in continentes_cache:
                cont = session.query(Continente).filter_by(nombre=nom_cont).first()
                if not cont:
                    cont = Continente(nombre=nom_cont)
                    session.add(cont)
                    session.flush()
                continentes_cache[nom_cont] = cont

        # Resolución de entidad Pais de Nacimiento
        if nom_pais_nac not in paises_cache:
            p_nac = session.query(Pais).filter_by(nombre=nom_pais_nac).first()
            if not p_nac:
                p_nac = Pais(nombre=nom_pais_nac, continente=continentes_cache[nom_continente_nac])
                session.add(p_nac)
                session.flush()
            paises_cache[nom_pais_nac] = p_nac

        # Resolución de entidad Pais de la Liga
        if nom_pais_liga not in paises_cache:
            p_liga = session.query(Pais).filter_by(nombre=nom_pais_liga).first()
            if not p_liga:
                p_liga = Pais(nombre=nom_pais_liga, continente=continentes_cache[nom_continente_liga])
                session.add(p_liga)
                session.flush()
            paises_cache[nom_pais_liga] = p_liga

        # Construcción de la entidad raíz estructurada
        nuevo_jugador = Jugador(
            nombre=row['nombre_jugador'],
            posicion=row['posicion'],
            edad=int(row['edad']),
            partidos_seleccion=int(row['numero_partidos_seleccion']),
            goles_seleccion=int(row['goles_seleccion']),
            pais_nacimiento=paises_cache[nom_pais_nac],
            pais_liga=paises_cache[nom_pais_liga]
        )
        session.add(nuevo_jugador)

    try:
        session.commit()
        print("[SUCCESS] Confirmación transaccional (Commit) exitosa.")
    except Exception as e:
        session.rollback()
        print(f"[CRITICAL] Excepción en persistencia. Rollback ejecutado: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    migrar()