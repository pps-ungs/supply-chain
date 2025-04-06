########################################################################
# Modelo de Cadena de Distribución Básica
# ---------------------------------------
########################################################################

########################################################################
# Conjuntos de datos
# ------------------

# Conjunto de $kF$ centros de fabricación del producto
# F = {f1, f2, ..., fi, ..., fkF}
F = set()

# Conjunto de $kS$ centros de distribución del producto
# S = {s1, s2, ..., sj, ..., skS}
S = set()

# Conjunto de $kP$ puntos de venta del producto
# P = {p1, p2, ..., pk, ..., pkP}
P = set()

# Conjunto de $kE$ escenarios de demanda posibles
# E = {e1, e2, ..., el, ..., ekE}
E = set()

#
########################################################################

########################################################################
# Variables de decisión
# ---------------------

# Conjunto de variables de decisión que representan la cantidad de
# producto a producir en el centro de fabricación $i$
# X = {x1, x2, ..., xi, ..., xkF}
X = set()

# Conjunto de variables de decisión que representan la cantidad de
# producto sobrante en el punto de venta $k$ para el escenario $l$
# Y = {y1, y2, ..., ykl, ..., ykPkE}
Y = set()