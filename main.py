#!/usr/bin/env python

import time
import sys
import os
import setup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "models/")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "experiments/")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "experiments/initial_x/")))

from hill_climbing import HillClimbing
from random_restart import RandomRestart
from ant_colony import AntColony
import db.config as dbconfig
import initial_x as initial_x

def main() -> None:
    config = dbconfig.load_config('db/database.ini', 'supply_chain')
    ans = input("Do you want to create (c), restore (t) or read (r) database? (c/t/r): ")
    
    if ans == "c":
        setup.create_database(config)
    elif ans == "t":
        setup.restore_database()
    elif ans != "r":
        print("Invalid option. Exiting.")
        sys.exit(1)    
    
    data = setup.read_database(config)
    F, S, P, E = data["F"], data["S"], data["P"], data["E"]
    print("[okay] Data loaded from database")

    t = time.time()

    model = AntColony(F, S, P, E, alpha=0.5, beta=3.0, rho=0.3, num_prod_levels=500)
    result = model.solve(num_ants=100, max_iterations=1000)
    print("############################### RESULTS ################################")
    print("X:", result["X"])
    print("Z:", result["Z"])
    print("Margin:", result["margin"])
    print("pStk:", result["pStk"])
    print("pDIn:", result["pDIn"])
    print("CTf2s:", result["CTf2s"])
    print("CTs2p:", result["CTs2p"])
    print("Iterations:", result.get("iterations"))
    print("Time:", time.time() - t)
    print("Halting condition:", result["halting_condition"])
    print("########################################################################")

    # print("############################### RESULTS ################################")
    # print("X:", result["X"])
    # print("Z:", result["Z"])
    # print("Margin:", result["margin"])
    # print("pStk:", result["pStk"])
    # print("pDIn:", result["pDIn"])
    # print("CTf2s:", result["CTf2s"])
    # print("CTs2p:", result["CTs2p"])
    # print("Iterations:", result.get("iterations"))
    # print("Time:", time.time() - t)
    # print("Halting condition:", result["halting_condition"])
    # print("########################################################################")

    # model = HillClimbing(F, S, P, E)
    # result = model.solve(step=936, initial_X=initial_x.get_initial_X_from_most_probable_scenario(model, F, E), max_iterations_allowed=100)

    # print("############################### RESULTS ################################")
    # print("X:", result["X"])
    # print("Z:", result["Z"])
    # print("Margin:", result["margin"])
    # print("pStk:", result["pStk"])
    # print("pDIn:", result["pDIn"])
    # print("CTf2s:", result["CTf2s"])
    # print("CTs2p:", result["CTs2p"])
    # print("Iterations:", result.get("iterations"))
    # print("Time:", time.time() - t)
    # print("Halting condition:", result["halting_condition"])
    # print("########################################################################")

    # model = RandomRestart(F, S, P, E)
    # result = model.solve(step=936, initial_X=initial_x.get_initial_X_from_most_probable_scenario(model, F, E), max_iterations_allowed=100)

    # print("############################### RESULTS ################################")
    # print("X:", result["X"])
    # print("Z:", result["Z"])
    # print("Margin:", result["margin"])
    # print("pStk:", result["pStk"])
    # print("pDIn:", result["pDIn"])
    # print("CTf2s:", result["CTf2s"])
    # print("CTs2p:", result["CTs2p"])
    # print("Iterations:", result.get("iterations"))
    # print("Time:", time.time() - t)
    # print("Halting condition:", result["halting_condition"])
    # print("########################################################################")

if __name__ == "__main__":
    main()
