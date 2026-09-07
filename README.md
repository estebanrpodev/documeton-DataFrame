# Bot de Ventas - Consolidado de Reportes

Script en Python con `pandas` que lee los reportes de ventas de 4 sucursales (Medellín, Bogotá, Cali y Barranquilla), los consolida, limpia y genera un Excel final más gráficos de análisis con `matplotlib`.

## Estructura

```
├── datos/                     # Archivos fuente (NO se modifican)
│   ├── sucursal_medellin.csv      # Formato estándar
│   ├── sucursal_bogota.xlsx       # Con nombres de columnas distintos
│   ├── sucursal_cali.csv          # Formato estándar
│   ├── sucursal_barranquilla.xlsx # Formato estándar
│   ├── sucursal_medellin_reporte2.csv    # Reporte nuevo para el bot
│   ├── sucursal_cali_reporte2.csv        # Reporte nuevo para el bot
│   └── sucursal_bucaramanga_reporte2.csv # Reporte nuevo para el bot
├── resultados/                # Salidas generadas por los scripts
│   ├── consolidado_limpio.xlsx    # Consolidado limpio y normalizado
│   ├── grafico_categoria.png      # Barras: ventas por categoría
│   ├── grafico_vendedor.png       # Torta: participación por vendedor
│   ├── resumen_ejecutivo.txt      # Resumen de las 4 métricas clave
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
6. **Imprime un banner** en pantalla con el total de ventas acumuladas.
7. **Reescribe `resultados/resumen_ejecutivo.txt`** con las 4 métricas de negocio (categoría y vendedor top con `idxmax()`, producto más vendido con `value_counts()` y ticket promedio con `mean()`).
8. Sigue vigilando, listo para el siguiente archivo.

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

Números reales de la última ejecución del script (con los 3 reportes nuevos ya consolidados).

### Limpieza de datos

- Filas leídas: **78** → filas limpias: **75** (se eliminaron **3 duplicados**)
- Valores nulos corregidos:
  - `metodo_pago`: 14 → rellenados con `'Desconocido'`
  - `vendedor`: 2 → rellenados con `'Desconocido'`
  - `precio_unitario`: 3 → rellenados con la mediana del mismo producto

### Resumen ejecutivo (4 métricas clave)

En `resultados/resumen_ejecutivo.txt`:

| Métrica | Valor |
|---|---|
| Categoría con mejor desempeño (`idxmax()`) | Electrónica ($6.776.700) |
| Vendedor con más ventas (`idxmax()`) | Carlos ($3.315.000) |
| Producto más vendido (`value_counts()`) | Cargador USB-C (10 ventas) |
| Promedio de venta por transacción (`mean()`) | $133.517 |
| Total de ventas acumuladas | $10.013.800 |

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
| Electrónica | $6.776.700 |
| Ropa | $3.237.100 |
| **Total general** | **$10.013.800** |

### Participación por vendedor

| Vendedor | Ventas | % del total |
|---|---|---|
| Carlos | $3.315.000 | 33,1% |
| Camila Ruiz | $1.696.600 | 16,9% |
| Andres Gomez | $1.381.700 | 13,8% |
| Sofia Mena | $1.322.300 | 13,2% |
| Felipe Torres | $699.000 | 7,0% |
| Laura Diaz | $660.500 | 6,6% |
| Maria | $308.000 | 3,1% |
| Desconocido | $186.700 | 1,9% |
| Juan | $172.000 | 1,7% |
| Ana | $134.000 | 1,3% |
| Sofia | $103.000 | 1,0% |
| Diego | $35.000 | 0,3% |

> En el gráfico `grafico_vendedor.png`, los vendedores que aportan menos del **4%** se agrupan en la tajada **"Otros"** ($938.700) para que la torta siga siendo legible. Carlos, Camila Ruiz, Andres Gomez, Sofia Mena, Felipe Torres y Laura Diaz se muestran individualmente.

### Métodos de pago

Tarjeta: 23 ventas · Efectivo: 22 · Transferencia: 16 · Desconocido: 14

### Promedio de venta por transacción

El ticket promedio de venta es de **$133.517** por transacción.

Los gráficos con estos resultados quedan en `resultados/grafico_categoria.png` y `resultados/grafico_vendedor.png`.

\* Los totales corresponden a la suma de `precio_unitario` por venta, igual que en los gráficos.

## Análisis de negocio (preguntas con las 4 métricas)

Con las **4 métricas del resumen ejecutivo** respondemos las preguntas de negocio:

1. **¿Cuál es la categoría más rentable?** → **Electrónica**. Aporta $6.776.700 de los $10.013.800 totales (casi **68%**). Es el motor del negocio.
2. **¿Cuál es el vendedor estrella?** → **Carlos**, con $3.315.000 (33,1% del total). Prácticamente duplica al segundo, Camila Ruiz ($1.696.600).
3. **¿Qué producto se vende más?** → **Cargador USB-C** (y Jean clásico), ambos con 10 ventas. Son los artículos de mayor rotación, ideales para stock constante.
4. **¿Cuál es el ticket promedio de venta?** → **$133.517** por transacción. Da una referencia para presupuestos y para detectar ventas atípicas.

## Conclusión

El sistema de automatización funciona: detecta cada reporte nuevo que se arrastra a `datos/`, lo consolida con el resto, lo limpia y regenera el Excel, los gráficos, el log y el resumen ejecutivo sin intervención manual. Con las 4 métricas el negocio puede ver de un vistazo qué categoría domina (Electrónica), quién vende más (Carlos), qué vende más (Cargador USB-C / Jean clásico) y cuál es el monto promedio por venta ($133.517). Esto convierte un montón de archivos sueltos en decisiones accionables en segundos.

## Reflexión final

**Si fuera el dueño de este negocio, ¿confiaría en un sistema automático como este para tomar decisiones?**

Sí, confiaría en él, con ciertas condiciones. Confiaría porque elimina el error humano de consolidar a mano, procesa los datos siempre con el mismo criterio (normaliza, limpia duplicados y nulos) y entrega métricas claras y comparables en cada ejecución. La información que da —categoría más rentable, vendedor y producto top, ticket promedio— es exactamente la que necesito para decidir dónde invertir stock, a quién premiar o qué campañas lanzar, y sin el sistema tendría que armar esos números manualmente cada vez.

Sin embargo, no lo usaría como única fuente de decisión. El sistema solo resume lo que ya está en los datos: si un dato de entrada llega mal (un precio mal digitado, una sucursal incompleta), la respuesta sale mal aunque el proceso sea correcto ("garbage in, garbage out"). Por eso lo vería como un asistente de confianza que me ahorra tiempo y me señala tendencias, pero la decisión final la tomaría yo, validando los resultados con la realidad de la tienda y desconfiando inmediatamente de cualquier cifra que se vea poco razonable. En resumen: sí, lo usaría —pero como herramienta de apoyo, no como un oráculo ciego.

## Historial del problema de re-ejecución

En la primera versión, el script usaba `glob.glob("*.csv")` y `glob.glob("*.xlsx")` para descubrir los archivos a leer. El problema: al ejecutar, el propio script generaba los consolidados en la raíz, y en la **segunda ejecución** esos archivos también eran leídos. Al aplicarles el renombrado quedaban columnas duplicadas y `pd.concat()` fallaba con:

```
pandas.errors.InvalidIndexError: Reindexing only valid with uniquely valued Index objects
```

La solución fue doble:

1. **Módulo `datos.py`**: define los archivos fuente de forma confiable. Ahora, en lugar de una lista fija, usa `obtener_archivos_datos()` con **glob acotado**: solo busca `sucursal_*.csv` y `sucursal_*.xlsx` dentro de la carpeta `datos/`. Como las salidas viven en `resultados/` y no empiezan con `sucursal_`, nunca vuelven a ser leídas.
2. **Carpetas separadas**: los datos viven en `datos/` y las salidas en `resultados/`, así nunca se mezclan.
3. **Guardar sin índice**: los Excel de salida se guardan con `index=False`, evitando la columna extra `Unnamed: 0` al volver a leerlos.
