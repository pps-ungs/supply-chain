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

########################################################################
# m: margen bruto del producto en cada punto de venta
# m = {m_1, m_2, m_k, ..., m_kP}
# m = list()
#
# El margen bruto del producto en cada punto de venta es un valor
# fijo, que se obtiene de la base de datos. Se puede calcular
# a partir de la diferencia entre el precio de venta y el costo
# de producción.
def get_margin_per_point_of_sale(P: list) -> list:
    base_values = [5, 6, 7, 8, 8, 9]
    return [base_values[k % len(base_values)]**2 for k in range(len(P))]
#
########################################################################

########################################################################
# ct = costo de transportar una unidad del producto desde los centros de
#      fabricación a los centros de distribución
# ct = {ct_11, ct_12, ..., ct_ij, ..., ct_kFkS}
# ct = list()
#
# El costo de transporte desde los centros de fabricación a los centros
# de distribución es un valor fijo, que se obtiene de la base de datos.
# Se puede calcular a partir de la distancia entre los centros de
# fabricación y los centros de distribución, multiplicada por el costo
# de transporte por kilómetro.
def get_transportation_cost_from_fabrication_to_distribution(F: list, S: list) -> list:
    base_cost = 1000
    base_values = [1, 2, 3, 5, 8, 13]
    return [[base_values[(i + j) % len(base_values)] * 3 + base_cost for j in range(len(S))] for i in range(len(F))]
#
########################################################################

########################################################################
# cv = costo de transportar una unidad del producto desde los centros de
#      distribución a los puntos de venta
# cv = {cv_11, cv_12, ..., cv_jk, ..., cv_kSkP}
# cv = list()
#
# El costo de transporte desde los centros de distribución a los puntos
# de venta es un valor fijo, que se obtiene de la base de datos. Se puede
# calcular a partir de la distancia entre los centros de distribución y
# los puntos de venta, multiplicada por el costo de transporte por
# kilómetro.
def get_transportation_cost_from_distribution_to_sale(S: list, P: list) -> list:
    base_cost = 800
    base_values = [1, 2, 3, 5, 8, 13]
    return [[base_values[(j + k) % len(base_values)] * 2 + base_cost for j in range(len(S))] for k in range(len(P))]
#
########################################################################

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
# 6. Heurística
########################################################################

# monto de la ganancia esperada
def get_margin(E, P, wDP, Y, pi, m):
    margin = 0
    for k in range(P):
        for l in range(E):
            margin += (wDP[k] - Y[k][l]) * pi[l] * m[k]
    return margin

# penalidad esperada por stock almacenado en los puntos de venta
def get_penalty_stock(E, P, Y, pi, ps):
    pStK = 0
    for l in range(E):
        sum = 0
        for k in range(P):
            sum += ps[k] * Y[k][l]
        pStK += sum * pi[l]
    return pStK

# penalidad esperada por demanda insatisfecha en los puntos de venta
def get_penalty_unsatisfied_demand(E, P, Z, pi, pdi):
    pDIn = 0
    for l in range(E):
        sum = 0
        for k in range(P):
            sum += pdi[k] * Z[k][l]
        pDIn += sum * pi[l]
    return pDIn

# costo de transportar los productos desde los centros 
# de fabricacion a los centros de distribucion
def get_transportation_cost_from_fabrication_to_distribution(F, S, wDS, ct):
    CTf2s = 0
    for i in range(len(F)):
        for j in range(len(S)):
            CTf2s += ct[i][j] * wDS[i][j]
    return CTf2s

# costo de transportar los productos desde los centros 
# de distribucion a los puntos de venta
def get_transportation_cost_from_distribution_to_sale(S, P, wDP, cv):
    CTs2p = 0
    for k in range(len(P)):
        for j in range(len(S)):
            CTs2p += wDP[j][k] * cv[j][k]
    return CTs2p

def optimization_heuristic(F, S, P, E, d, m, cf, cp, ct, cv, pi, ps, pdi):
    X = [100, 200, 300, 400, 500, 100, 200, 300, 400, 500]   # x inicial  TODO: Sprint 4
    margin, pStk, pDIn, CTf2s, CTs2p = get_objective_function_values(F, S, P, E, X, d, m, cf, cp, ct, cv, pi, ps, pdi)
    best_sol = objective_function(margin, pStk, pDIn, CTf2s, CTs2p)
    
    actual_sol = 0
    
    while actual_sol <= best_sol:   # esto tiene que tener un criterio de parada TODO: Sprint 4
        X = [random.randint(0, 1000) for _ in range(len(X))]  # x nuevo ???? TODO: Sprint 4
        margin, pStk, pDIn, CTf2s, CTs2p = get_objective_function_values(F, S, P, E, X, d, m, cf, cp, ct, cv, pi, ps, pdi)
        actual_sol = objective_function(margin, pStk, pDIn, CTf2s, CTs2p)

        if actual_sol > best_sol:
            best_sol = actual_sol

    return X    # esto deberia devolver margin, pStk, pDIn, CTf2s, CTs2p TODO: Sprint 4

def get_objective_function_values(F, S, P, E, X, d, m, cf, cp, ct, cv, pi, ps, pdi):
    wDS = generate_products_to_distribution_center(X, S, cf)
    wDP = generate_products_to_points_of_sale(F, S, P, wDS, cp)
    Y, Z = generate_stock_and_unsatisfied_demand(S, P, d, wDP)
    
    margin = get_margin(E, P, wDP, Y, d, m)
    pStk = get_penalty_stock(E, P, Y, pi, ps)
    pDIn = get_penalty_unsatisfied_demand(E, P, Z, pi, pdi)
    CTf2s = get_transportation_cost_from_fabrication_to_distribution(F, S, wDS, ct)
    CTs2p = get_transportation_cost_from_distribution_to_sale(S, P, wDP, cv)

    return [margin, pStk, pDIn, CTf2s, CTs2p]  