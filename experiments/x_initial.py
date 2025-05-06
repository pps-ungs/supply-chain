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

    actual_sol = 0
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

def get_initial_X(E: list) -> list:
    scenario = E[0]
    total_demand = sum(scenario['data'].values())
    num_fabrication_centers = len(scenario['data'])
    return [total_demand // num_fabrication_centers for _ in range(num_fabrication_centers)]
