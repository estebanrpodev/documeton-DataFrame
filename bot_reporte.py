# ============================================
# BOT DE VENTAS - Guía de referencia
# Código completo hasta donde vamos, con espacios 
# comentados para las partes que ustedes completan
# ============================================
import pandas as pd
from datos import cargar_datos
import matplotlib.pyplot as plt

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

# --------------------------------------------
# PARTE 4: Limpieza de datos
# --------------------------------------------
filas_antes = len(df_consolidado)
df_consolidado = df_consolidado.drop_duplicates()
print(f"Filas antes: {filas_antes} - después: {len(df_consolidado)}")

print(df_consolidado.isnull().sum())
# completar: decidan qué valor tiene sentido para cada columna con nulos

# --------------------------------------------
# PARTE 5: Guardar el resultado
# --------------------------------------------
df_consolidado.to_excel("consolidado_limpio.xlsx", index=False)
print("Archivo guardado")

# --------------------------------------------
# PARTE 6: Análisis y visualización (NUEVO - hoy)
# --------------------------------------------

# 6a. EJEMPLO RESUELTO: ventas por categoría (gráfico de barras)
ventas_por_categoria = df_consolidado.groupby('categoria')['precio_unitario'].sum()  # Agrupa y suma por categoría
ventas_por_categoria.plot(kind='bar', title='Ventas por Categoria')  # Crea el gráfico de barras
plt.ticklabel_format(style='plain', axis='y')  # Evita notación científica (1e6)
plt.ylabel('Ventas totales ($)')
plt.xlabel('Categoría')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("grafico_ventas_categoria.png")
plt.show()

# 6b. EJEMPLO RESUELTO: participación por vendedor (gráfico de torta)
ventas_por_vendedor = df_consolidado.groupby('vendedor')['precio_unitario'].sum()  # Agrupa y suma por vendedor
ventas_por_vendedor.plot(kind='pie', autopct='%1.1f%%', title='Participacion de Ventas por Vendedor')  # Grafico de torta con porcentajes
plt.ylabel('')  # No aplica en gráficos de torta
plt.tight_layout()
plt.savefig("grafico_ventas_vendedor.png")
plt.show()

# 6c. AHORA USTEDES: ¿cuál es el producto que aparece más veces 
# en las ventas? Investiguen la función value_counts() y 
# apliquenla a la columna 'producto'
