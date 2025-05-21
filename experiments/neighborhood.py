import sys
import os
import random
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../modelo')))
import model


########################################################################
# Creación de vecinos
########################################################################

#* Retorna una lista de vecindarios, en los cuales sólo uno de los vecinos es ligeramente diferente al valor 
#* de X en el mismo índice. 
# Crea num_neighbors vecindarios.
# Ejemplo de return para num_neighbors=2:
#   [[100, 100, 100, 99.5, 100, 100, 100, 100, 100, 100], 100, 100, 100, 100, 100, 100, 100, 100.5, 100, 100]]
def create_one_change_neighbors(X, step, num_neighbors):
    neighbors = []
    for _ in range(num_neighbors):
        neighbor = X[:]
        idx = random.randint(0, len(X) - 1)
        delta = random.choice([-step, step])
        if neighbor[idx] + delta >= 0:
            neighbor[idx] += delta
        neighbors.append(neighbor)
    return neighbors

#* Retorna una lista de vecindarios, en los cuales entre 1 y 3 de los vecinos es ligeramente diferente al valor 
#* de X en el mismo índice. 
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
    ("Vecinos con multi change:", neighbors)
    return neighbors


#* Retorna una lista con 2*len(X) vecindarios. 
# Genera dos vecinos para cada X[i]: X[i] + step y X[i] - step
# Ejemplo de return con len(X)=2:
#   [[[99.5, 100], [100.5, 100], [100, 99.5], [100, 100.5]]
def create_exhaustive_neighbors(X, step, *args):
    neighbors = []
    for i in range(len(X)):
        for delta in [-step, step]:
            if X[i] + delta >= 0:
                neighbor = X[:]
                neighbor[i] += delta
                neighbors.append(neighbor)
    ("Vecinos con exhaustive change:", neighbors)
    return neighbors

def get_neighbor_strategies():
    return  {
    "one_change": create_one_change_neighbors,
    "exhaustive": create_exhaustive_neighbors,
    "multi_change": create_multi_change_neighbors,
    } 

########################################################################
# Evaluación de vecinos
########################################################################

#* Retorna la solución con mejor valor objetivo.
# Parametros:
    # evaluated: lista de tuplas --> [(vecino1, valor obj), (vecino2, valor obj), ..., (vecinoN, valor obj)]
    # current_value: mejor valor objetivo actual.
# Retorna una tupla: (mejor vecino, mejor funcion objetivo) o (None, valor objetivo actual)
def greedy_selection_eval(evaluated: tuple, current_value: float):
    best_n, best_y = max(evaluated, key=lambda t: t[1])
    return (best_n, best_y) if best_y > current_value else (None, current_value)

#* Retorna la primera solución que mejora la solución actual.
# Parametros:
    # evaluated: lista de tuplas --> [(vecino1, valor obj), (vecino2, valor obj), ..., (vecinoN, valor obj)]
    # current_value: mejor valor objetivo actual.
# Retorna una tupla: (mejor vecino, mejor funcion objetivo) o (None, valor objetivo actual)
def first_improvement_eval(evaluated, current_value):
    for n, y in evaluated:
        if y > current_value:
            return n, y
    return None, current_value

#* Retorna una solución elegida al azar que mejora la solución actual.
# Parametros:
    # evaluated: lista de tuplas --> [(vecino1, valor obj), (vecino2, valor obj), ..., (vecinoN, valor obj)]
    # current_value: mejor valor objetivo actual.
# Retorna una tupla: (mejor vecino, mejor funcion objetivo) o (None, valor objetivo actual)
def stochastic_selection_eval(evaluated, current_value):
    improving = [(n, y) for n, y in evaluated if y > current_value]
    if improving:
        return random.choice(improving)
    return None, current_value

def get_eval_strategies():
    return  {
    "greedy": greedy_selection_eval,
    "first-improvement": first_improvement_eval,
    "stochastic": stochastic_selection_eval,
    } 

########################################################################
# Heurísticas con estrategias
########################################################################

