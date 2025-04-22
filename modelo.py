import random
import numpy as np
import re
from db import write_csv

########################################################################
# Modelo de Cadena de Distribución Básica
########################################################################

########################################################################
# Conjuntos de datos
########################################################################

########################################################################
# Conjunto de $kF$ centros de fabricación
# ---------------------------------------
#
# Un centro de fabricación $f_i$ sólo tiene nombre.
#
# F = {f_1, f_2, ..., f_i, ..., f_kF}
# F = list()
#
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
#
########################################################################

########################################################################
# Conjunto de $kS$ centros de distribución
# ----------------------------------------
#
# Un centro de distribución $s_j$ sólo tiene nombre.
#
# S = {s_1, s_2, ..., s_j, ..., s_kS}
# S = list()
#
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
# Conjunto de $kP$ puntos de venta
# --------------------------------
#
# Un punto de venta $p_k$ sólo tiene nombre.
#
# P = {p_1, p_2, ..., p_k, ..., p_kP}
# P = list()
#
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
# Variables de decisión
########################################################################

########################################################################
# Conjunto de variables de decisión que representan la cantidad de
# producto a producir en el centro de fabricación $i$
#
# X = {x_1, x_2, ..., x_i, ..., x_kF}

def generar_produccion_por_centro(X: dict, F: list, cantidad: int):
    # Esto deberia salir de la heuristica
    for i in range(len(F)):
        X[i] = cantidad
    return None
#
########################################################################

########################################################################
# Conjunto de variables de decisión que representan la cantidad de
# producto sobrante en el punto de venta $k$ para el escenario $l$
#
# Y = {y_1, y_2, ..., y_kl, ..., y_kPkE}

Y = dict()
#
########################################################################

########################################################################
# Conjunto de variables de decisión que representan la cantidad de
# producto demandada que no pudo ser astisfecha en el punto de venta $k$
# para el escenario $l$
#
# Z = {z_11, z_12, ..., z_kl, ..., z_kPkE}
#
########################################################################

########################################################################
# Conjunto de variables de decisión que representan la cantidad de
# producto enviado del centro de fabricación $i$ al centro de
# distribución $j$
#
# wDS = {wds_11, wds_12, ..., wds_ij, ..., wds_kFkS}

def generar_wds(wDS: dict, F: list, S: list, cantidad: int):
    for i in range(len(F)):
        for j in range(len(S)):
            wDS[i, j] = cantidad
    return None
#
########################################################################

########################################################################
# Conjunto de variables de decisión que representan la cantidad de
# producto enviado del centro de distribución $j$ al punto de venta $k$
#
# wDP = {wdp_11, wdp_12, ..., wdp_jk, ..., wdp_kSkP}

def generar_wdp(wDP: dict, S: list, P: list, cantidad: int):
    for i in range(len(S)):
        for j in range(len(P)):
            wDP[i, j] = cantidad
    return None

#
########################################################################

########################################################################
# Parámetros
# ----------

#Xime TODO

# cf : F × S → R cf_{i,j}
# indica la proporcion de la cantidad de productos fabricados en $i$ que
# se deben enviar al centro de distribución $j$.

def crear_curva_fabricacion_distribucion(F, S, cf, curva_fabricacion_distribucion):
    for i in range(len(F)):
            for j in range(len(S)):
                cf[i, j] = curva_fabricacion_distribucion
    return None

# cp : S × P → R cp_{j,k} curva de distribucion de los productos entregados en los centros de distribucion que se deben enviar a los puntos de venta.
def crear_curva_distribucion_venta(S, P, cp, curva_distribucion_venta):
    for j in range(len(S)):
            for k in range(len(P)):
                cp[j, k] = curva_distribucion_venta
    return None

#
########################################################################

########################################################################
# Restricciones
# -------------

# La cantidad producida se debe distribuir desde los centros de fabricación a los centros de distribución según la curva de distribución establecida. Surge de X.
    # F centros de fabricacion
    # S centros de distribucion
    # X cantidad de producto a producir en el centro de fabricación $i$
    # cf curva de distribucion Fabrica-Centro de distribucion
    # wDS_{i, j} cantidad de producto que se transporta desde el centro de fabricacion i al centro de distribucion j.
def distribuye_a_centros_de_distribucion_segun_curva(F, S, X, cf, wDS):
    return all(X[i] * cf[i, j] == wDS[i, j] for i in range(len(F)) for j in range(len(S)))

# La cantidad producida se debe distribuir a los puntos de venta desde los centros de distribución según la curva de distribución establecida.
    # F centros de fabricacion
    # S centros de distribucion
    # P puntos de venta
    # cp curva de distribucion Centro de distribucion-Punto de venta
    # wDS_{i, j} cantidad de producto que se transporta desde el centro de fabricacion i al centro de distribucion j.
    # wDP_{j, k} cantidad de producto que se transporta desde el centro de distribucion j al punto de venta k.
def distribuye_a_centros_de_venta_segun_curva(F, S, P, cp, wDS, wDP):
    return all(suma := sum(wDS[i, j] for i in range(len(F))) * cp[j, k] == wDP[j, k] 
           for j in range(len(S)) for k in range(len(P)))

# Para determinar el stock al final del período de comercialización en cada punto de venta para cada uno de los escenarios se debe cumplir que:
    # Si la demanda supera a lo que recibió el punto de venta, el stock al final del periodo vale 0.
    # Si no, el stock sobrante se calcula restando lo que recibió el punto de venta y la demanda que tuvo.



# Para determinar la demanda insatisfecha en cada punto de venta para cada uno de los escenarios se debe cumplir que:
    # Si la demanda fue menor a lo que recibió el punto de venta, la demanda insatisfecha del periodo vale 0.
    # Si no, la demanda insatisfecha se calcula restando la demanda que tuvo el punto de venta y la cantidad de productos que recibió.


#
########################################################################

def main():

    ########## Generacion de conjuntos ##########
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
    E = list()
    generate_demand_scenarios_with_monte_carlo(E=E, P=P, kE=10, min_demand=1, max_demand=100)
    write_csv.add_rows_json(f"{path_to_files}/escenarios.csv",["nombre", "data"], E)
    print_demand_scenarios(E)

    # ########## Variables de decision ##########
    
    # ############### Parametros ###############
    # cf = dict() # fabricacion - distribucion
    # curva_fabricacion_distribucion = 0.1 #random.randint(0, 10)
    # crear_curva_fabricacion_distribucion(F, S, cf, curva_fabricacion_distribucion)
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
    # generar_wds(wDS, F, S, cantidad)
    # #wDS[1,1] = 0
    # print('wDS: ', wDS)

    # wDP = dict() # distribucion - ventas
    # cantidad = 10
    # generar_wdp(wDP, F, S, cantidad)
    # #wDS[1,1] = 0
    # print('wDP: ', wDP)

    # ############### Restricciones ###############

    # print(distribuye_a_centros_de_distribucion_segun_curva(F, S, X, cf, wDS))

    # print(distribuye_a_centros_de_venta_segun_curva(F, S, P, cp, wDS, wDP))

if __name__ == "__main__":
    main()
