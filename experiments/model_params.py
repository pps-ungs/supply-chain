import os
import sys
import time
import random # Not used in this script?

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../db/')))

import models.model as model
from db.config import *
from db.database import *
import experiments.initial_x.initial_x as initial_x
import neighborhood

def optimization_heuristic_test(
        F: list,
        S: list,
        P: list,
        E: list,
        neighbor_strategy: callable, 
        eval_strategy: callable, 
        step: int = 20, # ?
        epsilon: float = 1e-12,
        x_initial: list = None,
        num_neighbors=5,
        max_iterations_allowed: int = 1e12,
        max_stuck_allowed: int = 1e3) -> list:

    X_initial = x_initial
    Z_initial = model.get_objective_value(F, S, P, E, X_initial)

    X_current = X_initial
    Z_current = Z_initial

    it = 0
    stuck = 0

    ####################################################################
    # Criterios de parada
    Z_current_is_better = True
    limit_is_not_reached = True
    is_not_stuck = True
    ####################################################################

    while Z_current_is_better and limit_is_not_reached and is_not_stuck:
        # first improvement - multi change, con un step 20, 100.000 iteraciones, y 32 vecinos. 
        neighbors = neighbor_strategy(X_current, step, 32)
        evaluated_neighbors = [(n, model.get_objective_value(F, S, P, E, n)) for n in neighbors]

        # Evaluation of the neighbourhood
        best_n, best_z = eval_strategy(evaluated_neighbors, Z_current)

        # Comparing the best solution with the current one
        if best_n is not None:
            X_current = best_n
            Z_previous = Z_current
            Z_current = best_z


        ################################################################
        # Criterios de parada
        #
        # 1. Número máximo de iteraciones:
        it += 1
        limit_is_not_reached = it < max_iterations_allowed
        #
        # 2. Estancamiento:
        if Z_current == Z_previous:
            stuck += 1
            print(f"[warning] stuck in local optimum {Z_current} for {stuck} iterations")
        elif Z_current > Z_previous:
            stuck = 0
            # 3. Mejora entre las iteraciones
            #
            # Si la mejora es mayor a epsilon, se considera que la
            # solución actual es mejor que la anterior, y se sigue
            # buscando.
            Z_current_is_better = abs(Z_current - Z_previous) > epsilon
        else: # Z_current < Z_previous
            # Este es el caso en el que la solución anterior es mejor.
            # Si pasa esto no está claro qué hacer, por el momento, no
            # se hace nada, simplemente continua con la siguiente
            # iteración.
            stuck = 0
            print("[warning] previous objective value is better than the current one")

        if Z_current < 0:
            print(f"[warning] current objective value is negative: {Z_current}")

        is_not_stuck = stuck < max_stuck_allowed
        ################################################################

    halting_condition = None
    if not Z_current_is_better:
        halting_condition = "Satisfactory solution found"
    elif not limit_is_not_reached:
        halting_condition = "Maximum number of iterations"
    elif not is_not_stuck:
        halting_condition = "Stuck in local optimum"

    return [X_current, Z_current] + model.get_objective_function_values(F, S, P, E, X_current) + [halting_condition]

# Mínimo valor de stock inicial para cada centro de fabricación
def get_initial_X_minimal(F: list, min_value: int = 30) -> list:
    return [min_value + i**2 for i in range(len(F))]

# La demanda uniforme de cada centro de fabricación se calcula como la suma de las demandas 
# de todos los escenarios dividida por el número de escenarios.
def get_initial_X_uniform(F: list, E: list) -> list:
    total_demand = sum(sum(d.values()) for d in model.get_demand_per_point_of_sale(E))
    num_fabrication_centers = len(F)
    base_value = total_demand // (num_fabrication_centers * len(E))

    return [base_value + i for i in range(num_fabrication_centers)]

# La demanda promedio de cada centro de fabricación se calcula como la suma de las demandas
# promedio de todos los punto de venta en todos los escenarios dividida por el número de escenarios.
def get_initial_X_average_demand(F: list, E: list) -> list:
    average_demand = {}
    num_scenarios = len(E)

    for scenario in model.get_demand_per_point_of_sale(E):
        for key, value in scenario.items():
            if key not in average_demand:
                average_demand[key] = 0
            average_demand[key] += value

    for key in average_demand:
        average_demand[key] /= num_scenarios

    total_average_demand = sum(average_demand.values())
    num_fabrication_centers = len(F)
    return [total_average_demand // num_fabrication_centers for _ in range(num_fabrication_centers)]


def main():

    ####################################################################
    # Conjuntos
    ####################################################################

    config = load_config('db/database.ini', 'supply_chain')
    conn = get_connection(config)

    F = model.read_fabrication_centers(conn)
    S = model.read_distribution_centers(conn)
    P = model.read_points_of_sale(conn)
    E = model.read_scenarios(conn)

    conn.close()
    print("[okay] Connection to supply_chain closed")

    ####################################################################
    # Params
    ####################################################################

    steps = [10, 20]
    num_neighbors = [32, 16, 64]

    neighbours_strategies = {
        "exhaustive": neighborhood.create_exhaustive_neighbors,
        "multi_change": neighborhood.create_multi_change_neighbors,
    }

    evaluation_strategies = {
        "greedy": neighborhood.greedy_selection_eval,
        "first_improvement": neighborhood.first_improvement_eval,
    }

    num_iterations = [10000, 100000, 1000000, 10000000]

    initial_x_list = [
                        get_initial_X_minimal(F, 50),
                        get_initial_X_minimal(F, 10),
                        get_initial_X_uniform(F, E),
                        get_initial_X_average_demand(F, E)
                    ]

    for n_strategy, f_neighbourhood in neighbours_strategies.items():
        for eval_strategy, f_eval in evaluation_strategies.items():
            for step in steps:
                for n in num_neighbors:
                    for x_initial in initial_x_list:
                        for iterations in num_iterations:
                            print(f"Running strategy: {n_strategy}, eval_strategy: {eval_strategy}, step: {step}, num_neighbors: {n}, x_initial: {x_initial}, iterations: {iterations}")
                            t = time.time()
                            X, Z, margin, pStk, pDIn, CTf2s, CTs2p, halting_condition = optimization_heuristic_test(F, S, P, E, f_neighbourhood, f_eval, step=step, epsilon=1e-12, x_initial=x_initial, num_neighbors=n, max_iterations_allowed=iterations, max_stuck_allowed=1e3)

                            print("############################### RESULTS ################################")
                            print("X:", X)
                            print("Z:", Z) # Objective function value
                            print("Margin:", margin)
                            print("pStk:", pStk)
                            print("pDIn:", pDIn)
                            print("CTf2s:", CTf2s)
                            print("CTs2p:", CTs2p)
                            print("Halting condition:", halting_condition)
                            print("Time:", time.time() - t)
                            print("########################################################################")

if __name__ == "__main__":
    main()
