import random
import numpy as np
import re
from db import write_csv
from db.config import load_config
from db.database import *

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

def read_fabrication_centers() -> pd.DataFrame:
    config = load_config('db/database.ini', 'postgresql')
    conn = get_connection(config)
    fabrication_centers = read(conn, "select * from centro_de_fabricacion;")

    print(fabrication_centers)
    return fabrication_centers
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
########################################################################

########################################################################
# Conjunto de $kE$ escenarios de demanda posibles
# -----------------------------------------------
#
# E = {e_1, e_2, ..., e_l, ..., e_kE}
# E = [][]
#
# l → escenarios

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

    ####################################################################
    # Generacion de conjuntos
    ####################################################################
    read_fabrication_centers()
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
