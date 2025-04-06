#!/usr/bin/env python3

from database.config import load_config
from database.db import *

########################################################################
# WIP
"""
def generar_escenarios() -> set:
    return set()

# Función objetivo
# vtas: monto de ventas esperadas
# pStk: penalidad esperada por stock almacenado en los puntos de venta
# pDIn: penalidad esperada por demanda insatisfecha en los puntos de venta
def z(vtas: float, pStk: float, pDIn: float) -> float:
    return vtas - pStk - pDIn

def maximizar(z: callable[[float, float, float], float]) -> float:
    return 0

for escenario in generar_escenarios():
    vtas = escenario['vtas']
    pStk = escenario['pStk']
    pDIn = escenario['pDIn']

print(maximizar(z))
"""
########################################################################

create_supply_chain_database()

config = load_config('database/database.ini', 'postgresql')
conn = get_connection(config)

create_tables(conn)

usuaries_insert_statement = "insert into usuarie (id, nombre, apellido) values (%s, %s, %s)"
usuaries_csv_file = "database/data/usuaries.csv"
insert_data_from_csv(conn, usuaries_insert_statement, usuaries_csv_file)

conn.close()
print("[okay] Connection closed")

a = input("Do you want to dump (backup to a file) the database? (y/n): ")
dump()

a = input("Do you want to restore the database from the dump file? (y/n): ")
restore()
