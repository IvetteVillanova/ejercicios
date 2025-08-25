
"""
1 Carga inicial y exploración: * Cargar el archivo alumnos_Pr.csv 
y mostrar las primeras 5 filas para conocer su estructura.

"""

# Cargar el archivo CSV
import pandas as pd

archivo = "Z:/trabajo/alumnos_Pr.csv"

df = pd.read_csv(archivo)

# Mostrar todos registros
print(df)

# Mostrar las primeras 5 filas
print(df.head())


"""
02.	Cantidad total y por curso:
	* Mostrar cuántos alumnos hay en total y cuántos pertenecen a cada curso.
	* Indicar también el porcentaje de alumnos que representa cada curso sobre el total.
"""

# Cantidad total de alumnos
total_alumnos = len(df)

# Cantidad por curso
alumnos_por_curso = df['Curso'].value_counts()

# Porcentaje por curso
porcentaje_por_curso = (df['Curso'].value_counts(normalize=True) * 100).round(2)

# Mostrar resultados
print("Total de alumnos:", total_alumnos)
print("\nCantidad de alumnos por curso:")
print(alumnos_por_curso)
print("\nPorcentaje de alumnos por curso:")
print(porcentaje_por_curso)


"""
03.	Listado de alumnos ordenados:
	* Mostrar solo la columna con el nombre de los alumnos, pero ordenada alfabéticamente.
	* Además, indicar cuántos nombres comienzan con cada letra del abecedario y mostrar los
		3 primeros y 3 últimos nombres en orden.
"""

# Listado de alumnos ordenados alfabéticamente
nombres_ordenados = df['Nombre'].sort_values()

# Cantidad de nombres que comienzan con cada letra
cantidad_por_letra = df['Nombre'].str[0].value_counts().sort_index()

# Primeros 3 y últimos 3 nombres
primeros_tres = nombres_ordenados.head(3)
ultimos_tres = nombres_ordenados.tail(3)

# Mostrar resultados
print("Nombres ordenados alfabéticamente:")
print(nombres_ordenados)

print("\nCantidad de nombres por letra inicial:")
print(cantidad_por_letra)

print("\nPrimeros 3 nombres:")
print(primeros_tres)

print("\nÚltimos 3 nombres:")
print(ultimos_tres)


"""
04.	Promedios por curso:
	* Calcular, para cada curso, el promedio de PromedioMat y el promedio de PromedioLen.
	* Indicar cuál curso tiene mejor promedio en Matemática y cuál en Lenguaje.
"""

# Calcular promedios individuales por alumno
df['PromedioMat'] = df[['Matematica1', 'Matematica2']].mean(axis=1)
df['PromedioLen'] = df[['Lenguaje1', 'Lenguaje2']].mean(axis=1)

# Calcular promedios por curso
promedios_por_curso = df.groupby('Curso')[['PromedioMat', 'PromedioLen']].mean().round(2)

# Curso con mejor promedio en Matemática
mejor_mat = promedios_por_curso['PromedioMat'].idxmax()

# Curso con mejor promedio en Lenguaje
mejor_len = promedios_por_curso['PromedioLen'].idxmax()

# Mostrar resultados
print("Promedios por curso:")
print(promedios_por_curso)
print(f"\nCurso con mejor promedio en Matemática: {mejor_mat}")
print(f"Curso con mejor promedio en Lenguaje: {mejor_len}")


"""
05.	Promedio por ramos:
	* Crear las columnas PromedioMat y PromedioLen calculando el promedio de las 
		dos notas de Matemática y de las dos de Lenguaje por alumno.
"""

# Crear columnas con promedios por ramo
df['PromedioMat'] = df[['Matematica1', 'Matematica2']].mean(axis=1)
df['PromedioLen'] = df[['Lenguaje1', 'Lenguaje2']].mean(axis=1)

# Imprimir muestra de resultados
print("\nPromedios por ramo:")
print(df[['Nombre', 'Curso', 'PromedioMat', 'PromedioLen']].head().to_string(index=False))


"""
06.	Promedio general:
	* Crear la columna PromedioGen calculando el promedio entre PromedioMat y PromedioLen.
"""

# Crear columna de promedio general
df['PromedioGen'] = df[['PromedioMat', 'PromedioLen']].mean(axis=1)

# Imprimir muestra de resultados
print("\nPromedio general por alumno:")
print(df[['Nombre', 'Curso', 'PromedioMat', 'PromedioLen', 'PromedioGen']].head().to_string(index=False))

