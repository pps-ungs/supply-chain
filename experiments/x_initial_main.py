import os, sys, time, datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../db/')))
from db.config import *
from db.database import *
import model, x_initial

def get_best_sol(X_list: list, Y_list: list) -> tuple:
    best_X = X_list[0]
    best_Y = Y_list[0]

    for i in range(1, len(X_list)):
        if Y_list[i] > best_Y:
            best_X = X_list[i]
            best_Y = Y_list[i]

    return best_X, best_Y

def create_tables():
    conn = get_connection(load_config('db/database.ini', 'supply_chain'))
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
            obj decimal(15, 9),
            tiempo decimal(15, 9)
        );
        """
    execute(conn, query)

    conn.close()
    print("[okay] Connection to supply_chain closed")

def log_x_initial(X, obj, step, max_iterations, it, best_X, best_obj, initial_time, strategy):
    conn = get_connection(load_config('db/database.ini', 'supply_chain'))
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
                {obj},
                {step},
                {max_iterations},
                {it},
                '{json.dumps(best_X)}', 
                {best_obj}, 
                {time.time() - initial_time:.2f}, 
                '{strategy}');
            """
    execute(conn, query)
    conn.close()

def test(F, S, P, E, heuristic: callable, log_f: callable):
    num_iterations = [100, 10000, 100000]
    num_step = [0.05, 0.5, 1, 5, 10, 20, 40, 60, 80, 100]
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

                result = heuristic(F, S, P, E, step=step, initial_obj=(initial_x, initial_obj), log_f=log_f, strategy=strategy, max_iterations=iteration)
                print(f"Sol X = {result[0]}, Obj = {result[1]}, tiempo = {result[2]:.2f} segundos")

                results[(iteration, step, strategy)] = {
                    "X inicial": initial_x,
                    "Obj inicial": initial_obj,
                    "X": result[0],
                    "Obj": result[1],
                    "Tiempo": result[2]
                }

    print("################ RESULT ################")
    print(results)

def optimization_heuristic_initial_x(F: list, S: list, P: list, E: list, step: float, 
                                     initial_obj: tuple, log_f: callable, strategy: str, 
                                     max_iterations: int = 1000) -> list:
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
    return (best_X, best_obj, total_time)

def main():
    conn = get_connection(load_config('db/database.ini', 'supply_chain'))

    F = model.read_fabrication_centers(conn)
    S = model.read_distribution_centers(conn)
    P = model.read_points_of_sale(conn)
    E = model.read_scenarios(conn)

    create_tables()
    conn.close()

    test(F, S, P, E, optimization_heuristic_initial_x, log_x_initial)

if __name__ == "__main__":
    main()
