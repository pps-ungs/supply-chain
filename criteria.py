import random

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
    return neighbors

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

def get_initial_X_minimal(F: list, min_value: int = 30) -> list:
    return [min_value + i**2 for i in range(len(F))]