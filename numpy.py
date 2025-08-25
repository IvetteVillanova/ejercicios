# ==========================================
# Análisis con NumPy (Spyder)
# ==========================================
import numpy as np
import pandas as pd

# ------------------------------------------
# 01) Carga inicial y exploración
# ------------------------------------------
df = pd.read_csv("alumnos_Pr.csv")

print("\n[01] Primeras 5 filas (estructura del archivo):")
print(df.head().to_string(index=False))

# Crear vistas NumPy (para operar con NumPy)
nombres = df['Nombre'].to_numpy()
cursos  = df['Curso'].to_numpy()
mat1    = df['Matematica1'].to_numpy(dtype=float)
mat2    = df['Matematica2'].to_numpy(dtype=float)
len1    = df['Lenguaje1'].to_numpy(dtype=float)
len2    = df['Lenguaje2'].to_numpy(dtype=float)
genero  = df['Genero'].to_numpy() if 'Genero' in df.columns else None

# ------------------------------------------
# 05) Promedio por ramos (usando NumPy)
# ------------------------------------------
prom_mat = (mat1 + mat2) / 2.0
prom_len = (len1 + len2) / 2.0

# Añadir al DataFrame
df['PromedioMat'] = prom_mat
df['PromedioLen'] = prom_len

print("\n[05] Promedios por ramo (muestra):")
print(df[['Nombre','Curso','PromedioMat','PromedioLen']].head().to_string(index=False))

# ------------------------------------------
# 06) Promedio general (usando NumPy)
# ------------------------------------------
prom_gen = (prom_mat + prom_len) / 2.0
df['PromedioGen'] = prom_gen

print("\n[06] Promedio general (muestra):")
print(df[['Nombre','Curso','PromedioMat','PromedioLen','PromedioGen']].head().to_string(index=False))

# ------------------------------------------
# 02) Cantidad total y por curso (NumPy)
# ------------------------------------------
total_alumnos = nombres.size
cursos_unicos, counts_por_curso = np.unique(cursos, return_counts=True)
porcentajes = np.round(counts_por_curso / total_alumnos * 100, 2)

print("\n[02] Cantidad total y por curso:")
print(f"Total de alumnos: {total_alumnos}")
for c, n, p in zip(cursos_unicos, counts_por_curso, porcentajes):
    print(f"  Curso {c}: {n} alumnos ({p}%)")

# ------------------------------------------
# 03) Listado de alumnos ordenados + conteo por letra (NumPy)
# ------------------------------------------
# Orden alfabético de nombres
orden_nombres = np.argsort(nombres, kind='mergesort')
nombres_ordenados = nombres[orden_nombres]

# Conteo por inicial
iniciales = np.array([nm[0].upper() for nm in nombres])
letras, cnt_letras = np.unique(iniciales, return_counts=True)

print("\n[03] Nombres ordenados (primeros 10 como muestra):")
print("\n".join(nombres_ordenados[:10]))
print("\n[03] Cantidad de nombres por letra inicial:")
for L, cnt in zip(letras, cnt_letras):
    print(f"  {L}: {cnt}")
print("\n[03] Top 3 primeros y 3 últimos:")
print("  Primeros 3:", ", ".join(nombres_ordenados[:3]))
print("  Últimos 3:", ", ".join(nombres_ordenados[-3:]))

# ------------------------------------------
# 04) Promedios por curso y mejor curso en Mat/Len (NumPy)
# ------------------------------------------
promedio_mat_por_curso = {}
promedio_len_por_curso = {}

for c in cursos_unicos:
    mask = (cursos == c)
    promedio_mat_por_curso[c] = np.round(np.mean(prom_mat[mask]), 2)
    promedio_len_por_curso[c] = np.round(np.mean(prom_len[mask]), 2)

mejor_curso_mat = max(promedio_mat_por_curso, key=promedio_mat_por_curso.get)
mejor_curso_len = max(promedio_len_por_curso, key=promedio_len_por_curso.get)

print("\n[04] Promedios por curso:")
for c in cursos_unicos:
    print(f"  {c} -> PromedioMat: {promedio_mat_por_curso[c]} | PromedioLen: {promedio_len_por_curso[c]}")
