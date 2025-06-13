#!/usr/bin/env python

import os
import sys
import time
import inspect

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../db/')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../models/')))

from experiments.test.heuristic_test_helper import HeuristicTestHelper
from random_restart import RandomRestart
import setup

import db.config as dbconfig
import db.database as db
import models.model as model
import experiments.initial_x.initial_x as initial_x
import neighborhood
import json


def main():

    config = dbconfig.load_config('db/database.ini', 'supply_chain')
    
    data = setup.read_database(config)
    F, S, P, E = data["F"], data["S"], data["P"], data["E"]
    print("[okay] Data loaded from database")

    num_iterations = [50] # [100, 10000, 100000]
    num_step = [936]

    model = RandomRestart(F, S, P, E)
    
    test_helper = HeuristicTestHelper(dbconfig_path='db/database.ini', database_name='supply_chain')
    X = initial_x.get_initial_X_from_most_probable_scenario(model, F, E)
    Z = model.get_objective_value(F, S, P, E, X)
    
    result = test_helper.solve(
        model=model,
        experiment="x_from_most_probable_scenario",
        strategy="random_restart",
        step=num_step[0],
        initial_obj=(X, Z),
        max_iterations_allowed=num_iterations[0],
        loops_without_improvement=10,
        max_restarts=10
    )
    print(result)

    db.dump("db/data/supply_chain_xime.sql", config)

if __name__ == "__main__":
    main()