import os
import pandas as pd

CARPETA_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")

ARCHIVOS = [
    "sucursal_medellin.csv",
    "sucursal_bogota.xlsx",
    "sucursal_cali.csv",
    "sucursal_barranquilla.xlsx",
]

def cargar_datos():
    lista_dataframes = []
    for archivo in ARCHIVOS:
        ruta = os.path.join(CARPETA_DATOS, archivo)
        df = pd.read_csv(ruta) if archivo.endswith(".csv") else pd.read_excel(ruta)
        lista_dataframes.append(df)
        print(f"Leido: datos/{archivo} - {len(df)} filas")
    return lista_dataframes
