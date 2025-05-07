from experiments import neighborhood
from experiments.writeCSV import *


def run_creation_neighbors_experiment(F: list, S:list, P:list, E:list):
    
    dir = "experiments/results/creation_neighbors"
    headers = ["Neighbor strategy", "Num neighbors", "Best Y", "Num. iterations", "Time"]

    neighbor_strategies = neighborhood.get_neighbor_strategies()
    num_neigbors = [2, 4, 8, 16, 32, 64]
    num_iterations = [10000, 100000, 1000000, 10000000]

    for name, func in neighbor_strategies.items():
        print(f"Running strategy: {name}")
        results = []
        results.append(headers)
        for i in range(len(num_iterations)):
            for n in range(len(num_neigbors)):
                result = neighborhood.run_heuristic_with_neighbors_strategy(F=F, S=S, P=P, E=E, neighbor_strategy=func, num_neighbors=num_neigbors[n], max_iterations=num_iterations[i])
                results.append(result[1])

        writeCSV(filename=f"{dir}/results_neighbors_{name}.csv", rows=results)