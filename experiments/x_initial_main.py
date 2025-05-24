#!/usr/bin/env python

import os
import sys
import time
import inspect

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../db/')))

import db.config as dbconfig
import db.database as db
import model
import x_initial
import neighborhood

def create_tables():
    conn = db.get_connection(dbconfig.load_config('../db/database.ini', 'supply_chain'))
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

        create table if not exists experimentos_hill_climbing (
            id serial primary key,
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

# ESTA HARDCODEADA LA DISTRIBUCION
def log_optimization_heuristic(X_initial, Z_initial, X, Z, step, it, actual_time, halting_condition, strategy):
    conn = db.get_connection(dbconfig.load_config('../db/database.ini', 'supply_chain'))
    query = f"""
            insert into experimentos_hill_climbing (
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
        log_f: callable,
        strategy: str,
        step: int = 20, # ?
        initial_obj: tuple = (None, None),
        epsilon: float = 1e-12,
        max_iterations_allowed: int = 1e12,
        max_stuck_allowed: int = 1e3) -> dict:

    X_initial, Z_initial = initial_obj

    X_current = X_initial
    Z_current = Z_initial

    it = 0
    stuck = 0

    ####################################################################
    # Criterios de parada
    Z_current_is_better = True
    limit_is_not_reached = True
    is_not_stuck = True
    ####################################################################
    
    initial_time = time.time()

    while Z_current_is_better and limit_is_not_reached and is_not_stuck:
        # first improvement - multi change, con un step 20, 100.000 iteraciones, y 32 vecinos. 
        neighbors = neighborhood.create_exhaustive_neighbors(X_current, step, 32)
        evaluated_neighbors = [(n, model.get_objective_value(F, S, P, E, n)) for n in neighbors]

        # Evaluation of the neighbourhood
        best_n, best_z = neighborhood.greedy_selection_eval(evaluated_neighbors, Z_current)

        # Comparing the best solution with the current one
        if best_n is not None:
            X_current = best_n
            Z_previous = Z_current
            Z_current = best_z

        ################################################################
        # Criterios de parada
        #
        # 1. Número máximo de iteraciones:
        it += 1
        limit_is_not_reached = it < max_iterations_allowed
        #
        # 2. Estancamiento:
        if Z_current == Z_previous:
            stuck += 1
            print(f"[warning] stuck in local optimum {Z_current} for {stuck} iterations")
        elif Z_current > Z_previous:
            stuck = 0
            # 3. Mejora entre las iteraciones
            #
            # Si la mejora es mayor a epsilon, se considera que la
            # solución actual es mejor que la anterior, y se sigue
            # buscando.
            Z_current_is_better = abs(Z_current - Z_previous) > epsilon
        else: # Z_current < Z_previous
            # Este es el caso en el que la solución anterior es mejor.
            # Nosotros usamos greedy local search, por ende, no se
            # debería dar este caso. Pero si se da, es porque la
            # solución anterior es mejor que la actual.
            stuck = 0
            raise Exception(f"?previous objective value {Z_previous} is better than the current one {Z_current}")

        if Z_current < 0:
            print(f"[warning] current objective value is negative: {Z_current}")

        is_not_stuck = stuck < max_stuck_allowed
        ################################################################

    halting_condition = None
    if not Z_current_is_better:
        halting_condition = "Satisfactory solution found"
    elif not limit_is_not_reached:
        halting_condition = "Maximum number of iterations"
    elif not is_not_stuck:
        halting_condition = "Stuck in local optimum"

    actual_time = time.time() - initial_time
    log_f(X_initial, Z_initial, X_current, Z_current, step, it, actual_time, halting_condition, strategy)

    return {
        "X": X_current,
        "Z": Z_current,
        "time": actual_time,
        "halting_condition": halting_condition
    }

def test(F, S, P, E, num_iterations, num_step, heuristic: callable, log_f: callable):
    X_list, obj_list, strategies  = x_initial.get_posible_X_sorted(F, S, P, E)

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
    conn = db.get_connection(dbconfig.load_config('../db/database.ini', 'supply_chain'))

    F = model.read_fabrication_centers(conn)
    S = model.read_distribution_centers(conn)
    P = model.read_points_of_sale(conn)
    E = model.read_scenarios(conn)

    create_tables()
    conn.close()

    num_iterations = [100] # [100, 10000, 100000]
    num_step = [22, 24, 28, 36, 52, 84] # 20 + 2**(i+1)

    # test(F, S, P, E, num_iterations, num_step, optimization_heuristic_initial_x, log_x_initial)
    test(F, S, P, E, num_iterations, num_step, optimization_heuristic, log_optimization_heuristic)

    db.dump("db/data/supply_chain_dump.sql", {
        "user": "postgres",
        "password": "1234"
    })

if __name__ == "__main__":
    main()
