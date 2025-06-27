#!/usr/bin/env python

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../db/')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../models/')))

from experiments.test.heuristic_test_helper import HeuristicTestHelper
from models.random_restart import RandomRestart
import setup

import db.config as dbconfig
import db.database as db
import json

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

def log_random_restart(experiment, strategy, step, max_iterations_allowed, max_loops_without_improvement, max_restarts, result):
    config = dbconfig.load_config('db/database.ini', 'supply_chain')
    conn = db.get_connection(config)

    query = f"""
        insert into experimento_random_restart 
        values (
            default,
            'RandomRestart',
           '{experiment}',
           '{json.dumps(result["initial_X"])}',
            {result["initial_Z"]:.2f},
            {step:.2f},
            {max_iterations_allowed},
            {result["iterations"]},
            {max_loops_without_improvement},
            {result["loops_without_improvement"]},
            {max_restarts},
            {result["amount_of_restarts"]},
            '{json.dumps(result["X"])}',
            {result["Z"]:.2f},
            {result["time"]:.2f},
            '{result["halting_condition"]}',
            '{strategy}',
            'normal'
        );
        """

    print("[data] Creating tables in database...")
    db.execute(conn, query)
    conn.close()
    print("[okay] Connection to database closed")

def test(experiment, strategy, model, iterations, steps, max_loops_without_improvement_list, max_restarts_list, log_f: callable):
    test_helper = HeuristicTestHelper()
    all_results = {}

    for step in steps:
        for it in iterations:
            for max_loops_without_improvement in max_loops_without_improvement_list:
                for max_restarts in max_restarts_list:
                    result = test_helper.solve(
                        model=model,
                        step=step,
                        max_iterations_allowed=it,
                        max_loops_without_improvement=max_loops_without_improvement,
                        max_restarts=max_restarts,
                        get_history=True,
                    )

                    all_results[(it, step, strategy)] = {
                        "X": result.get("X"),
                        "Obj": result.get("Z"),
                        "Tiempo": result.get("time"),
                        "Halting Condition": result.get("halting_condition")
                    }

                    print(f"X: {result.get('X')}, Z: {result.get('Z')}, Time: {result.get('time')}, Halting Condition: {result.get('halting_condition')}")

                    history = result.get("history", [])
                    for entry in history:
                        log_f(
                            experiment=experiment,
                            strategy=strategy,
                            step=step,
                            max_iterations_allowed=it,
                            max_loops_without_improvement=max_loops_without_improvement,
                            max_restarts=max_restarts,
                            result=entry
                        )
    return all_results

def main():
    # Load the database configuration & read the data
    config = dbconfig.load_config('db/database.ini', 'supply_chain')
    data = setup.read_database(config)

    F, S, P, E = data["F"], data["S"], data["P"], data["E"]
    print("[okay] Data loaded from database")

    # Uncomment the following line to create the tables in the database
    # create_tables(config)

    # Define the parameters for the random restart experiment
    iterations = [50]
    steps = [936]
    max_loops_without_improvement_list = [10]
    max_restarts_list = [30]
    experiment = "random_restart_experiment"
    strategy = "random_restart"

    # Execute the random restart experiment
    model = RandomRestart(F, S, P, E)
    results = test(
        experiment=experiment,
        strategy=strategy,
        model=model,
        iterations=iterations,
        steps=steps,
        max_loops_without_improvement_list=max_loops_without_improvement_list,
        max_restarts_list=max_restarts_list,
        log_f=log_random_restart
    )

    print("################ RESULT ################")
    print(results)

    # Uncomment the following line to dump the database after running the experiment
    # db.dump("db/data/dumps/random_restart_experiment.sql", config)

if __name__ == "__main__":
    main()
