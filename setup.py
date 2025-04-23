#!/usr/bin/env python3

from db.config import load_config
from db.database import *
from db import write_csv
import numpy as np

####################################################################
# Operaciones de conjuntos
####################################################################

########################################################################
# Centros de fabricación

# Agrega un centro de fabricación a la lista F.
def add_fabrication_center(F: list, fabrication_center: str) -> None:
    if fabrication_center not in F:
        F.append([fabrication_center, None])
    return None

# Elimina un centro de fabricación de la lista F.
def remove_fabrication_center(F: list, fabrication_center: str) -> None:
    try:
        for fab_center in F:
            if fab_center[0] == fabrication_center:
                F.remove(fab_center)
    except ValueError:
        raise ValueError(f"?centro de fabricación {fabrication_center} no está en la lista.")
    return None

# Imprime los centros de fabricación en la lista F.
def print_fabrication_centers(F: list) -> None:
    names = sorted([name for name, _ in F])
    print("F: [ " + ", ".join(names) + " ]")
#
####################################################################

####################################################################
# Centros de distribución

# Agrega un centro de distribución a la lista S.
def add_distribution_center(S: list, distribution_center: str) -> None:
    if distribution_center not in S:
        S.append([distribution_center, None])
    return None

# Elimina un centro de distribución de la lista S.
def remove_distribution_center(S: list, distribution_center: str) -> None:
    try:
        for dis_center in S:
            if dis_center[0] == distribution_center:
                S.remove(dis_center)
    except ValueError:
        raise ValueError(f"?centro de distribución {distribution_center} no está en la lista.")
    return None

# Imprime los centros de distribución en la lista S.
def print_distribution_centers(S: list) -> None:
    names = sorted([name for name, _ in S])
    print("S: [ " + ", ".join(names) + " ]")
#
####################################################################

####################################################################
# Puntos de venta

# Agrega un punto de venta a la lista P.
def add_point_of_sale(P: list, point_of_sale: str) -> None:
    if point_of_sale not in P:
        P.append([point_of_sale, None])
    return None

# Elimina un punto de venta de la lista P.
def remove_point_of_sale(P: list, point_of_sale: str) -> None:
    try:
        for point in P:
            if point[0] == point_of_sale:
                P.remove(point)
    except ValueError:
        raise ValueError(f"?punto de venta {point_of_sale} no está en la lista.")
    return None

# Imprime los puntos de venta en la lista P.
def print_points_of_sale(P: list) -> None:
    names = sorted([name for name, _ in P])
    print("P: [ " + ", ".join(names) + " ]")
#
####################################################################

####################################################################
# Escenarios

# Imprime los escenarios de demanda en el conjunto E.
def print_demand_scenarios(E: list) -> None:
    print("E:")
    for l in range(len(E)):
        print(f"e_{l}: ", end=" [ ")
        print(", ".join([f"{k}: {d}" for k, d in E[l]]), end=" ]\n")
    return None

# Genera escenarios de demanda utilizando el método de Monte Carlo.
# Se generan $kE$ escenarios de demanda aleatorios entre un mínimo y un
# máximo, para cada punto de venta $k$.
#
# E: escenarios de demanda
# kE: número de escenarios a generar
# P: puntos de venta
# min_demand: demanda mínima
# max_demand: demanda máxima.
def generate_demand_scenarios_with_monte_carlo(E: list, kE: int, P: list, min_demand: int, max_demand: int) -> None:
    for l in range(kE):
        E.append([])
        for k in P:
            demand = np.random.uniform(min_demand, max_demand)
            E[l].append((k[0], demand))
    return None
#
####################################################################

####################################################################
# Generacion de conjuntos
####################################################################

path_to_files = "./db/data/conjuntos"

# Conjunto de centros de fabricación
F = list()
for i in range(0, 10):
    add_fabrication_center(F, f"f_{i}")
write_csv.add_rows(f"{path_to_files}/centros_de_fabricacion.csv",["nombre", "data"], F)
print_fabrication_centers(F)

# Conjunto de centros de distribución
S = list()
for i in range(0, 10):
    add_distribution_center(S, f"s_{i}")
write_csv.add_rows(f"{path_to_files}/centros_de_distribucion.csv",["nombre", "data"], S)
print_distribution_centers(S)

# Conjunto de puntos de venta
P = list()
for i in range(0, 10):
    add_point_of_sale(P, f"p_{i}")
write_csv.add_rows(f"{path_to_files}/puntos_de_venta.csv",["nombre", "data"], P)
print_points_of_sale(P)

# Conjunto de escenarios de demanda
# Obs: la decision de la cantidad de escenarios a generar, junto con las
# demandas mínima y máxima es arbitraria, por ahora. Estos valores se deberían
# definir en base a la heurística, y a las pruebas que hagamos.
E = list()
generate_demand_scenarios_with_monte_carlo(E=E, P=P, kE=10, min_demand=1, max_demand=100)
write_csv.add_rows_json(f"{path_to_files}/escenarios.csv",["nombre", "data"], E)
print_demand_scenarios(E)

####################################################################
# DB
####################################################################

config = load_config('db/database.ini', 'postgres')
create_supply_chain_database(config)

config = load_config('db/database.ini', 'supply_chain')
conn = get_connection(config)

create_tables(conn)

########################################################################
# Centros de fabricación
centro_de_fabricacion_insert_statement = "insert into centro_de_fabricacion (nombre, data) values (%s, %s)"
centro_de_fabricacion_csv_file = "./db/data/conjuntos/centros_de_fabricacion.csv"
insert_data_from_csv(conn, centro_de_fabricacion_insert_statement, centro_de_fabricacion_csv_file)
########################################################################

########################################################################
# Centros de distribución
centro_de_distribucion_insert_statement = "insert into centro_de_distribucion (nombre, data) values (%s, %s)"
centro_de_distribucion_csv_file = "./db/data/conjuntos/centros_de_distribucion.csv"
insert_data_from_csv(conn, centro_de_distribucion_insert_statement, centro_de_distribucion_csv_file)
########################################################################

########################################################################
# Puntos de venta
punto_de_venta_insert_statement = "insert into punto_de_venta(nombre, data) values (%s, %s)"
punto_de_venta_csv_file = "./db/data/conjuntos/puntos_de_venta.csv"
insert_data_from_csv(conn, punto_de_venta_insert_statement, punto_de_venta_csv_file)
########################################################################

########################################################################
# Escenarios
escenario_insert_statement = "insert into escenario (nombre, data) values (%s, %s)"
escenario_csv_file = "./db/data/conjuntos/escenarios.csv"
insert_data_from_csv_json(conn, escenario_insert_statement, escenario_csv_file)
########################################################################

conn.close()
print("[okay] Connection closed")

# Mock
# a = input("Do you want to dump (backup to a file) the database? (y/n): ")
# dump("db/data/supply_chain_dump.sql")

# a = input("Do you want to restore the database from the dump file? (y/n): ")
# restore("db/data/supply_chain_dump.sql")