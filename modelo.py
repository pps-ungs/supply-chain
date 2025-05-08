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
# Conjunto de $kF$ centros de fabricación
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
# Conjunto de $kS$ centros de distribución
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
# Conjunto de $kP$ puntos de venta
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
#
# E = {e_1, e_2, ..., e_l, ..., e_kE}
# E = [][]
# l → escenarios
def read_scenarios(conn: psycopg.Connection) -> list:
    scenarios = read(conn, "select * from escenario;")
    return scenarios.to_dict(orient='records')
#
########################################################################

########################################################################
# 3. Parámetros
########################################################################

########################################################################
# Nota:
# -----
#
# Todos estos parámetros son fijos, pero no necesariamente se obtienen
# de la base de datos.
#
# Ahora están calculados a partir de valores base porque da más
# flexibilidad a la hora de cambiar la cantidad de escenarios, puntos de
# venta, etc.
#
# Esto sirve para hacer pruebas con instancias más chicas.
#
# Cómo los calculamos y si tienen sentido, son cosas que tenemos que ver
# con las pruebas.
#
# Podemos hacer un hardcodeo de los valores en la base de datos.
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

# ojo que no tenemos esos datos
def get_margin_per_point_of_sale(P: list) -> list:
    base_margin = 300
    base_values = [5, 6, 7, 8, 8, 9]
    return [base_values[k % len(base_values)]**2 + base_margin for k in range(len(P))]
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

# idem caso anterior, no tenemos esos datos
def get_unit_transportation_cost_from_fabrication_to_distribution(F: list, S: list) -> list:
    base_cost = 2
    base_values = [1, 2, 3, 4, 5, 6]
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

# idem
def get_unit_transportation_cost_from_distribution_to_sale(S: list, P: list) -> list:
    base_cost = 1.5
    base_values = [1, 2, 3, 4, 5, 6]
    return [[base_values[(j + k) % len(base_values)] * 2 + base_cost for j in range(len(S))] for k in range(len(P))]
#
########################################################################

# pi = probabilidad de ocurrencia del escenario
def get_probability_of_occurrence(E):   # FIXME: no estoy leyendo las probabilidades de E, para simplificar, por ahora
    return [1 / len(E) for _ in range(len(E))] # equiprobable

# d = demanda de cada punto de venta para cada escenario
def get_demand_per_point_of_sale(E):
    rounded_demands = []
    for e in E:
        rounded_data = {key: max(0, int(round(value))) for key, value in e['data'].items()}
        rounded_demands.append(rounded_data)
    return rounded_demands

# cf = curva de distribucion de los productos fabricados a los diferentes centros de distribucion
def get_distribution_curve_from_fabrication_to_distribution(F, S):
    base_pattern = [1, 2, 3, 4, 5]
    matrix = []
    for i in range(len(F)):
        curve = [(base_pattern[i % len(base_pattern)]) * (i + j) for j in range(len(S))]
        total = sum(curve)
        curve = [value / total for value in curve]
        matrix.append(curve)
    return matrix

# cp = curva de distribucion de los productos entregados en los centros de distribucion que se deben enviar a los puntos de venta
def get_distribution_curve_from_distribution_to_sale(S, P):
    base_pattern = [1, 2, 3, 4, 5]
    matrix = []
    for j in range(len(S)):
        curve = [base_pattern[j % len(base_pattern)] + k * j for k in range(len(P))]
        total = sum(curve)
        curve = [value / total for value in curve]
        matrix.append(curve)
    return matrix

# ps = Penalidad unitaria por dejar un producto en el punto de venta sin comercializar
def get_distribution_curve_from_fabrication_to_sale(F, P):
    m = get_margin_per_point_of_sale(P)
    return [m[i] * 0.05 for i in range(len(P))]

# pdi = Penalidad unitaria por demanda insatisfecha en un punto de venta
def get_penalty_for_unsatisfied_demand(P):
    m = get_margin_per_point_of_sale(P)
    return [m[i] * 0.03 for i in range(len(P))]
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
# esto no esta bien, (wDP[j][k] - Y[k][l])  es negativo
def get_margin(E, P, S, wDP, Y, pi, m):
    margin = 0
    # for j in range(len(S)):     # no es lo que dice el enunciado, pero falta un indice
    for k in range(len(P)):
        for l in range(len(E)):
            # margin += wDP[j][k] - Y[l][k]) * pi[l] * m[k]
            margin += (get_products_received_by_point_of_sale(S, k, wDP) - Y[l][k]) * pi[l] * m[k]
    return margin

# penalidad esperada por stock almacenado en los puntos de venta
def get_penalty_stock(E, P, Y, pi, ps):
    pStK = 0
    for l in range(len(E)):
        sum = 0
        for k in range(len(P)):
            sum += ps[k] * Y[l][k]
        pStK += sum * pi[l]
    return pStK

