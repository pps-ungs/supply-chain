import random
import re
from db.config import load_config
from db.database import *
from variables_de_decision import *
import warnings
warnings.filterwarnings('ignore') # get rid of annoying pandas warnings

########################################################################
# Modelo de Cadena de Distribución Básica
########################################################################

########################################################################
# 1. Conjuntos de datos
########################################################################

########################################################################
# Conjunto de $kF$ centros de fabricación ✅
# ---------------------------------------
#
# Un centro de fabricación $f_i$ sólo tiene nombre, no tiene datos
# asociados.
#
# F = {f_1, f_2, ..., f_i, ..., f_kF}
# F = list()
#
# Importante: los centros de fabricación van con $i$.
# i → centros de fabricación

def read_fabrication_centers(conn: psycopg.Connection) -> list:
    fabrication_centers = read(conn, "select * from centro_de_fabricacion;")
    return fabrication_centers.to_dict(orient='records')
#
########################################################################

########################################################################
# Conjunto de $kS$ centros de distribución ✅
# ----------------------------------------
#
# Un centro de distribución $s_j$ sólo tiene nombre, no tiene datos
# asociados.
#
# S = {s_1, s_2, ..., s_j, ..., s_kS}
# S = list()
#
# Importante: los centros de distribución van con $j$.
# j → centros de distribución

def read_distribution_centers(conn: psycopg.Connection) -> list:
    distribution_centers = read(conn, "select * from centro_de_distribucion;")
    return distribution_centers.to_dict(orient='records')
#
########################################################################

########################################################################
# Conjunto de $kP$ puntos de venta ✅
# --------------------------------
#
# Un punto de venta $p_k$ sólo tiene nombre, no tiene datos asociados.
# (Pueden contener lugar de almacenamiento.)
#
# P = {p_1, p_2, ..., p_k, ..., p_kP}
# P = list()
#
# Importante: los puntos de venta van con $k$.
# k → puntos de venta

def read_points_of_sale(conn: psycopg.Connection) -> list:
    points_of_sale = read(conn, "select * from punto_de_venta;")
    return points_of_sale.to_dict(orient='records')
#
########################################################################

########################################################################
# Conjunto de $kE$ escenarios de demanda posibles
# -----------------------------------------------
# E = {e_1, e_2, ..., e_l, ..., e_kE}
# E = [][]
# l → escenarios
def read_scenarios(conn: psycopg.Connection) -> list:
    scenarios = read(conn, "select * from escenario;")
    return scenarios.to_dict(orient='records')


########################################################################
# 3. Parámetros
########################################################################

# m: margen bruto del producto en cada punto de venta
def get_margin_per_point_of_sale(P):
    base_values = [5, 6, 7, 8, 8, 9]
    return [base_values[i % len(base_values)]**2 for i in range(len(P))]

# ct = costo de transportar una unidad del producto desde los centros de fabricacion a los centros de distribucion
def get_transportation_cost_from_fabrication_to_distribution(F, S):
    base_cost = 1000
    base_values = [1, 2, 3, 5, 8, 13]
    return [[base_values[(i + j) % len(base_values)] * 3 + base_cost for i in range(len(S))] for j in range(len(F))]

# cv = costo de transportar una unidad del producto desde los centros de distribucion a los puntos de venta
def get_transportation_cost_from_distribution_to_sale(S, P):
    base_cost = 800
    base_values = [1, 2, 3, 5, 8, 13]
    return [[base_values[(i + j) % len(base_values)] * 2 + base_cost for i in range(len(S))] for j in range(len(P))]

# pi = probabilidad de ocurrencia del escenario
def get_probability_of_occurrence(E):
    return [0.3 for _ in range(len(E))] # equiprobable

# d = demanda de cada punto de venta para cada escenario
def get_demand_per_point_of_sale(E, P):
    return [e['data'] for e in E]

# cf = curva de distribucion de los productos fabricados a los diferentes centros de distribucion
def get_distribution_curve_from_fabrication_to_distribution(F, S):
    return [[round((i + 1) / sum(range(1, len(S) + 1)), 2) for i in range(len(S))] for _ in range(len(F))]

