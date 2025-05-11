import datetime
import os, sys, time, random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../db/')))
import model
from db.config import *
from db.database import *

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

# La demanda de cada centro de fabricación se calcula como la suma de las demandas
# Del escenario más probable
def get_initial_X_from_most_probable_scenario(F: list, E: list) -> list:
    probabilities = model.get_probability_of_occurrence(E)

    for i in range(len(E)):
        scenario = E[i]
        scenario["probability"] = probabilities[i]

    E = sorted(E, key=lambda x: x['probability'], reverse=True)

    single_scenario = model.get_demand_per_point_of_sale(E)[0] # Escenario más probable
    total_demand = sum(single_scenario.values())
    num_fabrication_centers = len(F)

    return [total_demand // num_fabrication_centers for _ in range(num_fabrication_centers)]

# Mínimo valor de stock inicial para cada centro de fabricación
def get_initial_X_minimal(F: list, min_value: int = 30) -> list:
    return [min_value + i**2 for i in range(len(F))]

# Toma las demandas máximas de cada punto de venta y las distribuye uniformemente entre los centros de fabricación.
def get_initial_X_higher_demand(F: list, E: list) -> list:
    total_demand = sum(max(d.values()) for d in model.get_demand_per_point_of_sale(E))
    return [total_demand // (len(F) * len(E)) for _ in range(len(F))]

# Genera valores de pseudorandoms basados en la suma de las demandas de todos los escenarios.
def get_initial_X_pseudorandom(F: list, E: list, seed: int = 42) -> list:
    random.seed(seed)
    total_demand = sum(sum(d.values()) for d in model.get_demand_per_point_of_sale(E))

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

    Y_list = [model.get_objective_value(F, S, P, E, X) for X in X_list]
    
    pairs_of_X_Y = list(zip(X_list, Y_list, strategies))
    pairs_of_X_Y.sort(key=lambda x: x[1], reverse=True)

    X_list = [pair[0] for pair in pairs_of_X_Y]
    Y_list = [pair[1] for pair in pairs_of_X_Y]
    strategies = [pair[2] for pair in pairs_of_X_Y] 

    return X_list, Y_list, strategies

def optimization_heuristic_initial_x(F: list, S: list, P: list, E: list, step: float, max_iterations: int = 1000) -> list:
    X_list, Y_list, strategies = get_posible_X_sorted(F, S, P, E)
    results = []

    conn = get_connection(load_config('db/database.ini', 'supply_chain'))
    for i in range(len(X_list)):
        initial_time = time.time()

        X = X_list[i]
        Y = Y_list[i]

        X_best = X
        Y_best = Y

        it = 0
        print(f"X inicial {X_best}, Y = {Y_best}")

        while it < max_iterations:
            X_1 = [X[i] - step for i in range(len(X))]
            X_2 = [X[i] + step for i in range(len(X))]

            Y_1 = model.get_objective_value(F, S, P, E, X_1)
            Y_2 = model.get_objective_value(F, S, P, E, X_2)

            X_best_neighbour, Y_best_neighbour = model.get_best_sol([X, X_1, X_2], [Y, Y_1, Y_2])

            if X_best_neighbour > X_best and Y_best_neighbour > 0:
                X_best = X_best_neighbour
                Y_best = Y_best_neighbour
                
                query = f"""
                            insert into experimentos_x_inicial (
                                x_inicial, 
                                y_inicial,
                                step,
                                cant_iteraciones,
                                x_optimo, 
                                y_optimo, 
                                tiempo, 
                                estrategia) 
                            values (
                                '{json.dumps(X)}',
                                {Y},
                                {step},
                                {max_iterations},
                                '{json.dumps(X_best)}', 
                                {Y_best}, 
                                {time.time() - initial_time:.2f}, 
                                '{strategies[i]}');
                            """
                execute(conn, query)

            it += 1

        total_time = time.time() - initial_time
        print(f"Sol X = {X_best}, Y = {Y_best}, tiempo = {total_time:.2f} segundos")
        results.append((X_best, Y_best, total_time))

    conn.close()
    print("[okay] Connection to supply_chain closed")
    
    complete_results = {}
    for i in range(len(X_list)):
        X = X_list[i]
        Y = Y_list[i]
        strategy = strategies[i]
        result = results[i]
        
        complete_results[i] = {
            "X": X,
            "Y": Y,
            "nuevo_X": result[0],
            "nuevo_Y": result[1],
            "time": result[2],
            "strategy": strategy
        }

    return complete_results

def main():
    conn = get_connection(load_config('db/database.ini', 'supply_chain'))

    F = model.read_fabrication_centers(conn)
    S = model.read_distribution_centers(conn)
    P = model.read_points_of_sale(conn)
    E = model.read_scenarios(conn)

    query = """
        create table if not exists experimentos_x_inicial (
            id serial primary key,
            x_inicial text,
            y_inicial decimal(15, 9),
            step decimal(15, 2),
            cant_iteraciones integer,
            x_optimo text,
            y_optimo decimal(15, 9),
            tiempo decimal(15, 9),
            estrategia text
        );
        """
    execute(conn, query)

    conn.close()
    print("[okay] Connection to supply_chain closed")

    num_iterations = [100, 10000, 100000, 1000000, 10000000]
    num_step = [0.05, 0.5, 1, 5, 10, 20, 40, 60, 80, 100]

    for iteration in num_iterations:
        for step in num_step:
            print("################ EXECUTION ################")
            print(f"Running with {iteration} iterations and step {step}")

            results = optimization_heuristic_initial_x(F, S, P, E, step=step, max_iterations=iteration)
            
            print("################ RESULT ################")
            print(results)

if __name__ == "__main__":
    main()
