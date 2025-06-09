#!/usr/bin/env python

import os
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../db")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../models")))

import db.config as dbconfig
import experiments.run_experiments as nh
import setup
import models.hill_climbing as hill_climbing


def main():
    config = dbconfig.load_config('db/database.ini', 'supply_chain')
    
    data = setup.read_database(config)
    F, S, P, E = data["F"], data["S"], data["P"], data["E"]

    model = hill_climbing.HillClimbing(F, S, P, E)

    dir = "results_new_db/creation_evaluation_neighbors"
    # nh.run_creation_neighbors_experiment(dir=dir, model=model)
    # nh.run_eval_neighbors_experiment(dir=dir, model=model)
    nh.run_creation_eval_neighbors_experiment(dir=dir, model=model)


if __name__ == "__main__":
    main()
