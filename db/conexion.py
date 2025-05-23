
from sqlalchemy import create_engine
import os

def get_engine():
    usuario = os.getenv("DB_USER")
    contrasena = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST", "localhost")
    puerto = os.getenv("DB_PORT", "5432")
    nombre_bd = os.getenv("DB_NAME")

    engine = create_engine(f"postgresql+psycopg2://{usuario}:{contrasena}@{host}:{puerto}/{nombre_bd}")
    return engine
