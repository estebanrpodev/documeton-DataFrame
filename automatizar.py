# ============================================
# AUTOMATIZACIÓN - Bot de Ventas
# Vigila la carpeta datos/ y cuando detecta un archivo nuevo,
# procesa todo automáticamente: lee, consolida, normaliza, limpia,
# guarda el Excel, genera los gráficos y registra el proceso en un log
# ============================================
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from datos import cargar_datos

CARPETA_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")
CARPETA_RESULTADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados")


def normalizar(df):
    """
    Normaliza las columnas del archivo de Bogotá (nombres distintos)
    al formato estándar del resto de sucursales.
    """
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
    return df


def limpiar(df):
    """Elimina duplicados y rellena los nulos con valores que tienen sentido."""
    df = df.drop_duplicates()
    df['metodo_pago'] = df['metodo_pago'].fillna('Desconocido')
    df['vendedor'] = df['vendedor'].fillna('Desconocido')
    mediana_por_producto = df.groupby('producto')['precio_unitario'].transform('median')
    df['precio_unitario'] = df['precio_unitario'].fillna(mediana_por_producto)
    return df


def procesar_todo(archivo_nuevo):
    """
    Lee todos los reportes de sucursales, los normaliza, consolida y limpia,
    guarda el Excel consolidado, genera los dos gráficos y registra el proceso.
    """
    lista_informes = [normalizar(df) for df in cargar_datos()]
    df_consolidado = pd.concat(lista_informes, ignore_index=True)
    df_consolidado = limpiar(df_consolidado)

    # Excel consolidado
    df_consolidado.to_excel(os.path.join(CARPETA_RESULTADOS, "consolidado_limpio.xlsx"), index=False)

    # Gráfico 1: ventas por categoría (barras)
    ventas_categoria = df_consolidado.groupby('categoria')['precio_unitario'].sum()
    ventas_categoria.plot(kind='bar', title='Ventas por Categoría')
    plt.ticklabel_format(style='plain', axis='y')
    plt.ylabel('Ventas totales ($)')
    plt.xlabel('Categoría')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_RESULTADOS, "grafico_categoria.png"))
    plt.close()

    # Gráfico 2: participación por vendedor (torta)
    ventas_vendedor = df_consolidado.groupby('vendedor')['precio_unitario'].sum()
    ventas_vendedor.plot(kind='pie', autopct='%1.1f%%', title='Participación de Ventas por Vendedor')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_RESULTADOS, "grafico_vendedor.png"))
    plt.close()

    # Log del proceso
    with open(os.path.join(CARPETA_RESULTADOS, "log_automatizacion.txt"), "a", encoding="utf-8") as f:
        f.write(f"Proceso ejecutado: {pd.Timestamp.now()}\n")
        f.write(f"Archivo detectado: {archivo_nuevo}\n")
        f.write(f"Total de registros procesados: {len(df_consolidado)}\n")
        f.write("---\n")

    # Banner visual con resumen en pantalla
    total_ventas = df_consolidado['precio_unitario'].sum()
    print("=" * 40)
    print("  NUEVO REPORTE PROCESADO EXITOSAMENTE")
    print(f"  Total ventas acumuladas: ${total_ventas:,.0f}")
    print("=" * 40)

    # Resumen ejecutivo en archivo de texto
    categoria_top = df_consolidado.groupby('categoria')['precio_unitario'].sum().idxmax()
    vendedor_top = df_consolidado.groupby('vendedor')['precio_unitario'].sum().idxmax()

    # Metricas nuevas: producto mas vendido (value_counts) y promedio por transaccion (mean)
    productos_mas_vendidos = df_consolidado['producto'].value_counts()
    producto_top = productos_mas_vendidos.idxmax()
    producto_top_ventas = productos_mas_vendidos.max()
    promedio_por_transaccion = df_consolidado['precio_unitario'].mean()

    with open(os.path.join(CARPETA_RESULTADOS, "resumen_ejecutivo.txt"), "w", encoding="utf-8") as f:
        f.write("RESUMEN EJECUTIVO - Bot de Ventas\n")
        f.write(f"Fecha: {pd.Timestamp.now()}\n\n")
        f.write(f"Categoria con mejor desempeño: {categoria_top}\n")
        f.write(f"Vendedor con mas ventas: {vendedor_top}\n")
        f.write(f"Producto mas vendido: {producto_top} ({producto_top_ventas} ventas)\n")
        f.write(f"Promedio de venta por transacción: ${promedio_por_transaccion:,.0f}\n")
        f.write(f"Total de ventas acumuladas: ${total_ventas:,.0f}\n")

    print("Proceso completado - archivos actualizados en resultados/")


# ---------- LOOP DE VIGILANCIA ----------
if __name__ == "__main__":
    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)
    archivos_vistos = set(os.listdir(CARPETA_DATOS))

    print("Monitoreando carpeta 'datos/'... (Ctrl+C para detener)")
    while True:
        archivos_actuales = set(os.listdir(CARPETA_DATOS))
        archivos_nuevos = archivos_actuales - archivos_vistos

        if archivos_nuevos:
            print(f"Nuevo archivo detectado: {archivos_nuevos}")
            procesar_todo(archivos_nuevos)
            archivos_vistos = archivos_actuales

        time.sleep(5)
