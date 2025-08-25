# -*- coding: utf-8 -*-
"""
Carga inicial y exploración
    CArgar el archivo alumnos_pr
"""

import pandas as pd
import numpy as np

archivo = "c:/spider/alumnos_Pr.csv"

df = pd.read_csv(archivo)

print(df)

"""
02. CAntidad total y por curso:
    *Mostrar cuantos alumnos hay en total y cuantos por curso
    *Indicar tambien el porcentaje de alumnos que hay por curso
    
"""

total_alumnos = len(df)
print(total_alumnos)

#2. Otra manera de rralizarlo

print("\nCantidad de alumnos con el nombre:",df.shape[0])
print("Cantidad de columnas:",df.shape[1])

alumnos_curso = df["Curso"].value_counts()

porcentaje_curso = (alumnos_curso/total_alumnos)* 100


"""3. Listado de alumnos ordenados
"""
nombres_ordenados = df['Nombre'].sort_values().reset_index(drop=True)



"""Promedios por ramo y general(solo pandas)

"""

df['Promedio_Lenguaje'] = df[['Lenguaje1','Lenguaje2']].mean(axis=1).round(2)
df['Promedio_Matematicas'] = df[['Matematica1','Matematica2']].mean(axis=1).round(2)


df['Promedio_General'] = df[['Promedio_Lenguaje','Promedio_Matematicas']].mean(axis=1).round(2)



#===================================
# 3) Total y por curso
#===================================

total_alum = len(df)
resumen_curso =(
    df['Curso']
    .value_counts()
    .sort_index()
    .rename_axis('Curso')
    .to_frame('Cantidad')
    .assign(Porcentaje=lambda t: (t['Cantidad'] / total_alum*100).round(2))
    .reset_index()
    )



#===========================================
#4. Listado ordenado y conteo por incial
#===========================================
#tomaremos la variable de arriba nombres_ordenados

conteo_iniciales = (
    nombres_ordenados.str[0].str.upper()
    .value_counts()
    .sort_index()
    .rename_axis('Inicial')
    .to_frame('Cantidad')
    .reset_index()
        
   )


primeros3 = nombres_ordenados.head(3).tolist()
ultimos3 = nombres_ordenados.tail(3).tolist()

#==========================
#5 Promedios por curso y mejores cursos
#=========================================


promedios_curso =(
    df.groupby('Curso', as_index=True)
    .agg(PromedioMat_prom=('Promedio_Matematicas','mean'),
                          PromedioLeng_prom=('Promedio_Lenguaje','mean'))
         .round(2)
             
    )

mejor_mat_curso = promedios_curso['PromedioMat_prom'].idxmax()
mejor_leng_curso = promedios_curso['PromedioLeng_prom'].idxmax()

print(promedios_curso)
print(mejor_leng_curso)
print(mejor_mat_curso)

#=====================================
#6 Aprobacion y reprobacion por ramo
#======================================


df['EstadoMat'] = df['Promedio_Matematicas'].ge(4.0).map({True:'Aprobado', False: 'Reprobado'})
df['EstadoLeng'] =df['Promedio_Lenguaje'].ge(4.0).map({True:'Aprobado', False: 'Reprobado'})


tabla_aprob = (
    pd.DataFrame({
        'Matematica': df['EstadoMat'].value_counts().reindex(['Aprobado','Reprobado']).fillna(0).astype(int),
        'Lenguaje' : df['EstadoLeng'].value_counts().reindex(['Aprobado','Reprobado']).fillna(0).astype(int)
        
        
     })
    .rename_axis('Estado')
    .reset_index()
    
)