# -*- coding: utf-8 -*-
# Resolución de 14 preguntas sobre clientes.csv y movimientos.csv
# Requisitos: pandas (pip install pandas)

import pandas as pd

# ---------- Cargar archivos ----------
clientes = pd.read_csv("d:/p/clientes.csv")
movimientos = pd.read_csv("d:/p/movimientos.csv")

# Asegurar tipos
movimientos["Fecha"] = pd.to_datetime(movimientos["Fecha"], errors="coerce")
movimientos["Monto"] = pd.to_numeric(movimientos["Monto"], errors="coerce")

# Unir movimientos con clientes (para preguntas que requieren datos combinados)
df = movimientos.merge(clientes, on="ClienteID", how="inner")

# --------------------------------------------------------------------------
# 1) Clientes totales
total_clientes = clientes.shape[0]
print("1) Total de clientes registrados:", total_clientes)

# --------------------------------------------------------------------------
# 2) Primeros 5 clientes (nombre y correo)
print("\n2) Primeros 5 clientes (Nombre, Correo):")
print(clientes.loc[:, ["Nombre", "Correo"]].head(5).to_string(index=False))

# --------------------------------------------------------------------------
# 3) Movimientos totales
total_movs = movimientos.shape[0]
print("\n3) Total de movimientos:", total_movs)

# --------------------------------------------------------------------------
# 4) Tipos de movimientos y conteo por tipo
print("\n4) Tipos de movimiento y sus conteos:")
print(movimientos["Descripcion"].value_counts().to_string())

# --------------------------------------------------------------------------
# 5) Montos positivos vs negativos (abonos vs egresos)
conteo_abonos = (movimientos["Monto"] > 0).sum()
conteo_egresos = (movimientos["Monto"] < 0).sum()
print("\n5) Abonos (positivos):", conteo_abonos)
print("   Egresos (negativos):", conteo_egresos)

# --------------------------------------------------------------------------
# 6) Mayor depósito (monto positivo) y a qué cliente pertenece
dep_positivos = df[df["Monto"] > 0]
if not dep_positivos.empty:
    idx_max_dep = dep_positivos["Monto"].idxmax()
    fila_max_dep = dep_positivos.loc[idx_max_dep, ["Fecha", "Monto", "Descripcion", "ClienteID", "Nombre", "RUT", "Correo"]]
    print("\n6) Mayor depósito (positivo):")
    print(fila_max_dep.to_string())
else:
    print("\n6) No hay depósitos positivos.")

# --------------------------------------------------------------------------
# 7) Mayor egreso (monto más negativo) y quién lo realizó
egresos = df[df["Monto"] < 0]
if not egresos.empty:
    idx_min_egreso = egresos["Monto"].idxmin()  # más negativo
    fila_min_egreso = egresos.loc[idx_min_egreso, ["Fecha", "Monto", "Descripcion", "ClienteID", "Nombre", "RUT", "Correo"]]
    print("\n7) Mayor egreso (más negativo):")
    print(fila_min_egreso.to_string())
else:
    print("\n7) No hay egresos negativos.")

# --------------------------------------------------------------------------
# 8) Saldo por cliente (suma de sus movimientos)
saldo_por_cliente = df.groupby(["ClienteID", "Nombre"], as_index=False)["Monto"].sum().rename(columns={"Monto": "Saldo"})
print("\n8) Saldo total por cliente (primeros 10):")
print(saldo_por_cliente.sort_values("Saldo", ascending=False).head(10).to_string(index=False))

# --------------------------------------------------------------------------
# 9) Top 5 clientes con mayor saldo acumulado
top5 = saldo_por_cliente.sort_values("Saldo", ascending=False).head(5)
print("\n9) Top 5 clientes por saldo:")
print(top5.to_string(index=False))

# --------------------------------------------------------------------------
# 10) Número de clientes con saldo total negativo
clientes_saldo_neg = (saldo_por_cliente["Saldo"] < 0).sum()
print("\n10) Clientes con saldo total negativo:", clientes_saldo_neg)

# --------------------------------------------------------------------------
# 11) Promedio de monto de movimientos por cliente y cliente con promedio más alto
promedio_monto_cliente = df.groupby(["ClienteID", "Nombre"], as_index=False)["Monto"].mean().rename(columns={"Monto": "PromedioMonto"})
max_prom = promedio_monto_cliente["PromedioMonto"].max() if not promedio_monto_cliente.empty else None
print("\n11) Promedio de monto por cliente (primeros 10):")
print(promedio_monto_cliente.sort_values("PromedioMonto", ascending=False).head(10).to_string(index=False))
if max_prom is not None:
    fila_max_prom = promedio_monto_cliente.loc[promedio_monto_cliente["PromedioMonto"].idxmax()]
    print("\n   Cliente con mayor promedio de movimiento:")
    print(fila_max_prom.to_string(index=False))

# --------------------------------------------------------------------------
# 12) Mes con más movimientos en total
if movimientos["Fecha"].notna().any():
    movs_por_mes = movimientos.assign(Mes=movimientos["Fecha"].dt.to_period("M")).groupby("Mes").size().sort_values(ascending=False)
    print("\n12) Conteo de movimientos por mes:")
    print(movs_por_mes.to_string())
    mes_top = movs_por_mes.idxmax() if not movs_por_mes.empty else None
    print("   Mes con más movimientos:", mes_top)
else:
    print("\n12) No hay fechas válidas para calcular el mes con más movimientos.")

# --------------------------------------------------------------------------
# 13) Cliente más activo (mayor cantidad de movimientos)
conteo_movs_cliente = df.groupby(["ClienteID", "Nombre"]).size().reset_index(name="CantidadMovs")
if not conteo_movs_cliente.empty:
    fila_mas_activo = conteo_movs_cliente.sort_values("CantidadMovs", ascending=False).iloc[0]
    print("\n13) Cliente más activo (más movimientos):")
    print(fila_mas_activo.to_string())
else:
    print("\n13) No hay movimientos para determinar el cliente más activo.")

# --------------------------------------------------------------------------
# 14) Resumen por cliente: total abonos, total egresos y saldo final
def sum_pos(x):
    return x[x > 0].sum() if not x.empty else 0
def sum_neg(x):
    return x[x < 0].sum() if not x.empty else 0

resumen = df.groupby(["ClienteID", "Nombre"])["Monto"].agg(
    TotalAbonos=lambda s: sum_pos(s),
    TotalEgresos=lambda s: sum_neg(s),
    Saldo="sum"
).reset_index()

print("\n14) Resumen por cliente (primeros 10):")
print(resumen.sort_values("Saldo", ascending=False).head(10).to_string(index=False))


