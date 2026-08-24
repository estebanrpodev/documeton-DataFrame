# ============================================
# BOT DE VENTAS - Script principal
# Lee los reportes de las 4 sucursales (carpeta datos/),
# los consolida, limpia, analiza y guarda todo en resultados/
# ============================================
import os
import pandas as pd
from datos import cargar_datos
import matplotlib.pyplot as plt

# Carpeta donde se guardan todos los resultados
CARPETA_RESULTADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados")
os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

# 1. Cargar solo los archivos fuente de la carpeta datos/
#    (ya no se usa glob.glob, asi los archivos generados no se vuelven a leer)
lista_dataframes = cargar_datos()

# 2. Normalizar nombres de columnas ANTES de consolidar:
#    uno de los 4 archivos (Bogota) tiene columnas con nombres distintos a los demas.
#    Se construye una lista nueva en vez de modificar lista_dataframes mientras se recorre.
dataframes_normalizados = []
for df in lista_dataframes:
    if 'Fecha_Venta' in df.columns:
        df = df.rename(columns={
            "Fecha_Venta": "fecha",
            "Producto": "producto",
            "Categoria": "categoria",
            "Cant": "cantidad",
            "Valor_Unitario": "precio_unitario",
            "Vendedor": "vendedor",
            "Pago": "metodo_pago"
        })
    dataframes_normalizados.append(df)

# 3. Consolidar todo en un solo DataFrame
df_consolidado = pd.concat(dataframes_normalizados, ignore_index=True)

# --------------------------------------------
# PARTE 4: Limpieza de datos
# --------------------------------------------

# 4a. Quitar filas duplicadas exactas
filas_antes = len(df_consolidado)
df_consolidado = df_consolidado.drop_duplicates()
print(f"Filas antes: {filas_antes} - después: {len(df_consolidado)}")

# 4b. Manejo de nulos: decidimos qué valor tiene sentido para cada columna
print("\nNulos por columna antes de la limpieza:")
print(df_consolidado.isnull().sum())

df_consolidado['metodo_pago'] = df_consolidado['metodo_pago'].fillna('Desconocido')
df_consolidado['vendedor'] = df_consolidado['vendedor'].fillna('Desconocido')

# Para el precio usamos la mediana del mismo producto (mas justa que un valor global)
mediana_por_producto = df_consolidado.groupby('producto')['precio_unitario'].transform('median')
df_consolidado['precio_unitario'] = df_consolidado['precio_unitario'].fillna(mediana_por_producto)

print("\nNulos después de la limpieza:", df_consolidado.isnull().sum().sum())

# --------------------------------------------
# PARTE 5: Guardar el resultado
# --------------------------------------------
ruta_salida = os.path.join(CARPETA_RESULTADOS, "consolidado_limpio.xlsx")
df_consolidado.to_excel(ruta_salida, index=False)
print(f"\nArchivo guardado en {ruta_salida}")

# --------------------------------------------
# PARTE 6: Análisis y visualización
# --------------------------------------------

# 6a. Ventas por categoría (gráfico de barras)
ventas_por_categoria = df_consolidado.groupby('categoria')['precio_unitario'].sum()
ventas_por_categoria.plot(kind='bar', title='Ventas por Categoria')
plt.ticklabel_format(style='plain', axis='y')  # Evita notación científica (1e6)
plt.ylabel('Ventas totales ($)')
plt.xlabel('Categoría')
plt.xticks(rotation=0)
plt.tight_layout()  # Ajusta los elementos para que no se corten
plt.savefig(os.path.join(CARPETA_RESULTADOS, "grafico_categoria.png"))
plt.show()
plt.close()  # Cierra la figura para que el siguiente grafico no se dibuje encima

# 6b. Participación por vendedor (gráfico de torta)
ventas_por_vendedor = df_consolidado.groupby('vendedor')['precio_unitario'].sum()
ventas_por_vendedor.plot(kind='pie', autopct='%1.1f%%', title='Participacion de Ventas por Vendedor')
plt.ylabel('')  # No aplica en gráficos de torta
plt.tight_layout()
plt.savefig(os.path.join(CARPETA_RESULTADOS, "grafico_vendedor.png"))
plt.show()
plt.close()  # Buena practica: no dejar figuras abiertas al terminar

# 6c. Productos más vendidos con value_counts()
#     Si hay empate en el primer puesto, se reportan todos los empatados
productos_mas_vendidos = df_consolidado['producto'].value_counts()
print("\nProductos por número de ventas:")
print(productos_mas_vendidos.head(10))

max_ventas = productos_mas_vendidos.max()
empatados = list(productos_mas_vendidos[productos_mas_vendidos == max_ventas].index)
if len(empatados) == 1:
    print(f"\nEl producto más vendido es: {empatados[0]} ({max_ventas} veces)")
else:
    print(f"\nEmpate en el primer puesto con {max_ventas} ventas cada uno:")
    for p in empatados:
        print(f"  - {p}")
