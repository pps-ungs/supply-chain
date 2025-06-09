#!/usr/bin/env python

import os
import sys
import time
import inspect

from models.hill_climbing import HillClimbing

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../db/')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/')))

import db.config as dbconfig
import db.database as db
import models.model as model
import experiments.initial_x as initial_x
import neighborhood
import json

def create_tables():
    conn = db.get_connection({
        "user": "postgres",
        "password": "",
        "dbname": "supply_chain"
    })
    query = """
        create table if not exists x_inicial (
            id serial primary key,
            x_inicial text,
            obj_inicial decimal(15, 9),
            estrategia text
        );

        create table if not exists experimentos_x_inicial (
            id serial primary key,
            id_x_inicial integer references x_inicial(id),
            step decimal(15, 2),
            cant_iteraciones integer,
            iteracion integer,
            x_optimo text,
            obj decimal(15, 2),
            tiempo decimal(15, 2)
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
            insert into experimentos_x_inicial (
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

            # print(f"X = {best_X}, Y = {best_obj}, iteración = {it}, tiempo = {time.time() - initial_time:.2f} segundos")
            log_f(X, obj, step, max_iterations, it, best_X, best_obj, initial_time, strategy)

        it += 1

    total_time = time.time() - initial_time

    return {
        "X": best_X,
        "Z": best_obj,
        "time": total_time
    }

def log_optimization_heuristic(experiment, X_initial, Z_initial, X, Z, step, it, actual_time, halting_condition, strategy):
    conn = db.get_connection({
        "user": "postgres",
        "password": "",
        "dbname": "supply_chain"
    })
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

def optimization_heuristic(
        F: list,
        S: list,
        P: list,
        E: list,
        experiment: str,
        log_f: callable,
        strategy: str,
        step: int = 20, # ?
        initial_obj: tuple = (None, None),
        epsilon: float = 1e-12,
        max_iterations_allowed: int = 1e12,
        max_stuck_allowed: int = 1e3) -> dict:
    
    intial_time = time.time()
    
    model = HillClimbing(F, S, P, E)
    result = model.solve(
        step=step,
        epsilon=epsilon,
        max_iterations_allowed=max_iterations_allowed,
        max_stuck_allowed=max_stuck_allowed,
        initial_X = initial_obj[0]
    )

    actual_time = time.time() - intial_time
    
    X = result["X"]
    Z = result["Z"]
    halting_condition = result.get("halting_condition", "unknown")
    
    log_f(
        experiment=experiment,
        X_initial=initial_obj[0],
        Z_initial=initial_obj[1],
        X=X,
        Z=Z,
        step=step,
        it=result.get("iterations", 0),
        actual_time=actual_time,
        halting_condition=halting_condition,
        strategy=strategy
    )

    return {
        "X": X,
        "Z": Z,
        "time": actual_time,
        "halting_condition": halting_condition
    }

def test(experiment, F, S, P, E, num_iterations, num_step, heuristic: callable, log_f: callable):
    X_list, obj_list, strategies  = initial_x.get_posible_X_sorted(F, S, P, E)

    print("################ X INICIAL ################")
    for i in range(len(X_list)):
        print(f"X inicial {X_list[i]}, Obj inicial = {obj_list[i]}, Estrategia = {strategies[i]}")

    results = {}

    for i in range(len(X_list)):
        for iteration in num_iterations:
            for step in num_step:
                print("################ EXECUTION ################")
                initial_x = X_list[i]
                initial_obj = obj_list[i]
                strategy = strategies[i]

                print(f"Strategy {strategy} running with {iteration} iterations and step {step}")
                print(f"X inicial {initial_x}, Obj inicial = {initial_obj}")

                # Detecta los argumentos de la función
                params = inspect.signature(heuristic).parameters

                kwargs = {
                    "F": F,
                    "S": S,
                    "P": P,
                    "E": E,
                    "step": step,
                    "initial_obj": (initial_x, initial_obj),
                }
                # Agrega los argumentos opcionales según corresponda
                if "log_f" in params:
                    kwargs["log_f"] = log_f
                if "strategy" in params:
                    kwargs["strategy"] = strategy
                if "max_iterations" in params:
                    kwargs["max_iterations"] = iteration
                if "max_iterations_allowed" in params:
                    kwargs["max_iterations_allowed"] = iteration
                if "experiment" in params:
                    kwargs["experiment"] = experiment

                result = heuristic(**kwargs)

                results[(iteration, step, strategy)] = {
                    "X inicial": initial_x,
                    "Obj inicial": initial_obj,
                    "X": result.get("X"),
                    "Obj": result.get("Z"),
                    "Tiempo": result.get("time"),
                    "Halting Condition": result.get("halting_condition") if "halting_condition" in result else None
                }

                print(f"X {result.get('X')}, Obj = {result.get('Z')}, Tiempo = {result.get('time')}, Halting Condition = {result.get('halting_condition') if 'halting_condition' in result else None}")

    print("################ RESULT ################")
    print(results)

def main():
    conn = db.get_connection({
        "user": "postgres",
        "password": "",
        "dbname": "supply_chain"
    })

    F = model.read_fabrication_centers(conn)
    S = model.read_distribution_centers(conn)
    P = model.read_points_of_sale(conn)
    E = model.read_scenarios(conn)

    create_tables()
    conn.close()

    num_iterations = [100] # [100, 10000, 100000]
    num_step = [936, 939, 940]

    test("multi_change_900_step", F, S, P, E, num_iterations, num_step, optimization_heuristic, log_optimization_heuristic)
    # test("100_it_all_x", F, S, P, E, num_iterations, num_step, optimization_heuristic, log_optimization_heuristic)

    db.dump("db/data/supply_chain_dump.sql", {
        "user": "postgres",
        "password": ""
    })

if __name__ == "__main__":
    main()
