# -*- coding: utf-8 -*-
"""
Created on Mon Aug 25 09:34:10 2025

@author: Lenovo
"""

import pandas as pd

clientes = pd.read_csv("c:/spider/clientes.csv")
movimientos = pd.read_csv("c:/spider/movimientos.csv")

#UNIRLOS POR CLIENTEID

df = pd.merge(movimientos, clientes, on="ClienteID", how="inner")


#1. Clientes totales

total_clientes = len(clientes)
"""total.clie = clientes.shape[0]
esto es mas profesionalll!!! OJOOOOOOOO hacelo asi!!
"""

#2. Primeros Clientes

primeros_5 = clientes[['Nombre','Correo']].head()

#3. Movimientos totales¿cuantos movimientos contiene el archivo movimientos.csv?

total_movimientos = len(movimientos)
print(total_movimientos)

#4. Tipos de movimientos

tipo_movimientos = movimientos["Descripcion"].value_counts()

#5. Montos positivos vs montos negativos¿cuantos son abonos y ctos egresos?


movimientos['Tipo'] = movimientos['Monto'].apply(lambda x: 'Abonos' if x>0 else 'Egreso')

montos_positivos = len(movimientos[movimientos['Monto']>=0])
montos_negativos = len(movimientos[movimientos['Monto']<0])


#6. Mayor deposito (cualquier abono) y a que cliente pertenece

dep_positivo = df[df['Monto']>0]
if not dep_positivo.empty:
    idx_max_dep = dep_positivo['Monto'].idxmax()
    fila_max_dep = dep_positivo.loc[idx_max_dep, ['Fecha','Monto','Descripcion','ClienteID', 'Nombre', 'RUT', 'Correo']]
    print("\n6) Mayor deposito (positivo):")
    print(fila_max_dep.to_string())
    
else:
    print ("\n6) No hay deposito positivo.")
    
    
#7. Mayor egreso

egresos = df[df['Monto']<0]
if not egresos.empty:
    idx_min_egres = egresos['Monto'].idxmin()
    fila_min_egre = egresos.loc[idx_min_egres, ['Fecha','Monto','Descripcion','ClienteID', 'Nombre', 'RUT', 'Correo']]
    print("\n6) Menor egreso (negativo):")
    print(fila_min_egre.to_string())
    
else:
    print ("\n6) No hay deposito negativo.")


#8. 