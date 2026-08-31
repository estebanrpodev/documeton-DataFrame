import os
import glob
import pandas as pd

CARPETA_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")

def obtener_archivos_datos():
    """
    Descubre dinamicamente los archivos fuente sucursal_*.csv/.xlsx en la
    carpeta datos/. Se usa glob acotado al prefijo 'sucursal_' y a esa carpeta,
    de modo que NUNCA se leen las salidas de resultados/ (evita el problema de
    re-ejecucion documentado en el README).
    """
    archivos = []
    for patron in ("sucursal_*.csv", "sucursal_*.xlsx"):
        archivos.extend(glob.glob(os.path.join(CARPETA_DATOS, patron)))
    return [a for a in sorted(archivos) if os.path.isfile(a)]

def cargar_datos():
    lista_dataframes = []
    for ruta in obtener_archivos_datos():
        _, nombre = os.path.split(ruta)
        df = pd.read_csv(ruta) if ruta.endswith(".csv") else pd.read_excel(ruta)
        lista_dataframes.append(df)
        print(f"Leido: datos/{nombre} - {len(df)} filas")
    return lista_dataframes