print(f"\n  Curso con mejor promedio en Matemática: {mejor_curso_mat}")
print(f"  Curso con mejor promedio en Lenguaje : {mejor_curso_len}")

# ------------------------------------------
# 07) Aprobación en Mat y Len (tabla resumen con NumPy)
# ------------------------------------------
umbral = 4.0
estado_mat = np.where(prom_mat >= umbral, 'Aprobado', 'Reprobado')
estado_len = np.where(prom_len >= umbral, 'Aprobado', 'Reprobado')
df['EstadoMat'] = estado_mat
df['EstadoLen'] = estado_len

# Conteos por estado (garantizar ambas categorías)
def conteo_estados(estados):
    cats = np.array(['Aprobado','Reprobado'])
    u, cnt = np.unique(estados, return_counts=True)
    # map a dict y asegurar todas las categorías
    base = {k:0 for k in cats}
    base.update({k:v for k,v in zip(u,cnt)})
    return base

res_mat = conteo_estados(estado_mat)
res_len = conteo_estados(estado_len)
tabla_resumen = pd.DataFrame({'Matemática': res_mat, 'Lenguaje': res_len})
print("\n[07] Resumen Aprobación/Reprobación:")
print(tabla_resumen.to_string())

# ------------------------------------------
# 08) Reprobados Lenguaje (detalle)
# ------------------------------------------
mask_reprob_len = prom_len < 4.0
det_reprob_len = pd.DataFrame({'Nombre': nombres[mask_reprob_len],
                               'Curso' : cursos[mask_reprob_len]})
print("\n[08] Alumnos que reprobaron Lenguaje:")
print(det_reprob_len.to_string(index=False))

# ------------------------------------------
# 09) Alumno destacado en Matemática 1 (por curso)
# ------------------------------------------
rows_destacados = []
for c in cursos_unicos:
    mask = (cursos == c)
    idx_local = np.argmax(mat1[mask])         # posición dentro del grupo
    idx_global = np.flatnonzero(mask)[idx_local]  # índice real en df
    rows_destacados.append({
        'Nombre'      : nombres[idx_global],
        'Curso'       : c,
        'Matematica1' : mat1[idx_global],
        'PromedioMat' : prom_mat[idx_global],
        'PromedioGen' : prom_gen[idx_global]
    })
destacados_df = pd.DataFrame(rows_destacados)
print("\n[09] Destacados en Matemática 1 por curso:")
print(destacados_df.to_string(index=False))

# ------------------------------------------
# 10) Top 3 por curso según PromedioGen (NumPy)
# ------------------------------------------
top_rows = []
for c in cursos_unicos:
    mask = (cursos == c)
    # argsort ascendente; para descendente usamos signo negativo
    orden = np.argsort(-prom_gen[mask], kind='mergesort')
    idxs_globales = np.flatnonzero(mask)[orden][:3]
    for i in idxs_globales:
        top_rows.append({
            'Nombre': nombres[i],
            'Curso': cursos[i],
            'PromedioMat': prom_mat[i],
            'PromedioLen': prom_len[i],
            'PromedioGen': prom_gen[i]
        })
top3_df = pd.DataFrame(top_rows)
print("\n[10] Top 3 PromedioGen por curso:")
print(top3_df.to_string(index=False))

# ------------------------------------------
# 11) Estados de rendimiento académico (incluye EstadoGen)
# ------------------------------------------
estado_gen = np.where(prom_gen >= umbral, 'Aprobado', 'Reprobado')
df['EstadoGen'] = estado_gen

# Resumen por curso y estado usando NumPy
def resumen_por_curso_estado(cursos_arr, estado_arr, prefijo):
    filas = []
    for c in cursos_unicos:
        mask = (cursos_arr == c)
        est_c = estado_arr[mask]
        base = conteo_estados(est_c)
        filas.append({'Curso': c,
                      f'{prefijo}_Aprobado': base['Aprobado'],
                      f'{prefijo}_Reprobado': base['Reprobado']})
    return pd.DataFrame(filas).set_index('Curso')

res_mat_df = resumen_por_curso_estado(cursos, estado_mat, 'Mat')
res_len_df = resumen_por_curso_estado(cursos, estado_len, 'Len')
res_gen_df = resumen_por_curso_estado(cursos, estado_gen, 'Gen')

