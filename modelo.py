import random
import re
from db import write_csv
from db.config import load_config
from db.database import *
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
#
# E = {e_1, e_2, ..., e_l, ..., e_kE}
# E = [][]
#
# l → escenarios
def read_scenarios(conn: psycopg.Connection) -> list:
    scenarios = read(conn, "select * from escenario;")
    return scenarios.to_dict(orient='records')
#
########################################################################

########################################################################
# 2. Variables de decisión
########################################################################

########################################################################
# Conjunto de variables de decisión que representan la cantidad de
# producto a producir en el centro de fabricación $i$
#
# X = {x_1, x_2, ..., x_i, ..., x_kF}
# X = list()
#
# Asigna la cantidad de producto a producir en el centro de fabricación
# $i$. Estos valores se toman de la solución de la heurística.
#
# X: lista de cantidades a producir
# solution: diccionario con la solución de la heurística.
def allocate_production_per_center(X: list, solution: dict) -> None:
    X = []
    quantities = solution["X"]
    for i in range(len(quantities)):
        X.append(quantities[i])
    return None
#
########################################################################

########################################################################
# Conjunto de variables de decisión que representan la cantidad de
# producto sobrante en el punto de venta $k$ para el escenario $l$
#
# Y = {y_1, y_2, ..., y_kl, ..., y_kPkE}
# Y = list()
#
# Asigna la cantidad de producto sobrante en el punto de venta $k$ para 
# el escenario $l$. Estos valores se toman de la solución de la
# heurística.
def allocate_surplus_per_point(Y: list, solution: dict) -> None:
    Y = []
    quantities = solution["Y"]
    for kl in range(len(quantities)):
        Y.append(quantities[kl])
    return None 
#
########################################################################

########################################################################
# Conjunto de variables de decisión que representan la cantidad de
# producto demandada que no pudo ser astisfecha en el punto de venta $k$
# para el escenario $l$
#
# Z = {z_11, z_12, ..., z_kl, ..., z_kPkE}
# Z = list()
#
# Asigna la cantidad de producto demandada que no pudo ser satisfecha
# en el punto de venta $k$ para el escenario $l$. Estos valores se toman
# de la solución de la heurística.
def allocate_unsatisfied_demand(Z: list, solution: dict) -> None:
    Z = []
    quantities = solution["Z"]
    for kl in range(len(quantities)):
        Z.append(quantities[kl])
    return None
#
########################################################################

########################################################################
# Conjunto de variables de decisión que representan la cantidad de
# producto enviado del centro de fabricación $i$ al centro de
# distribución $j$
#
# wDS = {wds_11, wds_12, ..., wds_ij, ..., wds_kFkS}
# wDS = list()
#
# Asigna la cantidad de producto enviado del centro de fabricación $i$
# al centro de distribución $j$. Estos valores se toman de la solución
# de la heurística.
#
# wDS: lista de cantidades a enviar
# solution: diccionario con la solución de la heurística.
def allocate_distribution_per_center(wDS: list, solution: dict) -> None:
    wDS = []
    quantities = solution["wDS"]
    for ij in range(len(quantities)):
        wDS.append(quantities[ij])
    return None
#
########################################################################

########################################################################
# Conjunto de variables de decisión que representan la cantidad de
# producto enviado del centro de distribución $j$ al punto de venta $k$
#
# wDP = {wdp_11, wdp_12, ..., wdp_jk, ..., wdp_kSkP}
# wDP = list()
#
# Asigna la cantidad de producto enviado del centro de distribución $j$
# al punto de venta $k$. Estos valores se toman de la solución de la
# heurística.
#
# wDP: lista de cantidades a enviar
# solution: diccionario con la solución de la heurística.
def allocate_distribution_per_point_of_sale(wDP: list, solution: dict) -> None:
    wDP = []
    quantities = solution["wDP"]
    for jk in range(len(quantities)):
        wDP.append(quantities[jk])
    return None
#
########################################################################

########################################################################
# 3. Parámetros
########################################################################

#Xime TODO

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

#Xime TODO

#
########################################################################

########################################################################
# 5. Restricciones
########################################################################

########################################################################
# La cantidad producida se debe distribuir desde los centros de
# fabricación a los centros de distribución según la curva de
# distribución establecida. Surge de X.
#
# F: centros de fabricación
# S: centros de distribución
# X: cantidad de producto a producir en el centro de fabricación $i$
# cf: curva de distribución Fábrica-Centro de distribución
# wDS[i][j] cantidad de producto que se transporta desde el centro de
# fabricación $i$ al centro de distribucion $j$.
def distribuye_a_centros_de_distribucion_segun_curva(F, S, X, cf, wDS):
    return all(X[i] * cf[i, j] == wDS[i, j] for i in range(len(F)) for j in range(len(S)))
