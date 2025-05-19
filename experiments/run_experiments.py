from experiments import neighborhood
from experiments.writeCSV import *


def run_creation_neighbors_experiment(F: list, S:list, P:list, E:list):
    
    dir = "experiments/results2/creation_neighbors"
    headers = ["Neighbor strategy", "Num neighbors", "Best Y", "Num. iterations", "Step", "Time"]

    neighbor_strategies = neighborhood.get_neighbor_strategies()
    num_neigbors = [2, 4, 8, 16, 32, 64]
    num_iterations = [10000, 100000, 1000000, 10000000]
    num_step = [10, 20, 40, 60, 80, 100]

    for name, func in neighbor_strategies.items():
        print(f"Running strategy: {name}")
        results = []
        results.append(headers)
        for i in range(len(num_iterations)):
            for s in range(len(num_step)):
                for n in range(len(num_neigbors)):
                    result = neighborhood.run_heuristic_with_neighbors_strategy(F=F, S=S, P=P, E=E, step=num_step[s], neighbor_strategy=func, num_neighbors=num_neigbors[n], max_iterations=num_iterations[i])
                    results.append(result)

        writeCSV(filename=f"{dir}/results_neighbors_{name}.csv", rows=results)


def run_eval_neighbors_experiment(F: list, S:list, P:list, E:list):
    
    dir = "experiments/results/evaluation_neighbors"
    headers = ["Evaluation strategy", "Best Y", "Num. iterations", "Step", "Time"]

    eval_strategies = neighborhood.get_eval_strategies()
    num_iterations = [10000, 100000, 1000000, 10000000]
    num_step = [10, 20, 40, 60, 80, 100]

    for name, func in eval_strategies.items():
        print(f"Running strategy: {name}")
        results = []
        results.append(headers)
        for i in range(len(num_iterations)):
            for s in range(len(num_step)):
                result = neighborhood.run_heuristic_with_eval_strategy(F=F, S=S, P=P, E=E, step=num_step[s], eval_strategy=func, max_iterations=num_iterations[i])
                results.append(result)

        writeCSV(filename=f"{dir}/results_neighbors_{name}.csv", rows=results)

def run_creation_aval_neighbors_experiment(F: list, S:list, P:list, E:list):
    
    dir = "experiments/results2/creation_evaluation_neighbors"
    headers = ["Evaluation strategy", "Neighbor strategy", "Best Y", "Num neighbors", "Num. iterations", "Step", "Time"]

    eval_strategies = neighborhood.get_eval_strategies()
    neighbor_strategies = neighborhood.get_neighbor_strategies()
    num_neigbors = [2, 4, 8, 16, 32, 64]
    num_iterations = [10000, 100000, 1000000, 10000000]
    num_step = [10, 20, 40, 60, 80, 100]

    for name_c, func_c in neighbor_strategies.items():
            for name_e, func_e in eval_strategies.items():
                print(f"Running strategy: {name_e} - {name_c}")
                results = []
                results.append(headers)
                for i in range(len(num_iterations)):
                    for s in range(len(num_step)):
                        if name_c != "exhaustive":
                            for n in range(len(num_neigbors)):
                                result = neighborhood.run_heuristic_with_all_strategies(F=F, S=S, P=P, E=E, step=num_step[s], neighbor_strategy=func_c, eval_strategy=func_e, num_neighbors=num_neigbors[n], max_iterations=num_iterations[i])
                                results.append(result)
                        else:
                            result = neighborhood.run_heuristic_with_all_strategies(F=F, S=S, P=P, E=E, step=num_step[s], neighbor_strategy=func_c, eval_strategy=func_e, num_neighbors=0, max_iterations=num_iterations[i])
                            results.append(result)

                writeCSV(filename=f"{dir}/{name_c}/results_neighbors_{name_e}.csv", rows=results)