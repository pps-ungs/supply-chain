#!/usr/bin/env python

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../db/')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../models/')))

from experiments.test.heuristic_test_helper import HeuristicTestHelper
from models.random_restart import RandomRestart
import setup
import json # Not used in this script?

import db.config as dbconfig
import db.database as db
import experiments.initial_x.initial_x as initial_x

def create_tables(config):
    conn = db.get_connection(config)

    query = """
        create table if not exists experimento_random_restart (
            id serial primary key,
            modelo text,
            experimento text,
            x_inicial text,
            obj_inicial decimal(15, 2),
            step decimal(15, 2),
            cant_iteraciones integer,
            iteracion integer,
            cant_iteraciones_sin_mejora_max integer,
            cant_iteraciones_sin_mejora integer,
            cant_reinicios_max integer,
            cant_reinicios integer,
            x_optimo text,
            obj decimal(15, 2),
            tiempo decimal(15, 2),
            motivo_parada text,
            estrategia text,
            distribucion text
        );
        """

    print("[data] Creating tables in database...")
    db.execute(conn, query)
    conn.close()
    print("[okay] Connection to database closed")

def main():

    config = dbconfig.load_config('db/database.ini', 'supply_chain')
    
    data = setup.read_database(config)
    F, S, P, E = data["F"], data["S"], data["P"], data["E"]
    print("[okay] Data loaded from database")

    create_tables(config)
    print("[okay] Tables created in database")  

    num_iterations = [50] # [100, 10000, 100000]
    num_step = [936]

    model = RandomRestart(F, S, P, E)
    
    test_helper = HeuristicTestHelper()
    X = [0 for _ in F]
    Z = model.get_objective_value(F, S, P, E, X)
    
    result = test_helper.solve(
        model=model,
        step=num_step[0],
        initial_obj=(X, Z),
        max_iterations_allowed=num_iterations[0],
        loops_without_improvement=10,
        max_restarts=10
    )

    print(result)

    db.dump("db/data/dumps/random_restart_experiment.sql", config)

if __name__ == "__main__":
    main()
