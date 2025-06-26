#!/usr/bin/env python

import os
import sys
import time
import inspect # Not used in this script?

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../db/')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../models/')))

from experiments.test.heuristic_test_helper import HeuristicTestHelper
from models.hill_climbing import HillClimbing
import setup

import db.config as dbconfig
import db.database as db
import models.model as model
import experiments.initial_x.initial_x as initial_x
import experiments.neighborhood.neighborhood as neighborhood
import json

def create_tables(conn):
    query = """
        create table if not exists experimento_x_inicial (
            id serial primary key,
            x_inicial text,
            step decimal(15, 2),
            cant_iteraciones integer,
            iteracion integer,
            x_optimo text,
            obj decimal(15, 2),
            tiempo decimal(15, 2),
            estrategia text
        );

        create table if not exists experimento_hill_climbing (
            id serial primary key,
            experimento text,
            x_inicial text,
            obj_inicial decimal(15, 2),
            step decimal(15, 2),
            cant_iteraciones integer,
            iteracion integer,
            x_optimo text,
            obj decimal(15, 2),
            tiempo decimal(15, 2),
            motivo_parada text,
            estrategia text,
            distribucion text
        );
        """
    db.execute(conn, query)

    conn.close()
    print("[okay] Connection to supply_chain closed")

def log_x_initial(X, obj, step, max_iterations, it, best_X, best_obj, initial_time, strategy):
    conn = db.get_connection(dbconfig.load_config('../db/database.ini', 'supply_chain'))
    query = f"""
            insert into experimento_x_inicial (
                x_inicial, 
                obj_inicial,
                step,
                cant_iteraciones,
                iteracion,
                x_optimo, 
                obj, 
                tiempo,
                estrategia) 
            values (
                '{json.dumps(X)}',
                {obj:.2f},
                {step:.2f},
                {max_iterations},
                {it},
                '{json.dumps(best_X)}', 
                {best_obj:.2f}, 
                {time.time() - initial_time:.2f}, 
                '{strategy}');
            """
    db.execute(conn, query)
    conn.close()

def get_best_sol(X_list: list, Y_list: list) -> tuple:
    best_X = X_list[0]
    best_Y = Y_list[0]

    for i in range(1, len(X_list)):
        if Y_list[i] > best_Y:
            best_X = X_list[i]
            best_Y = Y_list[i]

    return best_X, best_Y

def optimization_heuristic_initial_x(F: list, S: list, P: list, E: list, step: float, 
                                     initial_obj: tuple, log_f: callable, strategy: str, 
                                     max_iterations: int = 1000) -> dict:
    initial_time = time.time()

    X = initial_obj[0]
    obj = initial_obj[1]

    best_X = X
    best_obj = obj

    it = 0
   
    while it < max_iterations:
        # añadir la mejor manera de obtener los vecinos segun los experimentos
        X_neighbour_1 = [X[i] - step for i in range(len(X))]
        X_neighbour_2 = [X[i] + step for i in range(len(X))]

        obj_1 = model.get_objective_value(F, S, P, E, X_neighbour_1)
        obj_2 = model.get_objective_value(F, S, P, E, X_neighbour_2)

        X_best_neighbour, Y_best_neighbour = get_best_sol([best_X, X_neighbour_1, X_neighbour_2], [best_obj, obj_1, obj_2])

        if X_best_neighbour > best_X and Y_best_neighbour > 0:
            best_X = X_best_neighbour
            best_obj = Y_best_neighbour

            log_f(X, obj, step, max_iterations, it, best_X, best_obj, initial_time, strategy)

        it += 1

    total_time = time.time() - initial_time

    return {
        "X": best_X,
        "Z": best_obj,
        "time": total_time
    }

def log_optimization_heuristic(experiment, X_initial, Z_initial, X, Z, step, it, actual_time, halting_condition, strategy):
    config = dbconfig.load_config('db/database.ini', 'supply_chain')
    conn = db.get_connection(config)

    query = f"""
            insert into experimento_hill_climbing (
                experimento,
                x_inicial, 
                obj_inicial,
                step,
                cant_iteraciones,
                iteracion,
                x_optimo, 
                obj, 
                tiempo,
                motivo_parada,
                estrategia,
                distribucion) 
            values (
                '{experiment}',
                '{json.dumps(X_initial)}',
                {Z_initial:.2f},
                {step:.2f},
                {it},
                {it},
                '{json.dumps(X)}', 
                {Z:.2f}, 
                {actual_time:.2f},
                '{halting_condition}',
                '{strategy}',
                'normal');
            """
    db.execute(conn, query)
    conn.close()

def test(experiment, model, num_iterations, num_step, log_f: callable):
    helper = HeuristicTestHelper()

    results = initial_x.get_possible_X(model)
    results.sort(key=lambda x: x[1], reverse=True)
    X_list, obj_list, strategies = zip(*results)

    print("################ X INICIAL ################")
    for i in range(len(X_list)):
        print(f"X inicial {X_list[i]}, Obj inicial = {obj_list[i]}, Estrategia = {strategies[i]}")

    all_results = {}

    for i in range(len(X_list)):
        for iteration in num_iterations:
            for step in num_step:
                print("################ EXECUTION ################")
                initial_x_exp = X_list[i]
                initial_obj = obj_list[i]
                strategy = strategies[i]

                print(f"Strategy {strategy} running with {iteration} iterations and step {step}")
                print(f"X inicial {initial_x_exp}, Obj inicial = {initial_obj}")

                result = helper.solve(
                    model=model,
                    step=step,
                    initial_x=initial_x_exp,
                    max_iterations_allowed=iteration
                )

                log_f(
                    experiment=experiment,
                    X_initial=initial_x_exp,
                    Z_initial=initial_obj,
                    X=result["X"],
                    Z=result["Z"],
                    step=step,
                    it=result.get("iterations", 0),
                    actual_time=result["time"],
                    halting_condition=result["halting_condition"],
                    strategy=strategy
                )

                all_results[(iteration, step, strategy)] = {
                    "X inicial": initial_x_exp,
                    "Obj inicial": initial_obj,
                    "X": result.get("X"),
                    "Obj": result.get("Z"),
                    "Tiempo": result.get("time"),
                    "Halting Condition": result.get("halting_condition")
                }

                print(f"X {result.get('X')}, Obj = {result.get('Z')}, Tiempo = {result.get('time')}, Halting Condition = {result.get('halting_condition')}")

    print("################ RESULT ################")
    print(all_results)

def main():

    config = dbconfig.load_config('db/database.ini', 'supply_chain')
    
    data = setup.read_database(config)
    F, S, P, E = data["F"], data["S"], data["P"], data["E"]
    print("[okay] Data loaded from database")

    num_iterations = [50] # [100, 10000, 100000]
    num_step = [936]

    model = HillClimbing(F, S, P, E)
    test("test_hill_climbing", model, num_iterations, num_step, log_optimization_heuristic)
    db.dump("db/data/dumps/hill_climbing_test.sql", config)

if __name__ == "__main__":
    main()