#
########################################################################

########################################################################
# La cantidad producida se debe distribuir a los puntos de venta desde
# los centros de distribución según la curva de distribución establecida.
#
# F: centros de fabricación
# S: centros de distribución
# P: puntos de venta
# cp: curva de distribución Centro de distribución-Punto de venta
# wDS[i, j]: cantidad de producto que se transporta desde el centro de
# fabricación $i$ al centro de distribución $j$.
# wDP[j, k]: cantidad de producto que se transporta desde el centro de
# distribución $j$ al punto de venta $k$.
def distribuye_a_centros_de_venta_segun_curva(F, S, P, cp, wDS, wDP):
    return all(suma := sum(wDS[i, j] for i in range(len(F))) * cp[j, k] == wDP[j, k] 
           for j in range(len(S)) for k in range(len(P)))
#
########################################################################

########################################################################
# Para determinar el stock al final del período de comercialización en
# cada punto de venta para cada uno de los escenarios se debe cumplir
# que:
#
# Si la demanda supera a lo que recibió el punto de venta, el stock al
# final del periodo vale 0.
#
# Si no, el stock sobrante se calcula restando lo que recibió el punto
# de venta y la demanda que tuvo.
########################################################################

########################################################################
# Para determinar la demanda insatisfecha en cada punto de venta para
# cada uno de los escenarios se debe cumplir que:
#
# Si la demanda fue menor a lo que recibió el punto de venta, la demanda
# insatisfecha del periodo vale 0.
#
# Si no, la demanda insatisfecha se calcula restando la demanda que tuvo
# el punto de venta y la cantidad de productos que recibió.
########################################################################

########################################################################
# 6. Super Mock Heurística (WIP)
########################################################################

def optimization_heuristic(F, S, P, E, X, Y, Z, wDS, wDP):
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

def supply_chain(m: dict, ct: list, cv: list, pi: list, d: list, cf: list, cp: list, ps: list, pdi: list) -> None:
    print('WIP')

#
########################################################################

# Main de prueba, esto debería ir en un archivo separado.
def main():

    config = load_config('db/database.ini', 'supply_chain')
    conn = get_connection(config)

    fabrication_centers = read_fabrication_centers(conn)
    distribution_centers = read_distribution_centers(conn)
    points_of_sale = read_points_of_sale(conn)
    scenarios = read_scenarios(conn)

    print(scenarios)

    conn.close()
    print("[okay] Connection to supply_chain closed")

    ####################################################################
    # Variables de decisión
    ####################################################################
    
    ####################################################################
    # Parámetros
    ####################################################################

    # cf = dict() # fabricacion - distribucion
    # curva_fabricacion_distribucion = 0.1 #random.randint(0, 10)
    # allocate_distribution_per_center(wDS, X) # crear_curva_fabricacion_distribucion(F, S, cf, curva_fabricacion_distribucion)
    # print('cf: ', cf)

    # cp = dict() # distribucion - ventas
    # curva_distribucion_venta = 0.1 #random.randint(0, 10)
    # crear_curva_distribucion_venta(S, P, cp, curva_distribucion_venta)
    # print('cp: ', cp)

    # ############# Funcion objetivo ##############
    # # X, Y, Z, wDS, wDP
    # X = dict()
    # cantidad = 100
    # generar_produccion_por_centro(X, F, cantidad)
    # print('X: ', X)

    # wDS = dict()
    # cantidad = 10 # fabricacion - distribucion
    # # cada centro de fabricacion manda 10 productos a cada centro de venta --> en cada centro de venta hay 10*10=100 productos
    # allocate_distribution_per_center(wDS, X) # generar_wds(wDS, F, S, cantidad)
    # #wDS[1,1] = 0
    # print('wDS: ', wDS)

    # wDP = dict() # distribucion - ventas
    # cantidad = 10
    # allocate_distribution_per_point_of_sale(wDP, X) # generar_wdp(wDP, S, P, cantidad)
    # #wDS[1,1] = 0
    # print('wDP: ', wDP)

    # ############### Restricciones ###############

    # print(distribuye_a_centros_de_distribucion_segun_curva(F, S, X, cf, wDS))

    # print(distribuye_a_centros_de_venta_segun_curva(F, S, P, cp, wDS, wDP))

if __name__ == "__main__":
    main()