#* Evaluación de vecinos: Greedy.
#* Creación de vecinos: strategy.
def optimization_heuristic_neighbors_exp(F: list, S: list, P: list, E: list, step: float, neighbor_strategy: callable, num_neighbors=5, max_iterations=1000) -> list:
    X = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100] 
    Y = model.get_objective_value(F, S, P, E, X)
    X_best = X
    Y_best = Y
    it = 0
    while it < max_iterations:
        neighbors = neighbor_strategy(X_best, step, num_neighbors)
        # Lista de tuplas: (vecino, valor_objetivo)
        evaluated = [(n, model.get_objective_value(F, S, P, E, n)) for n in neighbors]
        # Se elige el que tiene el mayor valor de función objetivo.
        #  best_n: mejor vecino, best_y: valor objetivo
        best_n, best_y = max(evaluated, key=lambda t: t[1])
        if best_y > Y_best:
            X_best = best_n
            Y_best = best_y
        else:
            break
        it += 1
    return [X_best, Y_best] + model.get_objective_function_values(F, S, P, E, X_best) 

#* Evaluación de vecinos: strategy.
#* Creación de vecinos: exhaustive
def optimization_heuristic_eval_exp(F: list, S: list, P: list, E: list, step:20, eval_strategy: callable, max_iterations=10000) -> list:
    X = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100] 
    Y = model.get_objective_value(F, S, P, E, X)
    X_best = X
    Y_best = Y
    it = 0
    while it < max_iterations:
        neighbors = create_exhaustive_neighbors(X_best, step)
        # lista de tuplas: [(vecino1, valor obj), (vecino2, valor obj), ..., (vecinoN, valor obj)]
        evaluated = [(n, model.get_objective_value(F, S, P, E, n)) for n in neighbors]

        best_n, best_y = eval_strategy(evaluated, Y_best)
        if best_n is not None:
            X_best = best_n
            Y_best = best_y
        else:
            break
        it += 1
    return [X_best, Y_best] + model.get_objective_function_values(F, S, P, E, X_best) 

#* Evaluación de vecinos: strategy.
#* Creación de vecinos: strategy.
def optimization_heuristic_neighbors_eval_exp(F: list, S: list, P: list, E: list, step: float, neighbor_strategy: callable, eval_strategy: callable, num_neighbors=5, max_iterations=1000) -> list:
    X = [100 for _ in F] 
    Y = model.get_objective_value(F, S, P, E, X)
    X_best = X
    Y_best = Y
    it = 0
    while it < max_iterations:
        neighbors = neighbor_strategy(X_best, step, num_neighbors)
        evaluated = [(n, model.get_objective_value(F, S, P, E, n)) for n in neighbors]

        best_n, best_y = eval_strategy(evaluated, Y_best)
        if best_n is not None:
            X_best = best_n
            Y_best = best_y
        else:
            break
        it += 1
    return [X_best, Y_best] + model.get_objective_function_values(F, S, P, E, X_best) 

########################################################################
# Correr experimentos
########################################################################

def run_heuristic_with_neighbors_strategy(F: list, S: list, P: list, E: list, step: int, neighbor_strategy, num_neighbors: int, max_iterations: int):
    t = time.time()
    result = optimization_heuristic_neighbors_exp(F=F, S=S, P=P, E=E, step=step, neighbor_strategy=neighbor_strategy, num_neighbors=num_neighbors, max_iterations=max_iterations)
    return [neighbor_strategy.__name__, num_neighbors, result[1], max_iterations, step, time.time() - t]


def run_heuristic_with_eval_strategy(F: list, S: list, P: list, E: list, step:20, eval_strategy, max_iterations: 10000):
    t = time.time()
    result = optimization_heuristic_eval_exp(F=F, S=S, P=P, E=E, step=step, eval_strategy=eval_strategy, max_iterations=max_iterations)
    return [eval_strategy.__name__, result[1], max_iterations, step, time.time() - t]


def run_heuristic_with_all_strategies(F: list, S: list, P: list, E: list, step: float, neighbor_strategy: callable, eval_strategy: callable, num_neighbors=5, max_iterations=1000):
    t = time.time()
    result = optimization_heuristic_neighbors_eval_exp(F=F, S=S, P=P, E=E, step=step, neighbor_strategy=neighbor_strategy, eval_strategy=eval_strategy, num_neighbors=num_neighbors, max_iterations=max_iterations)
    return [ eval_strategy.__name__, neighbor_strategy.__name__, result[1], num_neighbors, max_iterations, step, time.time() - t]
