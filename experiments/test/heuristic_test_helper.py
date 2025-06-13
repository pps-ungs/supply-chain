import os
import sys
import inspect
import time
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../db/')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../models/')))

import db.config as dbconfig
import db.database as db


class HeuristicTestHelper:
    dbconfig = {}

    def __init__(self, dbconfig_path: str = 'db/database.ini', database_name: str = 'supply_chain'):
        self.dbconfig = dbconfig.load_config(dbconfig_path, database_name)
        self.create_tables()

    def create_tables(self):
        conn = db.get_connection(self.dbconfig)

        query = """
            create table if not exists experimento (
                id serial primary key,
                modelo text,
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

        print("[data] Creating tables in database...")
        db.execute(conn, query)
        conn.close()
        print("[okay] Connection to database closed")

    def solve(
            self,
            model,
            experiment: str,
            strategy: str,
            step: int = 20,
            initial_obj: tuple = (None, None),
            epsilon: float = 1e-12,
            max_iterations_allowed: int = 1e12,
            max_stuck_allowed: int = 1e3,
            loops_without_improvement = 0,
            max_restarts = 0
        ) -> dict:

        initial_time = time.time()

        solve_kwargs = {
            "step": step,
            "epsilon": epsilon,
            "max_iterations_allowed": max_iterations_allowed,
            "max_stuck_allowed": max_stuck_allowed,
            "initial_X": initial_obj[0],
            "loops_without_improvement": loops_without_improvement,
            "max_restarts": max_restarts
        }

        result = self.call_with_non_default_params(model.solve, **solve_kwargs)
        actual_time = time.time() - initial_time
        
        X = result["X"]
        Z = result["Z"]
        halting_condition = result.get("halting_condition", "unknown")
        
        self.log(
            model_name=model.__class__.__name__,
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
    
    import inspect

    def call_with_non_default_params(self, func, **kwargs):
        sig = inspect.signature(func)
        filtered = {}
        for k, v in kwargs.items():
            param = sig.parameters.get(k)
            if param is None:
                continue  # ignora parámetros que no existen en la función
            if param.default is inspect.Parameter.empty or v != param.default:
                filtered[k] = v
        return func(**filtered)
    
    def log(
            self,
            model_name,
            experiment, 
            X_initial,
            Z_initial, 
            X, 
            Z, 
            step, 
            it,
            actual_time, 
            halting_condition, 
            strategy
        ):

        conn = db.get_connection(self.dbconfig)

        query = f"""
                insert into experimento (
                    modelo,
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
                    '{model_name}',
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
        
        print("[data] Saving experiment in database...")
        db.execute(conn, query)
        conn.close()
        print("[okay] Connection to database closed")