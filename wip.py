########################################################################
# Modelo de Cadena de Distribución Básica
# ---------------------------------------
########################################################################

########################################################################
# Conjuntos de datos
# ------------------

# Conjunto de $kF$ centros de fabricación del producto
# F = {f_1, f_2, ..., f_i, ..., f_kF}
F = set()

# Conjunto de $kS$ centros de distribución del producto
# S = {s_1, s_2, ..., s_j, ..., s_kS}
S = set()

# Conjunto de $kP$ puntos de venta del producto
# P = {p_1, p_2, ..., p_k, ..., p_kP}
P = set()

# Conjunto de $kE$ escenarios de demanda posibles
# E = {e_1, e_2, ..., e_l, ..., e_kE}
E = set()

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
Xime TODO
#
########################################################################

########################################################################
# Restricciones
# -------------
Lu TODO
#
########################################################################