import pandas as pd

def process_precipitation_data(file_path, output_path):
    # Leer el CSV
    df = pd.read_csv(file_path)
    
    # Filtrar datos desde 2011
    df = df[df['AÑO'] >= 2011]
    
    # Lista de meses para promediar
    meses = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 
             'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE']
    
    # Agrupar por año y calcular promedio de cada mes
    promedios = df.groupby('AÑO')[meses].mean().round(2)
    
    # Guardar en nuevo CSV
    promedios.to_csv(output_path)
    
    return promedios

# Uso de la función
promedios = process_precipitation_data('Precipitaciones_Totales_Mensuales_20241220.csv', 'Promedio_precipitaciones.csv')
print(promedios)