#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../db')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../modelo')))
import time
from db.database import *
from experiments.neighborhood import *
from modelo import *


def main():
    conn = get_connection(load_config('db/database.ini', 'supply_chain'))

    F = read_fabrication_centers(conn)
    S = read_distribution_centers(conn)
    P = read_points_of_sale(conn)
    E = read_scenarios(conn)

    conn.close()
    print("[okay] Connection to supply_chain closed")

    strategies = {
        "one_change": create_neighbors_one_change,
        "exhaustive": create_all_neighbors,
        "multi_change": create_multi_change_neighbors,
    }

    for name, func in strategies.items():
        t = time.time()
        print(f"Running strategy: {name}")
        result = optimization_heuristic_neighbor(F=F, S=S, P=P, E=E, step=5, neighbor_func=func, num_neighbors=10, max_iterations=1000000)
        print(result)
        print(f"Best Y: {result[1]}")
        print(f"Time: {time.time() - t}")


if __name__ == "__main__":
    main()