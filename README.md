# Bot de Ventas - Consolidado de Reportes

Script en Python con `pandas` que lee los reportes de ventas de 4 sucursales (Medellín, Bogotá, Cali y Barranquilla), los consolida, limpia y genera un Excel final más gráficos de análisis con `matplotlib`.

## Estructura

```
├── datos/                     # Archivos fuente (NO se modifican)
│   ├── sucursal_medellin.csv      # Formato estándar
│   ├── sucursal_bogota.xlsx       # Con nombres de columnas distintos
│   ├── sucursal_cali.csv          # Formato estándar
│   └── sucursal_barranquilla.xlsx # Formato estándar
├── resultados/                # Salidas generadas por el script
│   ├── consolidado_limpio.xlsx    # Consolidado limpio y normalizado
│   ├── grafico_categoria.png      # Barras: ventas por categoría
│   └── grafico_vendedor.png       # Torta: participación por vendedor
├── main.py                    # Script principal: consolida, limpia, analiza y grafica
├── datos.py                   # Define los archivos fuente y los carga en DataFrames
└── README.md
```

## Cómo ejecutar

```bash
python main.py
```

Puedes ejecutarlo las veces que quieras: los archivos generados en `resultados/` no interfieren en la siguiente ejecución.

## Qué hace el script

1. **Carga**: lee los 4 archivos fuente desde `datos/`, sin importar si son `.csv` o `.xlsx`.
2. **Normaliza**: renombra las columnas de Bogotá (`Fecha_Venta`, `Producto`, ...) al formato estándar del resto.
3. **Limpia**:
   - Elimina filas duplicadas exactas.
   - Rellena nulos en `metodo_pago` y `vendedor` con `'Desconocido'`.
   - Rellena nulos en `precio_unitario` con la mediana del mismo producto.
4. **Guarda**: escribe `resultados/consolidado_limpio.xlsx` con `index=False`.
5. **Analiza y grafica**:
   - Barras: ventas totales por categoría → `resultados/grafico_categoria.png`.
   - Torta: participación de cada vendedor → `resultados/grafico_vendedor.png`.
   - Producto que más veces aparece en las ventas (`value_counts()`).

## Historial del problema de re-ejecución

En la primera versión, el script usaba `glob.glob("*.csv")` y `glob.glob("*.xlsx")` para descubrir los archivos a leer. El problema: al ejecutar, el propio script generaba los consolidados en la raíz, y en la **segunda ejecución** esos archivos también eran leídos. Al aplicarles el renombrado quedaban columnas duplicadas y `pd.concat()` fallaba con:

```
pandas.errors.InvalidIndexError: Reindexing only valid with uniquely valued Index objects
```

La solución fue doble:

1. **Módulo `datos.py`**: define una lista fija de los 4 archivos fuente (`ARCHIVOS`). Al importarlo, `main.py` solo lee los datos fuente y nunca lo que él mismo genera.
2. **Carpetas separadas**: los datos viven en `datos/` y las salidas en `resultados/`, así nunca se mezclan.
3. **Guardar sin índice**: los Excel de salida se guardan con `index=False`, evitando la columna extra `Unnamed: 0` al volver a leerlos.
