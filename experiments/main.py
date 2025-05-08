#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../db')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../modelo')))

from db.database import *
from modelo import *
from experiments.run_experiments import *

def main():
    conn = get_connection(load_config('db/database.ini', 'supply_chain'))

    F = read_fabrication_centers(conn)
    S = read_distribution_centers(conn)
    P = read_points_of_sale(conn)
    E = read_scenarios(conn)

    conn.close()
    print("[okay] Connection to supply_chain closed")

    # run_creation_neighbors_experiment(F=F, S=S, P=P, E=E)
    # run_eval_neighbors_experiment(F=F, S=S, P=P, E=E)
    run_creation_aval_neighbors_experiment(F=F, S=S, P=P, E=E)



if __name__ == "__main__":
    main()
