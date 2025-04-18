import numpy as np

########################################################################
# Modelo de Cadena de Distribución Básica
# ---------------------------------------
########################################################################

########################################################################
# Conjuntos de datos
# ------------------

# Conjunto de $kF$ centros de fabricación
# ---------------------------------------
#
# F = {f_1, f_2, ..., f_i, ..., f_kF}
# F = list()
#
# i → centros de fabricación

# Agrega un centro de fabricación a la lista F.
def add_fabrication_center(F: list, fabrication_center: str) -> None:
    if fabrication_center not in F:
        F.append(fabrication_center)
    return None

# Elimina un centro de fabricación de la lista F.
def remove_fabrication_center(F: list, fabrication_center: str) -> None:
    try:
        F.remove(fabrication_center)
    except ValueError:
        raise ValueError(f"?centro de fabricación {fabrication_center} no está en la lista.")
    return None

# Imprime los centros de fabricación en la lista F.
def print_fabrication_centers(F: list) -> None:
    print("F:", end=" [ ")
    print(", ".join(sorted(F)) + " ]")
    return None

# Conjunto de $kS$ centros de distribución
# ----------------------------------------
#
# S = {s_1, s_2, ..., s_j, ..., s_kS}
# S = list()
#
# j → centros de distribución

# Agrega un centro de distribución a la lista S.
def add_distribution_center(S: list, distribution_center: str) -> None:
    if distribution_center not in S:
        S.append(distribution_center)
    return None

# Elimina un centro de distribución de la lista S.
def remove_distribution_center(S: list, distribution_center: str) -> None:
    try:
        S.remove(distribution_center)
    except ValueError:
        raise ValueError(f"?centro de distribución {distribution_center} no está en la lista.")
    return None

# Imprime los centros de distribución en la lista S.
def print_distribution_centers(S: list) -> None:
    print("S:", end=" [ ")
    print(", ".join(sorted(S)) + " ]")
    return None

# Conjunto de $kP$ puntos de venta
# --------------------------------
#
# P = {p_1, p_2, ..., p_k, ..., p_kP}
# P = list()
#
# k → puntos de venta

# Agrega un punto de venta a la lista P.
def add_point_of_sale(P: list, point_of_sale: str) -> None:
    if point_of_sale not in P:
        P.append(point_of_sale)
    return None

# Elimina un punto de venta de la lista P.
def remove_point_of_sale(P: list, point_of_sale: str) -> None:
    try:
        P.remove(point_of_sale)
    except ValueError:
        raise ValueError(f"?punto de venta {point_of_sale} no está en la lista.")
    return None

# Imprime los puntos de venta en la lista P.
def print_points_of_sale(P: list) -> None:
    print("P:", end=" [ ")
    print(", ".join(sorted(P)) + " ]")
    return None

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
            E[l].append((k, demand))
    return None
#
########################################################################

########################################################################
# Variables de decisión
# ---------------------

# Conjunto de variables de decisión que representan la cantidad de
# producto a producir en el centro de fabricación $i$
# X = {x_1, x_2, ..., x_i, ..., x_kF}
X = set()

# Conjunto de variables de decisión que representan la cantidad de
# producto sobrante en el punto de venta $k$ para el escenario $l$
# Y = {y_1, y_2, ..., y_kl, ..., y_kPkE}
Y = set()

# Conjunto de variables de decisión que representan la cantidad de
# producto demandada que no pudo ser astisfecha en el punto de venta $k$
# para el escenario $l$
# Z = {z_11, z_12, ..., z_kl, ..., z_kPkE}
Z = set()

# Conjunto de variables de decisión que representan la cantidad de
# producto enviado del centro de fabricación $i$ al centro de
# distribución $j$
# wDS = {wds_11, wds_12, ..., wds_ij, ..., wds_kFkS}
wDS = set()

# Conjunto de variables de decisión que representan la cantidad de
# producto enviado del centro de distribución $j$ al punto de venta $k$
# wDP = {wdp_11, wdp_12, ..., wdp_jk, ..., wdp_kSkP}
wDP = set()

#
########################################################################

########################################################################
# Parámetros
# ----------

#Xime TODO

#
########################################################################

########################################################################
# Restricciones
# -------------

#Lu TODO

#
########################################################################

def main():
    # Conjunto de centros de fabricación
    F = list()
    for i in range(0, 10):
        add_fabrication_center(F, f"f_{i}")
    print_fabrication_centers(F)

    # Conjunto de centros de distribución
    S = list()
    for i in range(0, 10):
        add_distribution_center(S, f"s_{i}")
    print_distribution_centers(S)

    # Conjunto de puntos de venta
    P = list()
    for i in range(0, 10):
        add_point_of_sale(P, f"p_{i}")
    print_points_of_sale(P)

    # Conjunto de escenarios de demanda
    E = list()
    generate_demand_scenarios_with_monte_carlo(E=E, P=P, kE=10, min_demand=1, max_demand=100)
    print_demand_scenarios(E)

if __name__ == "__main__":
    main()