# penalidad esperada por demanda insatisfecha en los puntos de venta
def get_penalty_unsatisfied_demand(E, P, Z, pi, pdi):
    pDIn = 0
    for l in range(len(E)):
        sum = 0
        for k in range(len(P)):
            sum += pdi[k] * Z[l][k]
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

def optimization_heuristic(F: list, S: list, P: list, E: list, step: float, max_iterations: int = 1000) -> list:
    # this should be on the database
    probabilities = get_probability_of_occurrence(E)

    for i in range(len(E)):
        scenario = E[i]
        scenario["probability"] = probabilities[i]

    E = sorted(E, key=lambda x: x['probability'], reverse=True)

    X = get_initial_X(E)
    Y = get_objective_value(F, S, P, E, X)
    
    X_best = X
    Y_best = Y

    actual_sol = 0
    it = 0

    while it < max_iterations:  # Basic termination condition. fixme with a better one
        # Generating a new solution...
        # X = get_x()       para random restart
        # Y = get_objective_value(F, S, P, E, X)

        # Basic creation of neighbourhood
        X_1 = [X[i] - step for i in range(len(X))]
        X_2 = [X[i] + step for i in range(len(X))]

        # Evaluation of the neighbourhood
        Y_1 = get_objective_value(F, S, P, E, X_1)
        Y_2 = get_objective_value(F, S, P, E, X_2)

        X_best_neighbour, Y_best_neighbour = get_best_sol([X, X_1, X_2], [Y, Y_1, Y_2])

        # Comparing the best solution with the current one
        if X_best_neighbour > X_best and Y_best_neighbour > 0:
            X_best = X_best_neighbour
            Y_best = Y_best_neighbour

        # Shall we stop when we dont find a better solution?
        it += 1

    return [X_best, Y_best] + get_objective_function_values(F, S, P, E, X_best) + [get_objective_value(F, S, P, E, X_best)]

def get_initial_X(E: list) -> list:
    return [488 for _ in range(len(E))]

def get_x() -> list:
    return [random.randint(0, 1000) for _ in range(10)]

def get_best_sol(X: list, sol: list) -> list:
    best_y = sol[0]
    best_x = X[0]

    for i in range(1, len(sol)):
        if sol[i] > best_y:
            best_y = sol[i]
            best_x = X[i]

    return [best_x, best_y]

def get_objective_value(F, S, P, E, X):
    margin, pStk, pDIn, CTf2s, CTs2p = get_objective_function_values(F, S, P, E, X)
    return objective_function(margin, pStk, pDIn, CTf2s, CTs2p)

def get_objective_function_values(F, S, P, E, X):
    m = get_margin_per_point_of_sale(P)
    ct = get_unit_transportation_cost_from_fabrication_to_distribution(F, S)
    cv = get_unit_transportation_cost_from_distribution_to_sale(S, P)
    pi = get_probability_of_occurrence(E)
    d = get_demand_per_point_of_sale(E)
    cf = get_distribution_curve_from_fabrication_to_distribution(F, S)
    cp = get_distribution_curve_from_distribution_to_sale(S, P)
    ps = get_distribution_curve_from_fabrication_to_sale(F, P)
    pdi = get_penalty_for_unsatisfied_demand(P)

    wDS = generate_products_to_distribution_center(X, S, cf)
    wDP = generate_products_to_points_of_sale(F, S, P, wDS, cp)
    Y, Z = generate_stock_and_unsatisfied_demand(S, P, d, wDP)
    
    margin = get_margin(E, P, S, wDP, Y, pi, m)
    pStk = get_penalty_stock(E, P, Y, pi, ps)
    pDIn = get_penalty_unsatisfied_demand(E, P, Z, pi, pdi)
    CTf2s = get_transportation_cost_from_fabrication_to_distribution(F, S, wDS, ct)
    CTs2p = get_transportation_cost_from_distribution_to_sale(S, P, wDP, cv)

    return [margin, pStk, pDIn, CTf2s, CTs2p]


# F = ["f_0", "f_1", "f_2"]
# S = ["c_0", "c_1", "c_2"]
# P = ["p_0", "p_1", "p_2"]
# d = [{"p_0": 1, "p_1": 1, "p_2": 1}, {"p_0": 1, "p_1": 1, "p_2": 1}]
# wDS = [[3, 3, 3], [3, 3, 3], [3, 3, 3]] # cada centro de distr recibe 9 productos
# cp = [[0.1, 0.1, 0.1], [0.1, 0.1, 0.1], [0.1, 0.1, 0.1]] # cada centro de distr envia el 30% a cada centro de venta
# # cada punto de venta deberia recibir 3 productos, y quedarse con 2 sobrantes
# wDP = generate_products_to_points_of_sale(F, S, P, wDS, cp)
# Y, Z = generate_stock_and_unsatisfied_demand(S, P, d, wDP)
# print(wDP, Y, Z)
