#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../db')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../modelo')))
import time
from db.database import *
from experiments.neighborhood import *
from experiments.writeCSV import *
from modelo import *


def main():
    conn = get_connection(load_config('db/database.ini', 'supply_chain'))

    F = read_fabrication_centers(conn)
    S = read_distribution_centers(conn)
    P = read_points_of_sale(conn)
    E = read_scenarios(conn)

    conn.close()
    print("[okay] Connection to supply_chain closed")

    dir = "resultados"
    headers = ["Neighbor strategy", "Num neighbors", "Best Y", "Num. iterations"]
    neighbor_strategies = get_neighbor_strategies()
    num_neigbors = [2, 4, 8, 16, 32, 64]
    num_iterations = [10000, 100000, 1000000, 10000000]
    
    for name, func in neighbor_strategies.items():
        results = []
        results.append(headers)
        for i in range(len(num_iterations)):
            for n in range(len(num_neigbors)):
                result = run_neighbors_experiment(F=F, S=S, P=P, E=E, neighbor_strategy={"name": name, "func":func}, num_neighbors=num_neigbors[n], max_iterations=num_iterations[i])
                results.append(result[1])

        writeCSV(filename=f"{dir}/results_neighbors_{name}.csv", rows=results)

if __name__ == "__main__":
    main()