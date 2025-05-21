#!/usr/bin/env python

from db import write_csv
import numpy as np

####################################################################
# Centros de fabricación
# ------------------------------------------------------------------
#
# Agrega un centro de fabricación a la lista F.
def add_fabrication_center(F: list, fabrication_center: str) -> None:
    if fabrication_center not in F:
        F.append([fabrication_center, None])
    return None

# Imprime los centros de fabricación en la lista F.
def print_fabrication_centers(F: list) -> None:
    names = sorted([name for name, _ in F])
    print("F: [ " + ", ".join(names) + " ]")
#
####################################################################

####################################################################
# Centros de distribución
# ------------------------------------------------------------------
#
# Agrega un centro de distribución a la lista S.
def add_distribution_center(S: list, distribution_center: str) -> None:
    if distribution_center not in S:
        S.append([distribution_center, None])
    return None

# Imprime los centros de distribución en la lista S.
def print_distribution_centers(S: list) -> None:
    names = sorted([name for name, _ in S])
    print("S: [ " + ", ".join(names) + " ]")
#
####################################################################

####################################################################
# Puntos de venta
# ------------------------------------------------------------------
#
# Agrega un punto de venta a la lista P.
def add_point_of_sale(P: list, point_of_sale: str) -> None:
    if point_of_sale not in P:
        P.append([point_of_sale, None])
    return None

# Imprime los puntos de venta en la lista P.
def print_points_of_sale(P: list) -> None:
    names = sorted([name for name, _ in P])
    print("P: [ " + ", ".join(names) + " ]")
#
####################################################################

####################################################################
# Escenarios
# ------------------------------------------------------------------
#
# Imprime los escenarios de demanda en el conjunto E.
def print_demand_scenarios(E: list) -> None:
    print("E:")
    for l in range(len(E)):
        print(f"e_{l}: ", end=" [ ")
        print(", ".join([f"{k}: {d}" for k, d in E[l]]), end=" ]\n")
    return None

# Genera escenarios de demanda utilizando el método de Monte Carlo.
# Se generan $kE$ escenarios de demanda aleatorios para cada punto de venta $k$.
#
# probability_distribution: función que genera un número aleatorio siguendo una
#                           distribución de probabilidad.
# E: escenarios de demanda
# kE: número de escenarios a generar
# P: puntos de venta
def generate_demand_scenarios_with_monte_carlo(probability_distribution: callable, E: list, kE: int, P: list) -> None:
    for l in range(kE):
        E.append([])
        for k in P:
            demand = probability_distribution()
            E[l].append((k[0], demand))
    return None
#
####################################################################

# Genera un número aleatorio siguiendo una distribución uniforme entre min_demand y max_demand.
# min_demand: demanda mínima
# max_demand: demanda máxima.
def uniform_distribution(min_demand: int, max_demand: int) -> int:
    return int(np.random.uniform(min_demand, max_demand))

# Genera un número aleatorio siguiendo una distribución normal con media y
# desviación estándar.
#
# mean_demand: demanda promedio esperada
# std_dev_demand: desviación estándar de la demanda.
def normal_distribution(mean_demand: float, std_dev_demand: float) -> float:
    return np.random.normal(mean_demand, std_dev_demand)

# Genera un número aleatorio siguiendo una distribución de Poisson con parámetro lam.
def poisson_distribution(lam: float) -> float:
    return np.random.poisson(lam)

# Genera un número aleatorio siguiendo una distribución binomial con n ensayos y probabilidad p.
def binomial_distribution(n: int, p: float) -> float:
    return np.random.binomial(n, p)

####################################################################
# Generacion de conjuntos
def generate(path_to_files: str) -> None:
    # Conjunto de centros de fabricación
    F = list()
    for i in range(0, 4):
        add_fabrication_center(F, f"f_{i}")
    write_csv.add_rows(f"{path_to_files}/fabrication_centers.csv",["nombre", "data"], F)
    print_fabrication_centers(F)

    # Conjunto de centros de distribución
    S = list()
    for i in range(0, 10):
        add_distribution_center(S, f"s_{i}")
    write_csv.add_rows(f"{path_to_files}/distribution_centers.csv",["nombre", "data"], S)
    print_distribution_centers(S)

    # Conjunto de puntos de venta
    P = list()
    for i in range(0, 50):
        add_point_of_sale(P, f"p_{i}")
    write_csv.add_rows(f"{path_to_files}/points_of_sale.csv",["nombre", "data"], P)
    print_points_of_sale(P)

    # Conjunto de escenarios de demanda
    # Obs: la decision de la cantidad de escenarios a generar, junto con las
    # demandas mínima y máxima es arbitraria, por ahora. Estos valores se deberían
    # definir en base a la heurística, y a las pruebas que hagamos.
    E = list()

    # Generamos 500 escenarios de demanda aleatorios
    number_of_scenarios = 500
    generate_demand_scenarios_with_monte_carlo(lambda: uniform_distribution(min_demand=100, max_demand=500), E=E, P=P, kE=number_of_scenarios)
    # generate_demand_scenarios_with_monte_carlo(lambda: normal_distribution(mean_demand=678, std_dev_demand=25), E=E, P=P, kE=number_of_scenarios)
    # generate_demand_scenarios_with_monte_carlo(lambda: poisson_distribution(100), E=E, P=P, kE=number_of_scenarios)
    # generate_demand_scenarios_with_monte_carlo(lambda: binomial_distribution(100, 0.5), E=E, P=P, kE=number_of_scenarios)

    write_csv.add_rows_json(f"{path_to_files}/scenarios.csv",["nombre", "data"], E)
    print_demand_scenarios(E)
    print("500 scenarios have been created.")
    #
    ####################################################################

generate(path_to_files="./db/data/conjuntos")
