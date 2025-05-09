#!/usr/bin/env python3

from db.config import load_config
from db.database import *
from db import write_csv
import numpy as np

####################################################################
# DB
# ------------------------------------------------------------------
#
#
config = load_config('db/database.ini', 'postgres')
create_supply_chain_database(config)

config = load_config('db/database.ini', 'supply_chain')
conn = get_connection(config)

create_tables(conn)

####################################################################
# Centros de fabricación
centro_de_fabricacion_insert_statement = "insert into centro_de_fabricacion (nombre, data) values (%s, %s)"
centro_de_fabricacion_csv_file = "./db/data/conjuntos/centros_de_fabricacion.csv"
insert_data_from_csv(conn, centro_de_fabricacion_insert_statement, centro_de_fabricacion_csv_file)
####################################################################

####################################################################
# Centros de distribución
centro_de_distribucion_insert_statement = "insert into centro_de_distribucion (nombre, data) values (%s, %s)"
centro_de_distribucion_csv_file = "./db/data/conjuntos/centros_de_distribucion.csv"
insert_data_from_csv(conn, centro_de_distribucion_insert_statement, centro_de_distribucion_csv_file)
####################################################################

####################################################################
# Puntos de venta
punto_de_venta_insert_statement = "insert into punto_de_venta(nombre, data) values (%s, %s)"
punto_de_venta_csv_file = "./db/data/conjuntos/puntos_de_venta.csv"
insert_data_from_csv(conn, punto_de_venta_insert_statement, punto_de_venta_csv_file)
####################################################################

####################################################################
# Escenarios
escenario_insert_statement = "insert into escenario (nombre, data) values (%s, %s)"
escenario_csv_file = "./db/data/conjuntos/escenarios.csv"
insert_data_from_csv_json(conn, escenario_insert_statement, escenario_csv_file)
####################################################################

conn.close()
print("[okay] Connection closed")
#
####################################################################

# Mock
a = input("Do you want to dump (backup to a file) the database? (y/n): ")
dump("db/data/supply_chain_dump.sql")

a = input("Do you want to restore the database from the dump file? (y/n): ")
restore("db/data/supply_chain_dump.sql")
