import pandas as pd

def analizar_logueos(ruta_excel):
    print("Leyendo el reporte de Orion...")
    # Leemos la solapa correspondiente a OCTUBRE que vimos en tu planilla
    df = pd.read_excel(ruta_excel, sheet_name='OCTUBRE')
    
    # Mostramos los primeros registros para validar columnas
    print(f"Total de filas leídas: {len(df)}")
    
    # Aquí puedes agregar la lógica para buscar faltas 'F' o calcular horas
    # Por ejemplo, filtrar filas donde aparezca la 'F' de ausencias
    return df

if __name__ == "__main__":
    # Reemplaza con el nombre de tu archivo de prueba
    # archivo = "Logueos Naturgy BAN CAU SEPT-OCT.xlsx"
    # analizar_logueos(archivo)
    pass
