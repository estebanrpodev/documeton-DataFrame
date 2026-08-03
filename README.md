# Documeton - Consolidado de Reportes de Ventas

Script en Python con `pandas` que lee los reportes de ventas de 4 sucursales (Medellín, Bogotá, Cali y Barranquilla) y los consolida en archivos Excel.

## Estructura

```
├── datos.py                # Define los archivos fuente y los carga en una lista de DataFrames
├── bot_reporte.py          # Script principal: consolida y normaliza los datos
├── sucursal_medellin.csv   # Datos fuente (formato estándar)
├── sucursal_bogota.xlsx    # Datos fuente (con nombres de columnas distintos)
├── sucursal_cali.csv       # Datos fuente (formato estándar)
├── sucursal_barranquilla.xlsx  # Datos fuente (formato estándar)
├── consolidado_desordenado.xlsx   # Salida generada (columnas sin normalizar)
└── consolidado_semiordenado.xlsx  # Salida generada (columnas normalizadas)
```

## Cómo ejecutar

```bash
python bot_reporte.py
```

Puedes ejecutarlo las veces que quieras: los archivos generados no interfieren en la siguiente ejecución.

## El problema

En la primera versión, el script usaba `glob.glob("*.csv")` y `glob.glob("*.xlsx")` para descubrir los archivos a leer. El problema: al ejecutar, el propio script generaba `consolidado_desordenado.xlsx` y `consolidado_semiordenado.xlsx`, y en la **segunda ejecución** esos archivos generados también eran leídos.

`consolidado_desordenado.xlsx` contiene tanto las columnas originales (`Fecha_Venta`, `Producto`, ...) como las ya normalizadas (`fecha`, `producto`, ...). Al aplicarle el renombrado, quedaban **columnas duplicadas** y `pd.concat()` fallaba con:

```
pandas.errors.InvalidIndexError: Reindexing only valid with uniquely valued Index objects
```

La única forma de volver a ejecutar era borrar manualmente los archivos generados.

## La solución

1. **Crear el módulo `datos.py`**: define una lista fija de los 4 archivos fuente (`ARCHIVOS`) y la función `cargar_datos()`. Al importarlo, `bot_reporte.py` solo lee los datos fuente y nunca los archivos que él mismo genera, así que ya no se usa `glob`.

2. **Guardar sin índice**: los Excel de salida ahora se guardan con `index=False`, evitando la columna extra `Unnamed: 0` que agregaba `pandas` al volver a leerlos.