resumen_curso = pd.concat([res_mat_df, res_len_df, res_gen_df], axis=1)
print("\n[11] Resumen por curso (Aprobado/Reprobado en Mat/Len/Gen):")
print(resumen_curso.to_string())

# ------------------------------------------
# 12) Ranking de percentiles por curso (NumPy con empates promedio)
# ------------------------------------------
percentil_curso = np.empty_like(prom_gen, dtype=float)

for c in cursos_unicos:
    mask = (cursos == c)
    s = prom_gen[mask]
    n = s.size

    # Ranks con empates al promedio:
    # 1) Orden ascendente
    order = np.argsort(s, kind='mergesort')
    ranks = np.empty(n, dtype=float)
    # 2) Para cada valor único, asignar el promedio del rango (min..max)
    vals, starts, counts = np.unique(s[order], return_index=True, return_counts=True)
    for v, st, ct in zip(vals, starts, counts):
        # rangos naturales 1..n
        min_r = st + 1
        max_r = st + ct
        avg_r = (min_r + max_r) / 2.0
        ranks[st:st+ct] = avg_r
    # 3) Volver a la posición original
    inv_order = np.empty(n, dtype=int)
    inv_order[order] = np.arange(n)
    ranks_original = ranks[inv_order]
    # 4) Percentil 0-100
    percentiles = ranks_original / n * 100.0
    percentil_curso[mask] = percentiles

df['PercentilCurso'] = percentil_curso

ranking_np = pd.DataFrame({
    'Nombre': nombres,
    'Curso': cursos,
    'PromedioGen': prom_gen,
    'PercentilCurso': percentil_curso
})

# Ordenar: por Curso asc, luego Percentil desc, luego PromedioGen desc (desempate)
ranking_np = ranking_np.sort_values(['Curso','PercentilCurso','PromedioGen'],
                                    ascending=[True, False, False])

print("\n[12] Ranking de percentiles por curso (NumPy):")
tmp = ranking_np.copy()
tmp['PercentilCurso'] = np.round(tmp['PercentilCurso'], 2)
print(tmp.to_string(index=False))

# ------------------------------------------
# 13) Análisis comparativo por género (NumPy)
# ------------------------------------------
if genero is not None:
    gen_unicos = np.unique(genero)
    filas = []
    for g in gen_unicos:
        for c in cursos_unicos:
            mask = (genero == g) & (cursos == c)
            if np.any(mask):
                filas.append({'Genero': g, 'Curso': c, 'PromedioGen': np.round(np.mean(prom_gen[mask]), 2)})
            else:
                filas.append({'Genero': g, 'Curso': c, 'PromedioGen': np.nan})
    comp_genero_df = pd.DataFrame(filas).pivot(index='Genero', columns='Curso', values='PromedioGen')
    print("\n[13] Promedio general por Género y Curso (NumPy):")
    print(comp_genero_df.to_string())
else:
    print("\n[13] No es posible comparar por género: no existe la columna 'Genero'.")

# ------------------------------------------
# 14) Exportación de resultados finales (orden con NumPy)
# ------------------------------------------
# Ordenar por Curso asc y PromedioGen desc con np.lexsort
# Nota: lexsort usa la última clave como primaria
# Claves: ( -PromedioGen, Curso ) -> primaria Curso asc, secundaria PromedioGen desc
orden_final = np.lexsort(( -prom_gen, cursos ))
df_final = df.iloc[orden_final].copy()

# Guardar columnas requeridas
cols_export = list(df_final.columns)  # todas + calculadas
if 'PercentilCurso' not in cols_export:
    cols_export.append('PercentilCurso')
# asegurar orden de algunas claves útiles (opcional)
preferidas = ['Nombre','Curso','PromedioMat','PromedioLen','PromedioGen',
              'EstadoMat','EstadoLen','EstadoGen','PercentilCurso']
cols_export = preferidas + [c for c in df_final.columns if c not in preferidas]

df_final[cols_export].to_csv('alumnos_resultados.csv', index=False)
print("\n[14] Archivo 'alumnos_resultados.csv' exportado (ordenado por Curso asc y PromedioGen desc).")