"""
07.	Aprobación en Matemática y Lenguaje:
	* Mostrar cuántos alumnos aprobaron y reprobaron Matemática y cuántos aprobaron y 
		reprobaron Lenguaje, todo en una misma tabla resumen.
"""

# Definir umbral de aprobación
umbral_aprobacion = 4.0

# Clasificar aprobación en Matemática y Lenguaje
df['EstadoMat'] = df['PromedioMat'].apply(lambda x: 'Aprobado' if x >= umbral_aprobacion else 'Reprobado')
df['EstadoLen'] = df['PromedioLen'].apply(lambda x: 'Aprobado' if x >= umbral_aprobacion else 'Reprobado')

# Crear tabla resumen
resumen_aprobacion = pd.DataFrame({
    'Matemática': df['EstadoMat'].value_counts(),
    'Lenguaje': df['EstadoLen'].value_counts()
})

# Imprimir tabla resumen de forma limpia
print("\nResumen de aprobación y reprobación por ramo:")
print(resumen_aprobacion.to_string())


"""
08.	Reprobados Lenguaje (detalle):
	* Mostrar nombre y curso de los alumnos que reprobaron Lenguaje (PromedioLen < 4.0).
"""

# Filtrar alumnos reprobados en Lenguaje
reprobados_len = df[df['PromedioLen'] < 4.0][['Nombre', 'Curso']]

# Imprimir resultados de forma limpia
print("\nAlumnos que reprobaron Lenguaje:")
print(reprobados_len.to_string(index=False))

"""
08.	Reprobados Lenguaje (detalle):
	* Mostrar nombre y curso de los alumnos que reprobaron Lenguaje (PromedioLen < 4.0).
"""

# Filtrar alumnos reprobados en Lenguaje
reprobados_len = df[df['PromedioLen'] < 4.0][['Nombre', 'Curso']]

# Imprimir resultados de forma limpia
print("\nAlumnos que reprobaron Lenguaje:")
print(reprobados_len.to_string(index=False))


"""
09. Alumno destacado en Matemática 1 (por curso)
	* Encontrar, para cada curso, el estudiante que obtuvo la nota más alta en la columna Matematica1.
	* Además, mostrar sus promedios en Matemática (PromedioMat) y en general (PromedioGen) para evaluar 
		si su desempeño en Matemática es consistente con el global.
"""

# Localizar el índice del alumno con mayor nota en Matematica1 por curso
destacados_mat1 = df.loc[
    df.groupby('Curso')['Matematica1'].idxmax(),
    ['Nombre', 'Curso', 'Matematica1', 'PromedioMat', 'PromedioGen']
]

# Imprimir resultados de forma limpia
print("\nAlumnos destacados en Matemática 1 por curso:")
print(destacados_mat1.to_string(index=False))


"""
10. Mejores promedios generales (Top 3 por curso)
	* Ordenar los registros por Curso y, dentro de cada curso, por PromedioGen en orden descendente.
	* Presentar únicamente los tres primeros puestos de cada curso, indicando nombre, promedios y curso.
"""

# Ordenar por curso y promedio general descendente
top3_por_curso = df.sort_values(['Curso', 'PromedioGen'], ascending=[True, False])

# Seleccionar los 3 primeros de cada curso
top3_por_curso = top3_por_curso.groupby('Curso').head(3)[
    ['Nombre', 'Curso', 'PromedioMat', 'PromedioLen', 'PromedioGen']
]

# Imprimir tabla de forma limpia
print("\nTop 3 promedios generales por curso:")
print(top3_por_curso.to_string(index=False))


"""
11. Estados de rendimiento académico
	* Crear las siguientes columnas:
		- EstadoMat: “Aprobado” si PromedioMat es mayor o igual a 4.0, “Reprobado” si es menor.
		- EstadoLen: “Aprobado” si PromedioLen es mayor o igual a 4.0, “Reprobado” si es menor.
		- EstadoGen: “Aprobado” si PromedioGen es mayor o igual a 4.0, “Reprobado” si es menor.
"""

# Definir umbral de aprobación
umbral = 4.0

# Crear columnas de estado
df['EstadoMat'] = df['PromedioMat'].apply(lambda x: 'Aprobado' if x >= umbral else 'Reprobado')
df['EstadoLen'] = df['PromedioLen'].apply(lambda x: 'Aprobado' if x >= umbral else 'Reprobado')
df['EstadoGen'] = df['PromedioGen'].apply(lambda x: 'Aprobado' if x >= umbral else 'Reprobado')

