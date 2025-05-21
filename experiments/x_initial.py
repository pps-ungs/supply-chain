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
    X_list = [
                    get_initial_X_uniform(F, E),
                    get_initial_X_average_demand(F, E),
                    get_initial_X_from_most_probable_scenario(F, E),
                    get_initial_X_minimal(F, 10),
                    get_initial_X_minimal(F, 30),
                    get_initial_X_minimal(F, 50),
                    get_initial_X_higher_demand(F, E),
                    get_initial_X_pseudorandom(F, E)
                ]
    
    strategies = [
                    "uniform", 
                    "average_demand", 
                    "most_probable_scenario", 
                    "minimal_10",
                    "minimal_30",
                    "minimal_50", 
                    "higher_demand", 
                    "pseudorandom"
                ]

    obj_list = [model.get_objective_value(F, S, P, E, X) for X in X_list]
    
    pairs_of_X_obj = list(zip(X_list, obj_list, strategies))
    pairs_of_X_obj.sort(key=lambda x: x[1], reverse=True)

    X_list = [pair[0] for pair in pairs_of_X_obj]
    obj_list = [pair[1] for pair in pairs_of_X_obj]
    strategies = [pair[2] for pair in pairs_of_X_obj] 

    return X_list, obj_list, strategies

def get_best_sol(X_list: list, Y_list: list) -> tuple:
    best_X = X_list[0]
    best_Y = Y_list[0]

    for i in range(1, len(X_list)):
        if Y_list[i] > best_Y:
            best_X = X_list[i]
            best_Y = Y_list[i]

    return best_X, best_Y

def log_f(X, obj, step, max_iterations, it, best_X, best_obj, initial_time, strategy):
    conn = get_connection(load_config('db/database.ini', 'supply_chain'))
    query = f"""
            insert into experimentos_x_inicial (
                x_inicial, 
                obj_inicial,
                step,
                cant_iteraciones,
                iteracion,
                x_optimo, 
                obj, 
                tiempo, 
                estrategia) 
            values (
                '{json.dumps(X)}',
                {obj},
                {step},
                {max_iterations},
                {it},
                '{json.dumps(best_X)}', 
                {best_obj}, 
                {time.time() - initial_time:.2f}, 
                '{strategy}');
            """
    execute(conn, query)
    conn.close()

def optimization_heuristic_initial_x(F: list, S: list, P: list, E: list, step: float, initial_obj: tuple, log_f: callable, strategy: str, max_iterations: int = 1000) -> list:
    initial_time = time.time()

    X = initial_obj[0]
    obj = initial_obj[1]

    best_X = X
    best_obj = obj

    it = 0
   
    while it < max_iterations:
        X_neighbour_1 = [X[i] - step for i in range(len(X))]
        X_neighbour_2 = [X[i] + step for i in range(len(X))]

        obj_1 = model.get_objective_value(F, S, P, E, X_neighbour_1)
        obj_2 = model.get_objective_value(F, S, P, E, X_neighbour_2)

        X_best_neighbour, Y_best_neighbour = get_best_sol([best_X, X_neighbour_1, X_neighbour_2], [best_obj, obj_1, obj_2])

        if X_best_neighbour > best_X and Y_best_neighbour > 0:
            best_X = X_best_neighbour
            best_obj = Y_best_neighbour

            # print(f"X = {best_X}, Y = {best_obj}, iteración = {it}, tiempo = {time.time() - initial_time:.2f} segundos")
            log_f(X, obj, step, max_iterations, it, best_X, best_obj, initial_time, strategy)

        it += 1

    total_time = time.time() - initial_time
    return (best_X, best_obj, total_time)

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
            obj_inicial decimal(15, 9),
            step decimal(15, 2),
            cant_iteraciones integer,
            iteracion integer,
            x_optimo text,
            obj decimal(15, 9),
            tiempo decimal(15, 9),
            estrategia text
        );
        """
    execute(conn, query)

    conn.close()
    print("[okay] Connection to supply_chain closed")

    num_iterations = [100, 10000, 100000]
    num_step = [0.05, 0.5, 1, 5, 10, 20, 40, 60, 80, 100]
    X_list, obj_list, strategies  = get_posible_X_sorted(F, S, P, E)

    results = {}

    for i in range(len(X_list)):
        for iteration in num_iterations:
            for step in num_step:
                print("################ EXECUTION ################")
                
                initial_x = X_list[i]
                initial_obj = obj_list[i]
                strategy = strategies[i]

                print(f"Strategy {strategy} running with {iteration} iterations and step {step}")
                print(f"X inicial {initial_x}, Obj inicial = {initial_obj}")

                result = optimization_heuristic_initial_x(F, S, P, E, step=step, initial_obj=(initial_x, initial_obj), log_f=log_f, strategy=strategy, max_iterations=iteration)
                print(f"Sol X = {result[0]}, Obj = {result[1]}, tiempo = {result[2]:.2f} segundos")

                results[(iteration, step, strategy)] = {
                    "X inicial": initial_x,
                    "Obj inicial": initial_obj,
                    "X": result[0],
                    "Obj": result[1],
                    "Tiempo": result[2]
                }

    print("################ RESULT ################")
    print(results)

if __name__ == "__main__":
    main()
