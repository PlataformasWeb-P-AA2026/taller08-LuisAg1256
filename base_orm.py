# base_orm.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
# Importación del módulo de infraestructura desacoplado
from config import obtener_engine

Base = declarative_base()

class Continente(Base):
    __tablename__ = 'continentes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    paises = relationship("Pais", back_populates="continente")

class Pais(Base):
    __tablename__ = 'paises'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    continente_id = Column(Integer, ForeignKey('continentes.id'), nullable=False)
    
    continente = relationship("Continente", back_populates="paises")
    jugadores_nacimiento = relationship("Jugador", foreign_keys="[Jugador.pais_nacimiento_id]", back_populates="pais_nacimiento")
    jugadores_liga = relationship("Jugador", foreign_keys="[Jugador.pais_liga_id]", back_populates="pais_liga")

class Jugador(Base):
    __tablename__ = 'jugadores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    posicion = Column(String(50))
    edad = Column(Integer)
    partidos_seleccion = Column(Integer)
    goles_seleccion = Column(Integer)
    
    pais_nacimiento_id = Column(Integer, ForeignKey('paises.id'), nullable=False)
    pais_liga_id = Column(Integer, ForeignKey('paises.id'), nullable=False)
    
    pais_nacimiento = relationship("Pais", foreign_keys=[pais_nacimiento_id], back_populates="jugadores_nacimiento")
    pais_liga = relationship("Pais", foreign_keys=[pais_liga_id], back_populates="jugadores_liga")

engine = obtener_engine()
SessionLocal = sessionmaker(bind=engine)

def inicializar_bd():
    """Genera las estructuras físicas DDL usando el motor importado."""
    Base.metadata.create_all(engine)