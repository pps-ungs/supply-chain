import sys
import os
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../modelo')))
import modelo

# Retorna una lista de vecindarios, en los cuales sólo uno de los vecinos es ligeramente diferente al valor 
# de X en el mismo índice. 
# Crea num_neighbors vecindarios.
# Ejemplo de return para num_neighbors=2:
#   [[100, 100, 100, 99.5, 100, 100, 100, 100, 100, 100], 100, 100, 100, 100, 100, 100, 100, 100.5, 100, 100]]
def create_neighbors_one_change(X, step, num_neighbors):
    neighbors = []
    for _ in range(num_neighbors):
        neighbor = X[:]
        idx = random.randint(0, len(X) - 1)
        delta = random.choice([-step, step])
        if neighbor[idx] + delta >= 0:
            neighbor[idx] += delta
        neighbors.append(neighbor)
    return neighbors


# Retorna una lista de vecindarios, en los cuales entre 1 y 3 de los vecinos es ligeramente diferente al valor 
# de X en el mismo índice. 
# Crea num_neighbors vecindarios.
# Ejemplo de return para num_neighbors=2:
#   [[100, 100.5, 100, 100, 100, 100, 100, 100, 100, 100.5], [100, 100, 100, 99.5, 100, 99.5, 100, 100, 99.5, 100]]
def create_multi_change_neighbors(X, step, num_neighbors):
    neighbors = []
    for _ in range(num_neighbors):
        neighbor = X[:]
        for _ in range(random.randint(1, 3)):
            i = random.randint(0, len(X)-1)
            delta = random.choice([-step, step])
            if neighbor[i] + delta >= 0:
                neighbor[i] += delta
        neighbors.append(neighbor)
    return neighbors


# Retorna una lista con 2*len(X) vecindarios. 
# Genera dos vecinos para cada X[i]: X[i] + step y X[i] - step
# Ejemplo de return con len(X)=2:
#   [[[99.5, 100], [100.5, 100], [100, 99.5], [100, 100.5]]
def create_all_neighbors(X, step, *args):
    neighbors = []
    for i in range(len(X)):
        for delta in [-step, step]:
            if X[i] + delta >= 0:
                neighbor = X[:]
                neighbor[i] += delta
                neighbors.append(neighbor)
    return neighbors

def optimization_heuristic_neighbor(F: list, S: list, P: list, E: list, step: float, neighbor_func: callable, num_neighbors=5, max_iterations=1000) -> list:
    X = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100] 
    Y = modelo.get_objective_value(F, S, P, E, X)

    X_best = X
    Y_best = Y

    it = 0
    while it < max_iterations:
        neighbors = neighbor_func(X_best, step, num_neighbors)

        # Lista de tuplas: (vecino, valor_objetivo)
        evaluated = [(n, modelo.get_objective_value(F, S, P, E, n)) for n in neighbors]
        
        # Se elige el que tiene el mayor valor de función objetivo.
        #  best_n: mejor vecino, best_y: valor objetivo
        best_n, best_y = max(evaluated, key=lambda t: t[1])

        if best_y > Y_best:
            X_best = best_n
            Y_best = best_y
        else:
            break

        it += 1

    return [X_best, Y_best] + modelo.get_objective_function_values(F, S, P, E, X_best)
