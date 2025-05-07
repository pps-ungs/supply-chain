import modelo
import variables_de_decision
import validaciones

def optimization_heuristic_initial_x(F: list, S: list, P: list, E: list, step: float, max_iterations: int = 1000) -> list:
    # this should be on the database
    probabilities = modelo.get_probability_of_occurrence(E)

    for i in range(len(E)):
        scenario = E[i]
        scenario["probability"] = probabilities[i]

    E = sorted(E, key=lambda x: x['probability'], reverse=True)

    X = get_initial_X(E)
    Y = modelo.get_objective_value(F, S, P, E, X)

    print("X inicial:", X)
    
    X_best = X
    Y_best = Y

    it = 0

    while it < max_iterations:  # Basic termination condition. fixme with a better one
        # Generating a new solution...
        # X = get_x()       para random restart
        # Y = get_objective_value(F, S, P, E, X)

        # Basic creation of neighbourhood
        X_1 = [X[i] - step for i in range(len(X))]
        X_2 = [X[i] + step for i in range(len(X))]

        # Evaluation of the neighbourhood
        Y_1 = modelo.get_objective_value(F, S, P, E, X_1)
        Y_2 = modelo.get_objective_value(F, S, P, E, X_2)

        X_best_neighbour, Y_best_neighbour = modelo.get_best_sol([X, X_1, X_2], [Y, Y_1, Y_2])

        # Comparing the best solution with the current one
        if X_best_neighbour > X_best and Y_best_neighbour > 0:
            X_best = X_best_neighbour
            Y_best = Y_best_neighbour

        # Shall we stop when we dont find a better solution?
        it += 1

    return [X_best, Y_best] + modelo.get_objective_function_values(F, S, P, E, X_best) + [modelo.get_objective_value(F, S, P, E, X_best)]

def get_initial_X_uniform(F: list, E: list) -> list:
    total_demand = sum(sum(d.values()) for d in modelo.get_demand_per_point_of_sale(E))
    num_fabrication_centers = len(F)
    return [total_demand // num_fabrication_centers for _ in range(num_fabrication_centers)]

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

def get_initial_X_based_on_capacity(F: list, capacities: list, E: list) -> list:
    total_demand = sum(sum(d.values()) for d in modelo.get_demand_per_point_of_sale(E))
    total_capacity = sum(capacities)
    return [int((capacity / total_capacity) * total_demand) for capacity in capacities]

def get_initial_X_from_single_scenario(F: list, E: list) -> list:
    single_scenario = modelo.get_demand_per_point_of_sale(E)[0]  # Usar el primer escenario
    total_demand = sum(single_scenario.values())
    num_fabrication_centers = len(F)
    return [total_demand // num_fabrication_centers for _ in range(num_fabrication_centers)]

def get_initial_X_minimal(F: list, min_value: int = 100) -> list:
    return [min_value for _ in range(len(F))]

def get_posible_X_sorted(F: list, S: list, P: list, E: list) -> list:
    X_list = [  get_initial_X_uniform(F, E), 
                get_initial_X_average_demand(F, E), 
                get_initial_X_based_on_capacity(F, variables_de_decision.get_capacities(F), E), 
                get_initial_X_from_single_scenario(F, E), 
                get_initial_X_minimal(F)    ]
    
    Y_list = [modelo.get_objective_value(F, S, P, E, X) for X in X_list]
    
    pairs_of_X_Y = list(zip(X_list, Y_list))
    pairs_of_X_Y.sort(key=lambda x: x[1], reverse=True)

    X_list = [pair[0] for pair in pairs_of_X_Y]
    Y_list = [pair[1] for pair in pairs_of_X_Y]

    return X_list, Y_list