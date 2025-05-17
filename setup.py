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
fabrication_center_insert_statement = "insert into centro_de_fabricacion (nombre, data) values (%s, %s)"
fabrication_center_csv_file = "./db/data/conjuntos/fabrication_centers.csv"
insert_data_from_csv(conn, fabrication_center_insert_statement, fabrication_center_csv_file)
####################################################################

####################################################################
# Centros de distribución
distribution_center_insert_statement = "insert into centro_de_distribucion (nombre, data) values (%s, %s)"
distribution_center_csv_file = "./db/data/conjuntos/distribution_centers.csv"
insert_data_from_csv(conn, distribution_center_insert_statement, distribution_center_csv_file)
####################################################################

####################################################################
# Puntos de venta
point_of_sale_insert_statement = "insert into punto_de_venta(nombre, data) values (%s, %s)"
point_of_sale_csv_file = "./db/data/conjuntos/points_of_sale.csv"
insert_data_from_csv(conn, point_of_sale_insert_statement, point_of_sale_csv_file)
####################################################################

####################################################################
# Escenarios
scenario_insert_statement = "insert into escenario (nombre, data) values (%s, %s)"
scenario_csv_file = "./db/data/conjuntos/scenarios.csv"
insert_data_from_csv_json(conn, scenario_insert_statement, scenario_csv_file)
####################################################################

conn.close()
print("[okay] Connection closed")
#
####################################################################

# Mock
# a = input("Do you want to dump (backup to a file) the database? (y/n): ")
# dump("db/data/supply_chain_dump.sql")

# a = input("Do you want to restore the database from the dump file? (y/n): ")
# restore("db/data/supply_chain_dump.sql")
