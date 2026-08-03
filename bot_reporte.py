import pandas as pd
from datos import cargar_datos

# 1. Cargar solo los archivos fuente (ya no se usa glob.glob,
#    asi los archivos generados no se vuelven a leer)

lista_dataframes = cargar_datos()

# 2. Consolidar (ver problema)
df_consolidado = pd.concat(lista_dataframes, ignore_index=True)
df_consolidado.to_excel("consolidado_desordenado.xlsx", index=False)

# 3. Normalizar nombres de columnas: uno de los 4 archivos (Bogota)
#    tiene columnas con nombres distintos a los demas

for i, df in enumerate(lista_dataframes):
    if 'Fecha_Venta' in df.columns:
        lista_dataframes[i] = df.rename(columns={
            "Fecha_Venta": "fecha",
            "Producto": "producto",
            "Categoria": "categoria",
            "Cant": "cantidad",
            "Valor_Unitario": "precio_unitario",
            "Vendedor": "vendedor",
            "Pago": "metodo_pago"
        })

df_consolidado = pd.concat(lista_dataframes, ignore_index=True)
df_consolidado.to_excel("consolidado_semiordenado.xlsx", index=False)
