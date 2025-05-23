import pandas as pd
import re
import unicodedata

def limpiar_actividad(nombre: str) -> str:
    if pd.isna(nombre):
        return ''
    
    # 1. Eliminar espacios dobles o múltiples
    nombre = re.sub(r'\s+', ' ', nombre).strip()
    
    # 2. Eliminar tildes y caracteres no ASCII
    nombre = unicodedata.normalize('NFKD', nombre).encode('ASCII', 'ignore').decode('utf-8')

    # 3. Reemplazos específicos para unificar nombres
    reemplazos = {
        'Valor agregado bruto a precios basicos': 'Valor agregado bruto',
        'Ganaderia forestal, pesca y mineria': 'Ganaderia, forestal, pesca y mineria'  # unificado sin tilde ni coma
    }
    return reemplazos.get(nombre, nombre)  # Devuelve el reemplazo o el nombre limpio

def limpieza(texto):
   #eliminar espacios
    texto = re.sub(r'\s{2,}', ' ', texto).strip()
    texto= unicodedata.normalize('NFKD',texto).encode('ascii','ignore').decode('utf-8')
    return texto


def transform_frame_6(file_path: str) -> pd.DataFrame:
    df_raw = pd.read_excel(file_path, sheet_name=7, header=10)

    # Completar valores faltantes en la primera columna
    df_raw.iloc[:, 0] = df_raw.iloc[:, 0].ffill()

    # Mapear trimestres a fechas
    trimestre_map = {
        'I': '-3-31',
        'II': '-6-30',
        'III': '-9-30',
        'IV': '-12-31'
    }

    # Extraer año y trimestre, y formar fecha
    df_raw.iloc[:, 0] = df_raw.iloc[:, 0].astype(str).str.extract(r"(\d{4})")[0]
    df_raw.iloc[:, 1] = df_raw.iloc[:, 1].astype(str).str.strip()
    df_raw['Fecha'] = df_raw.iloc[:, 0] + df_raw.iloc[:, 1].map(trimestre_map)
    df_raw['Fecha'] = pd.to_datetime(df_raw['Fecha'], format='%Y-%m-%d')

    # Reestructurar a formato largo
    df_long = pd.melt(
        df_raw,
        id_vars=['Fecha'],
        value_vars=df_raw.columns[2:-1],
        var_name='Actividad Economica',
        value_name='Valor'
    )

    # Aplicar limpieza a los nombres de actividad económica
    df_long['Actividad Economica'] = df_long['Actividad Economica'].apply(limpiar_actividad)

    # Eliminar filas con Fecha o Valor vacíos
    df_long = df_long.dropna(subset=['Fecha', 'Valor'])

    return df_long


def transform_cuadro_7(filepath):
    df = pd.read_excel(filepath,sheet_name='CUADRO 7',header=10, nrows=124)
    #rellenar filas combinadas en la columna Ano
    df.iloc[:,0] =df.iloc[:,0].ffill()
    #Eliminar str de la columna Ano
    df.iloc[:,0]=df.iloc[:,0].astype(str).str.replace('[^0-9]', '', regex=True).str.strip()
    
    #Transformar trimestres a fechas trimestrales
    trimestre_map = {
        'I': '-3-31',
        'II': '-6-30',
        'III': '-9-30',
        'IV': '-12-31'
    }    
    df.iloc[:, 1] = df.iloc[:, 1].astype(str).str.strip().map(trimestre_map)
        
    # Crear la columna de fechas unificada
    df['Fecha'] = pd.to_datetime(df.iloc[:, 0] + df.iloc[:, 1], errors='coerce')
    
    #Eliminar las primeras dos columnas
    df.drop(df.columns[:2], axis=1, inplace=True)

    #Derretir columnas

    df_long= pd.melt(
            df,
            id_vars= ['Fecha'],
            value_vars=df.columns[0:-1],
            var_name='Actividad Economica',
            value_name='Valor'
    )
    df_long['Actividad Economica'] = df_long['Actividad Economica'].apply(limpieza)
    return df_long



