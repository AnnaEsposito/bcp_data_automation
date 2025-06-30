from etl.transform import transform_frame_6, transform_cuadro_7
from db.conexion import get_engine
from db.querys import cargar_hechos_cuadro6, cargar_hechos_cuadro7


# Ruta del archivo Excel original
file_path = "C:/Users/Anna Esposito/Desktop/bcp_data_automation/data/raw_excel/Anexo_Estadístico_del_Informe_Económico_28_04_2025(1).xlsx"

# Transformar el archivo al DataFrame limpio
df_long_cuadro_6= transform_frame_6(file_path)
df_long_cuadro7 =transform_cuadro_7(file_path)

# Cargar a la BD
cargar_hechos_cuadro6(df_long_cuadro_6, id_indicador=2, id_fuente=1, id_unidad=1)
cargar_hechos_cuadro7(df_long_cuadro7, id_indicador=3, id_fuente=1, id_unidad=1)
