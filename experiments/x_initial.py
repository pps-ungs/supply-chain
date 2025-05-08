import os, sys, time, random

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../db/')))
import modelo

from db.config import *
from db.database import *

# La demanda uniforme de cada centro de fabricacion se calcula como la suma de las demandas 
# de todos los escenarios dividida por el número de escenarios.
def get_initial_X_uniform(F: list, E: list) -> list:
    total_demand = sum(sum(d.values()) for d in modelo.get_demand_per_point_of_sale(E))
    num_fabrication_centers = len(F)
    base_value = total_demand // (num_fabrication_centers * len(E))

    return [base_value + i for i in range(num_fabrication_centers)]

# La demanda promedio de cada centro de fabricacion se calcula como la suma de las demandas
# promedio de todos los punto de venta en todos los escenarios dividida por el número de escenarios.
def get_initial_X_average_demand(F: list, E: list) -> list:
    average_demand = {}
    num_scenarios = len(E)

    for scenario in modelo.get_demand_per_point_of_sale(E):
        for key, value in scenario.items():
            if key not in average_demand:
                average_demand[key] = 0
            average_demand[key] += value

    for key in average_demand:
        average_demand[key] /= num_scenarios

    total_average_demand = sum(average_demand.values())
    num_fabrication_centers = len(F)
    return [total_average_demand // num_fabrication_centers for _ in range(num_fabrication_centers)]

# La demanda de cada centro de fabricacion se calcula como la suma de las demandas
# Del escenario más probable
def get_initial_X_from_most_probable_scenario(F: list, E: list) -> list:
    probabilities = modelo.get_probability_of_occurrence(E)

    for i in range(len(E)):
        scenario = E[i]
        scenario["probability"] = probabilities[i]

    E = sorted(E, key=lambda x: x['probability'], reverse=True)

    single_scenario = modelo.get_demand_per_point_of_sale(E)[0] # Escenario más probable
    total_demand = sum(single_scenario.values())
    num_fabrication_centers = len(F)

    return [total_demand // num_fabrication_centers for _ in range(num_fabrication_centers)]

# Mínimo valor de stock inicial para cada centro de fabricacion
def get_initial_X_minimal(F: list, min_value: int = 100) -> list:
    return [min_value for _ in range(len(F))]

# Toma las demandas máximas de cada punto de venta y las distribuye uniformemente entre los centros de fabricación.
def get_initial_X_higher_demand(F: list, E: list) -> list:
    total_demand = sum(max(d.values()) for d in modelo.get_demand_per_point_of_sale(E))
    return [total_demand // (len(F) * len(E)) for _ in range(len(F))]

# Genera valores de pseudorandoms basados en la suma de las demandas de todos los escenarios.
def get_initial_X_pseudorandom(F: list, E: list, seed: int = 42) -> list:
    random.seed(seed)
    total_demand = sum(sum(d.values()) for d in modelo.get_demand_per_point_of_sale(E))

    base_value = total_demand // (len(F) * len(E))
    return [base_value + random.randint(1, 10) for _ in range(len(F))]

def get_posible_X_sorted(F: list, S: list, P: list, E: list) -> list:
    X_list = [  get_initial_X_uniform(F, E), 
                get_initial_X_average_demand(F, E),
                get_initial_X_from_most_probable_scenario(F, E), 
                get_initial_X_minimal(F),
                get_initial_X_higher_demand(F, E),
                get_initial_X_pseudorandom(F, E)    ]
    
    strategies = ["uniform", "average_demand", "most_probable_scenario", "minimal", "higher_demand", "pseudorandom"]

    Y_list = [modelo.get_objective_value(F, S, P, E, X) for X in X_list]
    
    pairs_of_X_Y = list(zip(X_list, Y_list, strategies))
    pairs_of_X_Y.sort(key=lambda x: x[1], reverse=True)

    X_list = [pair[0] for pair in pairs_of_X_Y]
    Y_list = [pair[1] for pair in pairs_of_X_Y]
    strategies = [pair[2] for pair in pairs_of_X_Y] 

    return X_list, Y_list, strategies

def optimization_heuristic_initial_x(F: list, S: list, P: list, E: list, step: float, max_iterations: int = 1000) -> list:
    X_list, Y_list, strategies = get_posible_X_sorted(F, S, P, E)
    results = []

    print("X iniciales:", X_list)
    print("Y iniciales:", Y_list)
    print("Estrategias:", strategies)

    for i in range(len(X_list)):
        initial_time = time.time()

        X = X_list[i]
        Y = Y_list[i]

        X_best = X
        Y_best = Y

        it = 0
        print(f"Iteración {i}: X = {X_best}, Y = {Y_best}")

        while it < max_iterations:
            X_1 = [X[i] - step for i in range(len(X))]
            X_2 = [X[i] + step for i in range(len(X))]

            Y_1 = modelo.get_objective_value(F, S, P, E, X_1)
            Y_2 = modelo.get_objective_value(F, S, P, E, X_2)

            X_best_neighbour, Y_best_neighbour = modelo.get_best_sol([X, X_1, X_2], [Y, Y_1, Y_2])

            if X_best_neighbour > X_best and Y_best_neighbour > 0:
                X_best = X_best_neighbour
                Y_best = Y_best_neighbour

            it += 1
        
        total_time = time.time() - initial_time
        results.append((X_best, Y_best, total_time))
    
    complete_results = {}
    for i in range(len(X_list)):
        X = X_list[i]
        Y = Y_list[i]
        strategy = strategies[i]
        result = results[i]
        
        complete_results[X] = {
            "Y": Y,
            "best_X": result[0],
            "best_Y": result[1],
            "time": result[2],
            "strategy": strategy
        }

    return complete_results

def main():
    ####################################################################
    # Conjuntos
    ####################################################################

    conn = get_connection(load_config('db/database.ini', 'supply_chain'))

    F = modelo.read_fabrication_centers(conn)
    S = modelo.read_distribution_centers(conn)
    P = modelo.read_points_of_sale(conn)
    E = modelo.read_scenarios(conn)

    conn.close()
    print("[okay] Connection to supply_chain closed")

    results = optimization_heuristic_initial_x(F, S, P, E, step=5, max_iterations=1000000)
    print("################ RESULT ################")
    print(results)

    print("################ DB ################")
    conn = get_connection(load_config('db/database.ini', 'supply_chain'))
    
    query = """
            create table if not exists experimentos_x_inicial (
                id serial primary key,
                x_inicial decimal(10, 4),
                y_inicial decimal(10, 4),
                x_optimo decimal(10, 4),
                y_optimo decimal(10, 4),
                tiempo timestamp,
                estrategia text
            );
            """
    
    for x, result in results.items():
        query += f"""
            insert into experimentos_x_inicial (x_inicial, y_inicial, x_optimo, y_optimo, tiempo, estrategia) 
            values ({x}, {result['Y']}, {result['best_X']}, {result['best_Y']}, {result['time']}, {{result['strategy']}});
            """
    
    execute(conn, query)
    conn.close()
    print("[okay] Connection to supply_chain closed")

if __name__ == "__main__":
    main()
