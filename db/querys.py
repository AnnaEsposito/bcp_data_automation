import pandas as pd
from sqlalchemy import text
from db.conexion import get_engine
import unicodedata
import re

engine = get_engine()

def corregir_caracteres(texto: str) -> str:
    # Reemplazar caracteres problemáticos
    if pd.isna(texto):
        return ''
    texto = texto.replace('¡', 'í')  # Reemplazar '¡' por 'í'
    # Puedes añadir más reemplazos según sea necesario
    return texto

def cargar_hechos_cuadro6(df: pd.DataFrame, id_indicador: int, id_fuente: int, id_unidad: int):

    with engine.connect() as conn:
        query_6 = text("""
            SELECT d.id_detalle, 
                   CASE 
                       WHEN d.id_actividad IS NOT NULL AND a.nombre_actividad IS NOT NULL THEN a.nombre_actividad
                       WHEN d.id_compuesta IS NOT NULL AND ac.nombre_compuesto IS NOT NULL THEN ac.nombre_compuesto
                       ELSE d.nombre_detalle
                   END AS nombre
            FROM detalle_indicador d
            LEFT JOIN actividad_economica a ON d.id_actividad = a.id_actividad
            LEFT JOIN actividad_compuesta ac ON d.id_compuesta = ac.id_compuesta
        """)
        resultado = conn.execute(query_6).fetchall()
        # Crear un diccionario: actividad normalizada → id_detalle
        actividad_a_id = {
           corregir_caracteres(row.nombre): row.id_detalle
             for row in resultado
        }

        registros_nuevos = []

        for _, fila in df.iterrows():
            nombre_act = fila['Actividad Economica']
            id_detalle = actividad_a_id.get(nombre_act)

            if not id_detalle:
                print(f"[!] Actividad no encontrada: {fila['Actividad Economica']}")
                continue

            #Verificar si ya existe el registro
            existe = conn.execute(text("""
                SELECT 1 FROM hecho_economico
                WHERE id_detalle = :id_detalle AND fecha = :fecha AND valor = :valor
                """), {
                'id_detalle': id_detalle,
                'fecha': fila['Fecha'],
                'valor': fila['Valor']
            }).fetchone()

            if not existe:
                registros_nuevos.append({
                    'id_detalle': id_detalle,
                    'fecha': fila['Fecha'],
                    'valor': fila['Valor'],
                    'id_fuente': id_fuente,
                    'id_unidad': id_unidad
               })

        if registros_nuevos:
            df_nuevos = pd.DataFrame(registros_nuevos)
            df_nuevos.to_sql('hecho_economico', con=conn, if_exists='append', index=False)
            print(f"[✔] Se insertaron {len(df_nuevos)} registros nuevos en hecho_economico.")
            
             # Asegúrate de hacer commit si usas transacciones
            conn.commit()
        else:
            print("[ℹ] No hay nuevos registros para insertar.")
            
def cargar_hechos_cuadro7(df: pd.DataFrame, id_indicador: int, id_fuente: int, id_unidad: int):

    with engine.connect() as conn:
        # Obtener el mapeo adecuado para id_detalle considerando id_indicador
        query_detalles = text("""
            SELECT d.id_detalle, 
                   COALESCE(a.nombre_actividad, ac.nombre_compuesto, d.nombre_detalle) AS nombre,
                   d.id_indicador
            FROM detalle_indicador d
            LEFT JOIN actividad_economica a ON d.id_actividad = a.id_actividad
            LEFT JOIN actividad_compuesta ac ON d.id_compuesta = ac.id_compuesta
            WHERE d.id_indicador = :id_indicador
        """)
        
        resultado = conn.execute(query_detalles, {'id_indicador': id_indicador}).fetchall()
        
        # Crear un diccionario para mapear actividad + indicador a id_detalle
        actividad_a_id = {
            (corregir_caracteres(row.nombre), row.id_indicador): row.id_detalle
            for row in resultado
        }

        registros_nuevos = []

        for _, fila in df.iterrows():
            nombre_act = corregir_caracteres(fila['Actividad Economica'])
            key = (nombre_act, id_indicador)
            id_detalle = actividad_a_id.get(key)

            if not id_detalle:
                print(f"[!] Actividad no encontrada: {nombre_act} con id_indicador {id_indicador}")
                continue

            # Verificar si ya existe el registro
            existe = conn.execute(text("""
                SELECT 1 FROM hecho_economico
                WHERE id_detalle = :id_detalle AND fecha = :fecha AND valor = :valor
            """), {
                'id_detalle': id_detalle,
                'fecha': fila['Fecha'],
                'valor': fila['Valor']
            }).fetchone()

            if not existe:
                registros_nuevos.append({
                    'id_detalle': id_detalle,
                    'fecha': fila['Fecha'],
                    'valor': fila['Valor'],
                    'id_fuente': id_fuente,
                    'id_unidad': id_unidad
                })

        # Insertar los nuevos registros
        if registros_nuevos:
            df_nuevos = pd.DataFrame(registros_nuevos)
            df_nuevos.to_sql('hecho_economico', con=conn, if_exists='append', index=False)
            print(f"[✔] Se insertaron {len(df_nuevos)} registros nuevos en hecho_economico.")
            conn.commit()
        else:
            print("[ℹ] No hay nuevos registros para insertar.")