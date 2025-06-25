#!/usr/bin/env python

from db import write_csv
import numpy as np
import configparser
import os

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
# OBS: en el pdf de Enrique, dice que esto devuelve un número real, pero en un audio, me parece que
# dice que devuelve un entero. 
def normal_distribution(mean_demand: float, std_dev_demand: float) -> int:
    return int(np.random.normal(mean_demand, std_dev_demand))

# Genera un número aleatorio siguiendo una distribución de Poisson con parámetro lam.
# lam: parámetro de la distribución de Poisson.
def poisson_distribution(lam: float) -> float:
    return np.random.poisson(lam)

# Genera un número aleatorio siguiendo una distribución binomial con n ensayos y probabilidad p.
# n: número de ensayos
# p: probabilidad de éxito en cada ensayo.
def binomial_distribution(n: int, p: float) -> float:
    return np.random.binomial(n, p)

####################################################################
# Generacion de conjuntos
def generate(path_to_files: str) -> None:
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'input_config.ini')

    config = configparser.ConfigParser()
    config.read(config_path)

    number_of_fabrication_centers = config.getint('sets', 'number_of_fabrication_centers')
    number_of_distribution_centers = config.getint('sets', 'number_of_distribution_centers')
    number_of_points_of_sale = config.getint('sets', 'number_of_points_of_sale')

    number_of_scenarios = config.getint('scenarios', 'number_of_scenarios')
    mean_demand = config.getint('scenarios', 'mean_demand')
    std_dev_demand = config.getint('scenarios', 'std_dev_demand')

    # Conjunto de centros de fabricación
    F = list()
    for i in range(0, number_of_fabrication_centers):
        add_fabrication_center(F, f"f_{i}")
    write_csv.add_rows(f"{path_to_files}/fabrication_centers.csv",["nombre", "data"], F)
    # print_fabrication_centers(F)
    print(f"[okay] {number_of_fabrication_centers} fabrication centers have been created.")

    # Conjunto de centros de distribución
    S = list()
    for i in range(0, number_of_distribution_centers):
        add_distribution_center(S, f"s_{i}")
    write_csv.add_rows(f"{path_to_files}/distribution_centers.csv",["nombre", "data"], S)
    # print_distribution_centers(S)
    print(f"[okay] {number_of_distribution_centers} distribution centers have been created.")

    # Conjunto de puntos de venta
    P = list()
    for i in range(0, number_of_points_of_sale):
        add_point_of_sale(P, f"p_{i}")
    write_csv.add_rows(f"{path_to_files}/points_of_sale.csv",["nombre", "data"], P)
    # print_points_of_sale(P)
    print(f"[okay] {number_of_points_of_sale} points of sale have been created.")

    # Conjunto de escenarios de demanda
    E = list()

    generate_demand_scenarios_with_monte_carlo(lambda: normal_distribution(mean_demand, std_dev_demand), E=E, P=P, kE=number_of_scenarios)
    write_csv.add_rows_json(f"{path_to_files}/scenarios-normal.csv",["nombre", "data"], E)
    # print_demand_scenarios(E)
    print(f"[okay] {number_of_scenarios} scenarios using **normal distribution** have been created.")
    #
    ####################################################################

generate(path_to_files="./db/data/conjuntos")
