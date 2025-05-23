import sqlalchemy
import pandas as pd
from sqlalchemy import text
from db.conexion import get_engine

engine = get_engine()

def select_cuadro_6():
    try:
        with engine.connect() as conn:
                query = text("""SELECT valor, fecha, nombre_actividad, nombre_compuesto FROM hecho_economico he
                            INNER JOIN detalle_indicador de ON he.id_detalle=de.id_detalle 
                            LEFT JOIN actividad_economica ae ON de.id_actividad=ae.id_actividad
                            LEFT JOIN actividad_compuesta ac ON de.id_compuesta=ac.id_compuesta
                            WHERE id_indicador = 2;
                            """)
                df = pd.read_sql_query(query,conn)
                return df
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None
    
resultado = select_cuadro_6()
print(resultado.head())