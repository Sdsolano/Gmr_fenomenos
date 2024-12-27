import pandas as pd

# Leer los archivos CSV
precipitaciones = pd.read_csv('Promedio_precipitaciones.csv')
demanda = pd.read_csv('gmr_demanda (1).csv')

# Convertir precipitaciones de formato ancho a largo
meses = {
    'ENERO': 1, 'FEBRERO': 2, 'MARZO': 3, 'ABRIL': 4, 'MAYO': 5, 'JUNIO': 6,
    'JULIO': 7, 'AGOSTO': 8, 'SEPTIEMBRE': 9, 'OCTUBRE': 10, 'NOVIEMBRE': 11, 'DICIEMBRE': 12
}

# Convertir a formato largo y renombrar columnas
prec_largo = precipitaciones.melt(
    id_vars=['AÑO'],
    var_name='MES_NOMBRE',
    value_name='PRECIPITACION'
)

# Convertir nombres de meses a números
prec_largo['month'] = prec_largo['MES_NOMBRE'].map(meses)
prec_largo = prec_largo.rename(columns={'AÑO': 'year'})
prec_largo = prec_largo.drop('MES_NOMBRE', axis=1)

# Definir períodos de fenómenos
fenomenos = {
    2011: {'tipo': 'NIÑA', 'meses': [1,2,3,4,10,11,12]},
    2012: {'tipo': 'NIÑA', 'meses': [1,2,3,4]},
    2015: {'tipo': 'NIÑO', 'meses': [6,7,8,9,10,11,12]},
    2016: {'tipo': 'NIÑO', 'meses': [1,2,3]},
    2018: {'tipo': 'NIÑO', 'meses': [6,7,8,9,10,11,12]},
    2019: {'tipo': 'NIÑO', 'meses': [1,2,3]}
}

# Agregar columna de fenómenos
def asignar_fenomeno(row):
    year = row['year']
    month = row['month']
    if year in fenomenos and month in fenomenos[year]['meses']:
        return fenomenos[year]['tipo']
    return 'NORMAL'

# Combinar demanda con precipitaciones
df_final = demanda.merge(prec_largo, on=['year', 'month'])
df_final['FENOMENO'] = df_final.apply(asignar_fenomeno, axis=1)

# Guardar nuevo CSV
df_final.to_csv('demanda_precipitacion_fenomenos.csv', index=False)

# Imprimir primeras filas para verificar
print(df_final.head())