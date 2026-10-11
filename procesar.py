import pandas as pd

def procesar_reporte_asistencias(ruta_archivo):
    print("Iniciando procesamiento del reporte de Orion...")
    
    # 1. Leemos la solapa 'OCTUBRE' (puedes cambiarla por 'Control Tiempos' si prefieres)
    df = pd.read_excel(ruta_archivo, sheet_name='OCTUBRE')
    
    # 2. Mostramos las primeras filas en la terminal para verificar que leyó bien
    print(f"Total de filas leídas: {len(df)}")
    
    # 3. Aquí puedes agregar la lógica para filtrar o limpiar datos
    # Por ejemplo, si quieres ver las columnas disponibles:
    print("Columnas encontradas en el reporte:", df.columns)
    
    return df

if __name__ == "__main__":
    # Cambia 'tu_archivo.xlsx' por el nombre real del archivo que descargues de Orion
    # archivo_prueba = "tu_archivo.xlsx"
    # procesar_reporte_asistencias(archivo_prueba)
    pass