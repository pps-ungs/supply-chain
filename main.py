#!/usr/bin/env python

import time
import sys
import os
import setup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "models/")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "experiments/")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "experiments/initial_x/")))

from models.hill_climbing import HillClimbing
from models.random_restart import RandomRestart
from models.ant_colony import AntColony
import db.config as dbconfig
import experiments.initial_x.initial_x as initial_x

def main() -> None:
    ################################################################################
    # All the parameters for the experiments are defined here.
    ################################################################################
    # Parameters ACO
    num_ants        = 100
    max_iterations  = 1000
    alpha           = 0.5
    beta            = 3.0
    rho             = 0.1
    num_prod_levels = 200
    ################################################################################
    # Parameters Hill Climbing
    hill_climbing_step           = 936
    hill_climbing_max_iterations = 45
    ################################################################################
    # Parameters Random Restart
    random_restart_step           = 936
    random_restart_max_iterations = 45
    random_restart_max_loops_without_improvement = 10
    random_restart_max_restarts = 10
    ################################################################################

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

    model = AntColony(F, S, P, E, alpha, beta, rho, num_prod_levels)

    print("################################################################################")
    print("    Experiment **ANT COLONY OPTIMIZATION**")
    print("--------------------------------------------------------------------------------")
    print("PARAMETERS")
    print(f"    alpha: {model.alpha}, beta: {model.beta}, rho: {model.rho}, num_prod_levels: {model.num_prod_levels}")
    print("--------------------------------------------------------------------------------")

    result = model.solve(num_ants, max_iterations)
    
    print("RESULTS")
    print("                X:", result["X"])
    print("                Z:", result["Z"])
    print("           Margin:", result["margin"])
    print("             pStk:", result["pStk"])
    print("             pDIn:", result["pDIn"])
    print("            CTf2s:", result["CTf2s"])
    print("            CTs2p:", result["CTs2p"])
    print("       Iterations:", result.get("iterations"))
    print("             Time:", time.time() - t)
    print("Halting condition:", result["halting_condition"])
    print("################################################################################", "\n")

    model = HillClimbing(F, S, P, E)
    hill_climbing_initial_x = initial_x.get_initial_X_from_most_probable_scenario(model, F, E)

    print("################################################################################")
    print("    Experiment **HILL CLIMBING**")
    print("--------------------------------------------------------------------------------")
    print("PARAMETERS")
    print(f"    step: {hill_climbing_step}, initial_X: {hill_climbing_initial_x}, max_iterations_allowed: {hill_climbing_max_iterations}")
    print("--------------------------------------------------------------------------------")

    result = model.solve(step=hill_climbing_step, initial_X=hill_climbing_initial_x, max_iterations_allowed=hill_climbing_max_iterations)

    print("RESULTS")
    print("                X:", result["X"])
    print("                Z:", result["Z"])
    print("           Margin:", result["margin"])
    print("             pStk:", result["pStk"])
    print("             pDIn:", result["pDIn"])
    print("            CTf2s:", result["CTf2s"])
    print("            CTs2p:", result["CTs2p"])
    print("       Iterations:", result.get("iterations"))
    print("             Time:", time.time() - t)
    print("Halting condition:", result["halting_condition"])
    print("################################################################################", "\n")

    model = RandomRestart(F, S, P, E)

    print("################################################################################")
    print("    Experiment **RANDOM RESTART**")
    print("--------------------------------------------------------------------------------")
    print("PARAMETERS")
    print(f"    step: {random_restart_step}, max_iterations_allowed: {random_restart_max_iterations}")
    print("--------------------------------------------------------------------------------")

    result = model.solve(step=random_restart_step, max_iterations_allowed=random_restart_max_iterations, max_loops_without_improvement=random_restart_max_loops_without_improvement, max_restarts=random_restart_max_restarts)

    print("RESULTS")
    print("                X:", result["X"])
    print("                Z:", result["Z"])
    print("           Margin:", result["margin"])
    print("             pStk:", result["pStk"])
    print("             pDIn:", result["pDIn"])
    print("            CTf2s:", result["CTf2s"])
    print("            CTs2p:", result["CTs2p"])
    print("       Iterations:", result.get("iterations"))
    print("             Time:", time.time() - t)
    print("Halting condition:", result["halting_condition"])
    print("################################################################################", "\n")
    print("Successfully completed all experiments.")

if __name__ == "__main__":
    main()
