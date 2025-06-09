#!/usr/bin/env python

import os
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../db")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../modelo")))

import db.config as dbconfig
import db.database as db
import experiments.run_experiments as nh
from experiments.writeCSV import *
import models.model as model
import setup


def main():
    config = dbconfig.load_config('db/database.ini', 'supply_chain')
    
    data = setup.read_database(config)
    F, S, P, E = data["F"], data["S"], data["P"], data["E"]

    dir = "results_new_db/creation_evaluation_neighbors"
    # nh.run_creation_neighbors_experiment(dir=dir, F=F, S=S, P=P, E=E)
    # nh.run_eval_neighbors_experiment(dir=dir, F=F, S=S, P=P, E=E)
    nh.run_creation_eval_neighbors_experiment(dir=dir, F=F, S=S, P=P, E=E)


if __name__ == "__main__":
    main()
