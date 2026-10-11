import pandas as pd

def procesar_reporte_asistencias(ruta_archivo):
    print("Iniciando procesamiento del reporte...")
    
    # Leemos la solapa 'OCTUBRE' de tu planilla de control
    df = pd.read_excel(ruta_archivo, sheet_name='OCTUBRE')
    
    # Mostramos las primeras filas para verificar columnas clave (Legajo, Asesor, Turno)
    print("Datos cargados correctamente.")
    
    # Ejemplo de filtrado básico por equipos o turnos
    # Aquí puedes estructurar la lógica para calcular totales y desvíos
    return df

if __name__ == "__main__":
    # Coloca aquí la ruta de tu archivo de prueba local cuando lo descargues
    # archivo_prueba = "Logueos_Naturgy_Test.xlsx"
    # procesar_reporte_asistencias(archivo_prueba)
    pass
