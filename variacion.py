import pandas as pd
import numpy as np

# Leer datos
df = pd.read_csv('demanda_precipitacion_fenomenos.csv')

# Calcular tendencia anual para normalizar el crecimiento
df['year_avg'] = df.groupby('year')['total'].transform('mean')
df['demanda_normalizada'] = df['total'] / df['year_avg']

# Calcular promedios mensuales por fenómeno
def calcular_variacion_mensual(data):
    normal = data[data['FENOMENO'] == 'NORMAL'].groupby('month')['demanda_normalizada'].mean()
    nino = data[data['FENOMENO'] == 'NIÑO'].groupby('month')['demanda_normalizada'].mean()
    nina = data[data['FENOMENO'] == 'NIÑA'].groupby('month')['demanda_normalizada'].mean()
    
    var_nino = ((nino / normal) - 1) * 100
    var_nina = ((nina / normal) - 1) * 100
    
    return var_nino, var_nina

var_nino, var_nina = calcular_variacion_mensual(df)

# Crear DataFrame de resultados
resultado = pd.DataFrame({
    'Mes': range(1, 13),
    'Variacion_Nino_%': [var_nino.get(i, np.nan) for i in range(1, 13)],
    'Variacion_Nina_%': [var_nina.get(i, np.nan) for i in range(1, 13)]
})

# Calcular promedios excluyendo NaN
promedio_nino = np.nanmean(var_nino)
promedio_nina = np.nanmean(var_nina)

print("\nMuestra de datos normalizados:")
print(df[['year', 'month', 'FENOMENO', 'demanda_normalizada']].head(10))

print("\nVariaciones por mes:")
print(resultado.round(2))
print(f"\nPromedio general Niño: {promedio_nino:.2f}%")
print(f"Promedio general Niña: {promedio_nina:.2f}%")

# Análisis estadístico
for fenomeno in ['NORMAL', 'NIÑO', 'NIÑA']:
    data = df[df['FENOMENO'] == fenomeno]
    print(f"\nEstadísticas para {fenomeno}:")
    print(f"Número de meses: {len(data)}")
    print(f"Demanda promedio: {data['total'].mean():,.0f}")

    # los resultados de este codigo son:
    
    # Variaciones por mes:
    #     Mes  Variacion_Nino_%  Variacion_Nina_% 
    # 0     1              2.63              0.59
    # 1     2              4.04              0.96
    # 2     3              0.58              0.56
    # 3     4               NaN             -3.06
    # 4     5               NaN               NaN
    # 5     6              0.71               NaN
    # 6     7              0.92               NaN
    # 7     8             -0.28               NaN
    # 8     9              1.30               NaN
    # 9    10              0.63             -1.53
    # 10   11             -0.40              0.01
    # 11   12              0.25             -1.30

    # Promedio general Niño: 1.04%
    # Promedio general Niña: -0.54%

    # Estadísticas para NORMAL:
    # Número de meses: 77
    # Demanda promedio: 4,284,473,039

    # Estadísticas para NIÑO:
    # Número de meses: 20
    # Demanda promedio: 4,753,942,167

    # Estadísticas para NIÑA:
    # Número de meses: 11
    # Demanda promedio: 3,174,750,852

    # Por tanto los factores serán:

    # Para el fenómeno del Niño: 1.0104 
    # Para el fenómeno de la Niña: 0.9946

