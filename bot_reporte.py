import pandas as pd
import glob 

# 1. Buscar datos y leer archivos

df_medellin = pd.read_csv("sucursal_medellin.csv")
#print(df_medellin)

df_bogota = pd.read_excel("sucursal_bogota.xlsx")
#print(df_bogota.head(3))

#print(df_medellin.columns)
#print(df_bogota.columns)
archivo_csv = glob.glob("*.csv")
print(f"Archivo_csv {archivo_csv}")

archivo_xlsx = glob.glob("*.xlsx")
print(f"Archivo_xlsx {archivo_xlsx}")

# 2. Guardar en una lista

lista_dataframes = []

for archivo in archivo_csv:
    df = pd.read_csv(archivo)
    lista_dataframes.append(df)
    print(f"Leido: {archivo} - {len(df)} filas")

for archivo in archivo_xlsx:
    df = pd.read_excel(archivo)
    lista_dataframes.append(df)
    print(f"Leido: {archivo} - {len(df)} filas")