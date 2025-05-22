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
    base_value = int(total_demand // (num_fabrication_centers * len(E)))

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
    return [int(total_average_demand // num_fabrication_centers) for _ in range(num_fabrication_centers)]

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
    return [int(min_value + (min_value / len(F) * i**2)) for i in range(len(F))]

# Toma las demandas máximas de cada punto de venta y las distribuye uniformemente entre los centros de fabricación.
def get_initial_X_higher_demand(F: list, E: list) -> list:
    total_demand = sum(max(d.values()) for d in model.get_demand_per_point_of_sale(E))
    return [int(total_demand // (len(F) * len(E))) for _ in range(len(F))]

# Genera valores de pseudorandoms basados en la suma de las demandas de todos los escenarios.
def get_initial_X_pseudorandom(F: list, E: list, seed: int = 42) -> list:
    random.seed(seed)
    total_demand = sum(sum(d.values()) for d in model.get_demand_per_point_of_sale(E))

    base_value = total_demand // (len(F) * len(E))
    return [base_value + random.randint(1, 10) for _ in range(len(F))]

# Sensible al costo de un escenario
def get_initial_X_cost_sensitive(F: list, S: list, E: list) -> list:
    # Calculate average cost from each fabrication center to all distribution centers
    avg_costs_f2s = {}
    transportation_costs = model.get_unit_transportation_cost_from_fabrication_to_distribution(F, S)

    for i in range (len(F)):
        total_cost_from_f = 0
        num_s_centers = len(S)

        if num_s_centers > 0:
            for j in range(len(S)):
                total_cost_from_f += transportation_costs[i][j]
            avg_costs_f2s[F[i]['id']] = total_cost_from_f / num_s_centers
        else:
            avg_costs_f2s[F[i]['id']] = 0

    total_demand = sum(model.get_demand_per_point_of_sale(E)[0].values())
    
    inverted_costs = {f_id: 1.0 / (cost + 0.001) for f_id, cost in avg_costs_f2s.items()}
    total_inverted_cost_sum = sum(inverted_costs.values())

    initial_X = []
    if total_inverted_cost_sum > 0:
        for f_center in F:
            f_id = f_center['id']
            production_share = (inverted_costs[f_id] / total_inverted_cost_sum) 
            initial_X.append(int(total_demand * production_share))
    else:
        num_fabrication_centers = len(F)
        initial_X = [total_demand // num_fabrication_centers for _ in range(num_fabrication_centers)]

    return initial_X

# Demanda inicial ponderada por la probabilidad de ocurrencia de cada escenario
# Por ahora da lo mismo que la demanda promedio ya que las probabilidades son equiprobables
def get_initial_X_weighted_by_scenario_prob(F: list, E: list) -> list:
    expected_total_demand = 0
    probabilities = model.get_probability_of_occurrence(E)

    for i, scenario_data in enumerate(model.get_demand_per_point_of_sale(E)):
        scenario_prob = probabilities[i]
        total_demand_in_scenario = sum(scenario_data.values())
        expected_total_demand += total_demand_in_scenario * scenario_prob

    num_fabrication_centers = len(F)
    return [int(expected_total_demand // num_fabrication_centers) for _ in range(num_fabrication_centers)]

def get_initial_X_hybrid_demand_probabilistic(F: list, E: list, min_per_center: int = 10, randomness_range: int = 20) -> list:
    # Calcular la demanda total esperada (considerando probabilidades de escenario)
    expected_total_demand = 0
    probabilities = model.get_probability_of_occurrence(E)
    scenario_demands = model.get_demand_per_point_of_sale(E)

    for i, scenario_data in enumerate(scenario_demands):
        scenario_prob = probabilities[i]
        total_demand_in_scenario = sum(scenario_data.values())
        expected_total_demand += total_demand_in_scenario * scenario_prob

    num_fabrication_centers = len(F)
    
    if num_fabrication_centers == 0:
        return []

    # Calcular un base_value más centrado en la demanda esperada por centro de fabricación
    base_value = int(expected_total_demand // num_fabrication_centers)
    if base_value <= 0: # Asegurar que el valor base no sea cero o negativo
        base_value = 1 # O un valor mínimo razonable

    random.seed(20)
    initial_X = []
    for _ in range(num_fabrication_centers):
        # Añadir un componente aleatorio para variar la producción por centro
        # Puedes ajustar 'randomness_range' para más o menos variación
        variation = random.randint(-randomness_range // 2, randomness_range // 2)
        
        # Asegurar que el valor final sea al menos min_per_center y no negativo
        x_val = max(min_per_center, base_value + variation)
        initial_X.append(x_val)
        
    return initial_X

def get_initial_X_based_on_demand(F: list, E: list) -> list:
    max_demand = max(max(d.values()) for d in model.get_demand_per_point_of_sale(E))
    min_demand = min(min(d.values()) for d in model.get_demand_per_point_of_sale(E))

    initial_x = [max_demand - (min_demand * (i + 1) // len(F)) for i in range(len(F))]
    return initial_x


def get_posible_X_sorted(F: list, S: list, P: list, E: list) -> list:
    minimal_1 = int(sum(model.get_demand_per_point_of_sale(E)[0].values()) / len(F))
    minimal_2 = int(sum(sum(d.values()) for d in model.get_demand_per_point_of_sale(E)) / (len(F) * len(E)))

    max_demand = max(max(d.values()) for d in model.get_demand_per_point_of_sale(E))
    min_demand = min(min(d.values()) for d in model.get_demand_per_point_of_sale(E))
    minimal_3 = max_demand - min_demand

    X_list = [
                    get_initial_X_uniform(F, E),
                    get_initial_X_average_demand(F, E),
                    get_initial_X_from_most_probable_scenario(F, E),
                    get_initial_X_minimal(F, minimal_1),
                    get_initial_X_minimal(F, minimal_2),
                    get_initial_X_minimal(F, minimal_3),
                    get_initial_X_higher_demand(F, E),
                    get_initial_X_pseudorandom(F, E, 200),
                    # get_initial_X_weighted_by_scenario_prob(F, E),
                    get_initial_X_cost_sensitive(F, S, E),
                    get_initial_X_hybrid_demand_probabilistic(F, E, 5000),
                    get_initial_X_based_on_demand(F, E)
                ]
    
    strategies = [
                    "uniform", 
                    "average_demand", 
                    "most_probable_scenario", 
                    f"minimal_1_{minimal_1}",
                    f"minimal_2_{minimal_2}",
                    f"minimal_3_{minimal_3}",
                    "higher_demand", 
                    "pseudorandom",
                    # "weighted_by_scenario_prob",
                    "cost_sensitive",
                    "hybrid_demand_probabilistic",
                    "based_on_demand"
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

def optimization_heuristic_initial_x(F: list, S: list, P: list, E: list, step: float, 
                                     initial_obj: tuple, log_f: callable, strategy: str, 
                                     max_iterations: int = 1000) -> list:
    initial_time = time.time()

    X = initial_obj[0]
    obj = initial_obj[1]

    best_X = X
    best_obj = obj

    it = 0
   
    while it < max_iterations:
        # añadir la mejor manera de obtener los vecinos segun los experimentos
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

    print("################ X INICIAL ################")
    for i in range(len(X_list)):
        print(f"X inicial {X_list[i]}, Obj inicial = {obj_list[i]}, Estrategia = {strategies[i]}")

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
