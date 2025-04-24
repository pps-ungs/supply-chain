########################################################################
# 2. y 5. Variables de decisión y sus restricciones
########################################################################

########################################################################
# Conjunto de variables de decisión que representan la cantidad de
# producto a producir en el centro de fabricación $i$
# X = {x_1, x_2, ..., x_i, ..., x_kF}
# X = list()
# Asigna la cantidad de producto a producir en el centro de fabricación
# $i$. Estos valores se toman de la solución de la heurística.
# X: lista de cantidades a producir
# solution: diccionario con la solución de la heurística.
def allocate_production_per_center(X: list, solution: dict) -> None:
    X = []
    quantities = solution["X"]
    for i in range(len(quantities)):
        X.append(quantities[i])
    return None

########################################################################
# La cantidad producida se debe distribuir desde los centros de fabricación a los centros de  distribución según la curva de distribución establecida 
### Parametros ###
    # * X es una lista que contiene cuantos productos se fabrican en cada fabrica.
    # * S es una lista que contiene los centros de distribucion
    # * cf es la curva de distribucion fabricas-centros. Es de la forma: 
    #   [   [0.02, 0.04, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.16, 0.18], 
    #       [0.02, 0.04, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.16, 0.18], 
    #   ... ]
### Retorna ###
    # * wDS = [ [cantidad enviada de la fabrica 0 a cada centro de distr.], [cantidad enviada de la fabrica 1 a cada centro de distr.], ...]
def generate_products_to_distribution_center(X: list, S:list, cf: list) -> list:
    wDS = []
    for i in range(len(X)):
        factory_i = []
        for j in range(len(S)):
            factory_i.append(X[i] * cf[i][j])
        wDS.append(factory_i)
    return wDS

########################################################################
# La cantidad producida se debe distribuir a los puntos de venta desde los centros de distribución según la curva de distribución establecida.
### Parametros ###
    # * F es una lista que contiene las fabricas.
    # * S es una lista que contiene los centros de distribucion 
    # * P es una lista que contiene los puntos de venta
    # * wDS es la cantidad de productos que entrego cada fabrica a cada centro de distribucion. Es de la forma: 
    #   [[0.02, 0.04, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.16, 0.18], [0.02, 0.04, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.16, 0.18], ...]
    #   [ [cantidad enviada de la fabrica 0 a cada centro de distr.], [cantidad enviada de la fabrica 1 a cada centro de distr.], ...]
    # * cp es la curva de distribucion centros-puntos de venta. Es de la forma: 
### Retorna ###
    # * wDP = [ [cantidad enviada del centro de destr. 0 a cada punto de venta], [cantidad enviada del centro de destr. 1 a cada punto de venta], ...]
def generate_products_to_points_of_sale(F:list, S: list, P: list, wDS: list, cp: list):
    wDP = []
    for j in range(len(S)):
        center_j = []
        for k in range(len(P)):
            center_j.append(cp[j][k] * get_products_received_by_center(F, j, wDS))
        wDP.append(center_j)
    return wDP

# Retorna el total de productos que recibió un centro de distribucion: realiza la suma de productos enviados por cada fabrica a ese centro.
### Parametros: ###
    # * F es una lista que contiene las fabricas.
    # * distribution_center es el índice del centro de distribucion a evaluar
    # * wDS es la cantidad de productos que entrego cada fabrica a cada centro de distribucion. Es de la forma: 
    #     [ [cantidad enviada de la fabrica 0 a cada centro de distr.], [cantidad enviada de la fabrica 1 a cada centro de distr.], ...]
def get_products_received_by_center(F: list, distribution_center: int, wDS: list):
    result = 0
    for i in range(len(F)):
        result += wDS[i][distribution_center]
    return result

########################################################################
# Para determinar el stock al final del período de comercialización en cada punto de venta para cada uno de los escenarios se debe cumplir que:
    # Si la demanda supera a lo que recibió el punto de venta, el stock al final del periodo vale 0.
    # Si no, el stock sobrante se calcula restando lo que recibió el punto de venta y la demanda que tuvo.
# Para determinar la demanda insatisfecha en cada punto de venta para cada uno de los escenarios se debe cumplir que:
    # Si la demanda fue menor a lo que recibió el punto de venta, la demanda insatisfecha del periodo vale 0.
    # Si no, la demanda insatisfecha se calcula restando la demanda que tuvo el punto de venta y la cantidad de productos que recibió.
### Parametros ###
    # * S es una lista que contiene los centros de distribucion 
    # * P es una lista que contiene los puntos de venta
    # * d es una lista de diccionarios que contienen la demanda que recibe cada punto de venta en cada escenario posible. Es de la forma:
    #   [   {"p_0": x, "p_1": x, ...}, {"p_0": x, "p_1": x, ...}, {"p_0": x, "p_1": x, ...}, ...]
    # * wDP = es la cantidad de productos que entrego cada centro de distribucion a cada punto de venta. Es de la forma: 
    #      [ [cantidad enviada del centro de destr. 0 a cada punto de venta], [cantidad enviada del centro de destr. 1 a cada punto de venta], ...]
### Retorna ###
    # * Y es el stock sobrante de cada punto de venta al final del periodo en cada escenario. Es de la forma:
    #   [ [stock sobrante en el punto de venta 0 en en escenario 0, stock sobrante en el punto de venta 1 en en escenario 0, ...],
    #     [stock sobrante en el punto de venta 0 en en escenario 1, stock sobrante en el punto de venta 1 en en escenario 1 ...], 
    #   ...]
    # * Z es la demanda insatisfecha de cada punto de venta al final del periodo en cada escenario. Es de la forma:
    #   [ [demanda insatisfecha en el punto de venta 0 en en escenario 0, demanda insatisfecha en el punto de venta 1 en en escenario 0, ...],
    #     [demanda insatisfecha en el punto de venta 0 en en escenario 1, demanda insatisfecha en el punto de venta 1 en en escenario 1 ...], 
    #   ...]
def generate_stock_and_unsatisfied_demand(S: list, P:list, d: list, wDP: list):
    Y = []
    Z = []
    for k in range(len(P)):
        Z_k = []
        Y_k = []
        for l in range(len(d)):
            products_in_k = get_products_received_by_point_of_sale(S, k, wDP)
            key = f"p_{k}"
            if d[l][key] > products_in_k:
                Y_k.append(0)
                Z_k.append(d[l][key] - products_in_k )
            else:
                Y_k.append(products_in_k - d[l][key])
                Z_k.append(0)
        Y.append(Y_k)
        Z.append(Z_k)
    return Y, Z

# Retorna el total de productos que recibió un punto de venta: realiza la suma de productos enviados por cada centro de distribucion a ese punto de venta.
### Parametros: ###
    # * S es una lista que contiene los centros de distribucion.
    # * point_of_sale  es el índice del punto de venta a evaluar
    # * wDP = es la cantidad de productos que entrego cada centro de distribucion a cada punto de venta. Es de la forma: 
    #       [ [cantidad enviada del centro de destr. 0 a cada punto de venta], [cantidad enviada del centro de destr. 1 a cada punto de venta], ...]
def get_products_received_by_point_of_sale(S: list, point_of_sale: int, wDP: list):
    result = 0
    for j in range(len(S)):
        result += wDP[j][point_of_sale]
    return result