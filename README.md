# Bot de Ventas - Consolidado de Reportes

Script en Python con `pandas` que lee los reportes de ventas de 4 sucursales (Medellín, Bogotá, Cali y Barranquilla), los consolida, limpia y genera un Excel final más gráficos de análisis con `matplotlib`.

## Estructura

```
├── datos/                     # Archivos fuente (NO se modifican)
│   ├── sucursal_medellin.csv      # Formato estándar
│   ├── sucursal_bogota.xlsx       # Con nombres de columnas distintos
│   ├── sucursal_cali.csv          # Formato estándar
│   ├── sucursal_barranquilla.xlsx # Formato estándar
│   └── sucursal_*_reporte2.csv    # Reportes nuevos que arrastras a su tiempo
├── resultados/                # Salidas generadas por los scripts
│   ├── consolidado_limpio.xlsx    # Consolidado limpio y normalizado
│   ├── grafico_categoria.png      # Barras: ventas por categoría
│   ├── grafico_vendedor.png       # Torta: participación por vendedor
│   └── log_automatizacion.txt     # Registro de cada proceso de automatización
├── bot_reporte.py             # Script principal: consolida, limpia, analiza y grafica (una vez)
├── automatizar.py             # Bot que vigila datos/ y procesa reportes nuevos en automático
├── datos.py                   # Descubre los archivos fuente y los carga en DataFrames
└── README.md
```

## Cómo ejecutar

```bash
python bot_reporte.py
```

Puedes ejecutarlo las veces que quieras: los archivos generados en `resultados/` no interfieren en la siguiente ejecución.

## Automatización (automatizar.py)

El sistema ahora puede **vigilar la carpeta `datos/`** y procesar reportes nuevos automáticamente, sin que tengas que editar el código ni ejecutar nada a mano.

### Qué hace el sistema

Deja corriendo `automatizar.py` y él se encarga de todo: relee los reportes de las sucursales, los normaliza y consolida, limpia los datos, actualiza el Excel consolidado, regenera los dos gráficos y va guardando un **log** con cada proceso. Es como un empleado que está pendiente de la carpeta todo el tiempo.

### Cómo detecta los archivos nuevos

Funciona con `glob` para descubrir los archivos fuente y con una comparación de nombres:

1. Al arrancar, toma una "foto" de los nombres de archivos que ya hay en `datos/` (`sucursal_*.csv` y `sucursal_*.xlsx`).
2. Cada **5 segundos** vuelve a listar la carpeta y la compara con esa foto.
3. Si aparece un nombre que no estaba antes (por ejemplo `sucursal_cali_reporte2.csv`), ahí hay un archivo nuevo.

### Qué pasa cuando encuentra uno

Cuando detecta un archivo nuevo:

1. Imprime en consola `Nuevo archivo detectado: {...}` con su nombre.
2. Vuelve a leer **todos** los reportes con `glob` (los originales + el nuevo), los normaliza y los consolida en un solo DataFrame.
3. Limpia duplicados y rellena los nulos (método de pago y vendedor con `'Desconocido'`, precio con la mediana del producto).
4. Sobre-escribe `resultados/consolidado_limpio.xlsx` y regenera `grafico_categoria.png` y `grafico_vendedor.png`.
5. **Agrega** una entrada en `resultados/log_automatizacion.txt` con la fecha/hora, el archivo detectado y el total de registros procesados.
6. Sigue vigilando, listo para el siguiente archivo.

### Ejecutar la automatización

```bash
python automatizar.py
```

Imprime `Monitoreando carpeta 'datos/'...`. Deja el script corriendo y arrastra los nuevos reportes a `datos/`, uno a la vez. Para detenerlo usa `Ctrl+C`. El script `bot_reporte.py` sigue disponible si quieres procesar todo una sola vez.

## Qué hace el script (bot_reporte.py)

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
   - Producto que más veces aparece en las ventas (`value_counts()`), reportando empates si los hay.

## Resultados

Números reales de la última ejecución del script.

### Limpieza de datos

- Filas leídas: **66** → filas limpias: **63** (se eliminaron **3 duplicados**, todos de Cali)
- Valores nulos corregidos:
  - `metodo_pago`: 14 → rellenados con `'Desconocido'`
  - `vendedor`: 2 → rellenados con `'Desconocido'`
  - `precio_unitario`: 3 → rellenados con la mediana del mismo producto

### Producto más vendido

Empate en el primer puesto con **10 ventas** cada uno:

| Producto | Apariciones |
|---|---|
| Jean clasico | 10 |
| Cargador USB-C | 10 |
| Camiseta basica | 9 |
| Medias deportivas | 7 |

### Ventas por categoría

| Categoría | Ventas totales* |
|---|---|
| Electrónica | $3.323.700 |
| Ropa | $2.623.100 |
| **Total general** | **$5.946.800** |

### Participación por vendedor

| Vendedor | Ventas | % del total |
|---|---|---|
| Camila Ruiz | $1.696.600 | 28,5% |
| Andres Gomez | $1.381.700 | 23,2% |
| Sofia Mena | $1.322.300 | 22,2% |
| Felipe Torres | $699.000 | 11,8% |
| Laura Diaz | $660.500 | 11,1% |
| Desconocido | $186.700 | 3,1% |

### Métodos de pago

Tarjeta: 17 ventas · Efectivo: 16 · Transferencia: 16 · Desconocido: 14

Los gráficos con estos resultados quedan en `resultados/grafico_categoria.png` y `resultados/grafico_vendedor.png`.

\* Los totales corresponden a la suma de `precio_unitario` por venta, igual que en los gráficos.

## Historial del problema de re-ejecución

En la primera versión, el script usaba `glob.glob("*.csv")` y `glob.glob("*.xlsx")` para descubrir los archivos a leer. El problema: al ejecutar, el propio script generaba los consolidados en la raíz, y en la **segunda ejecución** esos archivos también eran leídos. Al aplicarles el renombrado quedaban columnas duplicadas y `pd.concat()` fallaba con:

```
pandas.errors.InvalidIndexError: Reindexing only valid with uniquely valued Index objects
```

La solución fue doble:

1. **Módulo `datos.py`**: define los archivos fuente de forma confiable. Ahora, en lugar de una lista fija, usa `obtener_archivos_datos()` con **glob acotado**: solo busca `sucursal_*.csv` y `sucursal_*.xlsx` dentro de la carpeta `datos/`. Como las salidas viven en `resultados/` y no empiezan con `sucursal_`, nunca vuelven a ser leídas.
2. **Carpetas separadas**: los datos viven en `datos/` y las salidas en `resultados/`, así nunca se mezclan.
3. **Guardar sin índice**: los Excel de salida se guardan con `index=False`, evitando la columna extra `Unnamed: 0` al volver a leerlos.
