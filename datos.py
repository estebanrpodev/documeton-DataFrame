import pandas as pd

ARCHIVOS = [
    "sucursal_medellin.csv",
    "sucursal_bogota.xlsx",
    "sucursal_cali.csv",
    "sucursal_barranquilla.xlsx",
]

def cargar_datos():
    lista_dataframes = []
    for archivo in ARCHIVOS:
        df = pd.read_csv(archivo) if archivo.endswith(".csv") else pd.read_excel(archivo)
        lista_dataframes.append(df)
        print(f"Leido: {archivo} - {len(df)} filas")
    return lista_dataframes