# cp = curva de distribucion de los productos entregados en los centros de distribucion que se deben enviar a los puntos de venta
def get_distribution_curve_from_distribution_to_sale(S, P):
    return [[round((i + 1) / sum(range(1, len(S) + 1)), 2) for i in range(len(P))] for _ in range(len(S))]

# ps = Penalidad unitaria por dejar un producto en el punto de venta sin comercializar
def get_distribution_curve_from_fabrication_to_sale(F, P):
    m = get_margin_per_point_of_sale(P)
    return [m[i] * 0.15 for i in range(len(P))]

# pdi = Penalidad unitaria por demanda insatisfecha en un punto de venta
def get_penalty_for_unsatisfied_demand(P):
    m = get_margin_per_point_of_sale(P)
    return [m[i] * 0.1 for i in range(len(P))]
#
########################################################################

########################################################################
# 4. Función objetivo
########################################################################

# Función objetivo a maximizar
# margen: ganancia bruta del producto en cada punto de venta
# pStk: costo de mantener el stock en el punto de venta
# pDIn: costo de la demanda insatisfecha en el punto de venta
# CTf2s: costo de transporte desde el centro de fabricación al centro de
#        distribución
# CTs2p: costo de transporte desde el centro de distribución al punto de
#        venta
def objective_function(margen, pStk, pDIn, CTf2s, CTs2p):
    return margen - pStk - pDIn - CTf2s - CTs2p
#
########################################################################

########################################################################
# 6. Super Mock Heurística (WIP)
########################################################################
def optimization_heuristic(F, S, P, E, X, Y, Z, wDS, wDP, d):
    # Inicializar variables de decisión
    X = [0] * len(F)
    Y = [0] * len(P) * len(E)
    Z = [0] * len(P) * len(E)
    wDS = [0] * len(F) * len(S)
    wDP = [0] * len(S) * len(P)

    # Generar una solución inicial aleatoria
    for i in range(len(F)):
        X[i] = random.randint(1, 100)

    for j in range(len(S)):
        for k in range(len(P)):
            wDP[j][k] = random.randint(1, 100)

    # Calcular la función objetivo
    objective_value = sum(X) + sum(Y) + sum(Z) + sum(wDS) + sum(wDP)

    return {
        "X": X,
        "Y": Y,
        "Z": Z,
        "wDS": wDS,
        "wDP": wDP,
        "objective_value": objective_value
    }

def supply_chain(objective_function, m: dict, ct: list, cv: list, pi: list, d: list, cf: list, cp: list, ps: list, pdi: list) -> None:
    print('WIP')
#
########################################################################

def main():

    ####################################################################
    # Conjuntos
    ####################################################################

    config = load_config('db/database.ini', 'supply_chain')
    conn = get_connection(config)

    F = read_fabrication_centers(conn)
    S = read_distribution_centers(conn)
    P = read_points_of_sale(conn)
    E = read_scenarios(conn)
    
    print("E:",E)

    conn.close()
    print("[okay] Connection to supply_chain closed")

    ####################################################################
    # Parámetros
    ####################################################################

    m = get_margin_per_point_of_sale(P)
    ct = get_transportation_cost_from_fabrication_to_distribution(F, S)
    cv = get_transportation_cost_from_distribution_to_sale(S, P)
    pi = get_probability_of_occurrence(E)
    d = get_demand_per_point_of_sale(E, P)
    cf = get_distribution_curve_from_fabrication_to_distribution(F, S)
    cp = get_distribution_curve_from_distribution_to_sale(S, P)
    ps = get_distribution_curve_from_fabrication_to_sale(F, P)
    pdi = get_penalty_for_unsatisfied_demand(P)

    print("S:", S)
    print("P:", P)
    print("CP:", cp)
    print("CF:", cf)
    print("d:", d)

    X = [100, 200, 300, 400, 500, 100, 200, 300, 400, 500]
    wDS = generate_products_to_distribution_center(X, S, cf)

    print("wDS:", wDS)

    wDP = generate_products_to_points_of_sale(F, S, P, wDS, cp)

    Y, Z = generate_stock_and_unsatisfied_demand(S, P, d, wDP)
    print("Y:", Y)
    print("Z:", Z)

    supply_chain(objective_function, m, ct, cv, pi, d, cf, cp, ps, pdi)


if __name__ == "__main__":
    main()