# Imprimir una muestra de las columnas creadas
print("\nEstados académicos por alumno:")
print(df[['Nombre', 'Curso', 'PromedioMat', 'EstadoMat', 'PromedioLen', 'EstadoLen', 'PromedioGen', 'EstadoGen']].to_string(index=False))


"""
12. Ranking de percentiles por curso
	* Calcular para cada alumno el percentil que le corresponde dentro de su curso según PromedioGen.
	* Mostrar los resultados con nombre, curso, promedio general y percentil, 
		ordenados de mayor a menor percentil en cada curso.
"""

# Percentil por curso (0-100). method='average' asigna promedio en empates.
df['PercentilCurso'] = (
    df.groupby('Curso')['PromedioGen']
      .rank(method='average', pct=True) * 100
)

# Ordenar por curso y percentil descendente (desempatar por PromedioGen desc)
ranking_percentiles = df.sort_values(
    ['Curso', 'PercentilCurso', 'PromedioGen'],
    ascending=[True, False, False]
)[['Nombre', 'Curso', 'PromedioGen', 'PercentilCurso']]

# Impresión limpia (redondeo de percentil)
tmp_print = ranking_percentiles.copy()
tmp_print['PercentilCurso'] = tmp_print['PercentilCurso'].round(2)

print("\nRanking de percentiles por curso (según PromedioGen):")
print(tmp_print.to_string(index=False))


"""
13. Análisis comparativo por género
	* Si existe la columna Genero, calcular el promedio general agrupando por género y curso.
	* Si no existe la columna, generar un mensaje que indique que la comparación no es posible.
"""

# (Opcional) Asegurar existencia de PromedioGen si este bloque corre aislado
if 'PromedioMat' not in df.columns:
    df['PromedioMat'] = df[['Matematica1', 'Matematica2']].mean(axis=1)
if 'PromedioLen' not in df.columns:
    df['PromedioLen'] = df[['Lenguaje1', 'Lenguaje2']].mean(axis=1)
if 'PromedioGen' not in df.columns:
    df['PromedioGen'] = df[['PromedioMat', 'PromedioLen']].mean(axis=1)

if 'Genero' in df.columns:
    # Promedio general por género y curso
    comp_genero = (df.groupby(['Genero', 'Curso'])['PromedioGen']
                     .mean()
                     .round(2)
                     .unstack('Curso'))  # columnas por curso para lectura Reordena las columnas

    print("\nPromedio general (PromedioGen) por Género y Curso:")
    print(comp_genero.to_string())
else:
    print("\nNo es posible realizar la comparación por género: la columna 'Genero' no existe en el DataFrame.")


"""
14. Exportación de resultados finales
	* Guardar el DataFrame final en un archivo llamado alumnos_resultados.csv.
	* El archivo debe estar ordenado primero por Curso y luego por PromedioGen de forma descendente.
	* Debe contener todas las columnas calculadas: PromedioMat, PromedioLen, PromedioGen, EstadoMat, EstadoLen, EstadoGen, PercenCurso.
"""

# (Opcional) Asegurar existencia de columnas calculadas si este bloque se ejecuta aislado
if 'PromedioMat' not in df.columns:
    df['PromedioMat'] = df[['Matematica1', 'Matematica2']].mean(axis=1)
if 'PromedioLen' not in df.columns:
    df['PromedioLen'] = df[['Lenguaje1', 'Lenguaje2']].mean(axis=1)
if 'PromedioGen' not in df.columns:
    df['PromedioGen'] = df[['PromedioMat', 'PromedioLen']].mean(axis=1)

if 'EstadoMat' not in df.columns:
    df['EstadoMat'] = df['PromedioMat'].apply(lambda x: 'Aprobado' if x >= 4.0 else 'Reprobado')
if 'EstadoLen' not in df.columns:
    df['EstadoLen'] = df['PromedioLen'].apply(lambda x: 'Aprobado' if x >= 4.0 else 'Reprobado')
if 'EstadoGen' not in df.columns:
    df['EstadoGen'] = df['PromedioGen'].apply(lambda x: 'Aprobado' if x >= 4.0 else 'Reprobado')
if 'PercentilCurso' not in df.columns:
    df['PercentilCurso'] = (
        df.groupby('Curso')['PromedioGen']
          .rank(method='average', pct=True) * 100
    )

# Ordenar por Curso y PromedioGen descendente
df_final = df.sort_values(['Curso', 'PromedioGen'], ascending=[True, False])

# Exportar a CSV
df_final.to_csv('alumnos_resultados.csv', index=False)

