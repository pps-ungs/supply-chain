#!/usr/bin/env python

import os
import sys
import json
import time
import numpy as np

# Ajusta las rutas para importar tus módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../db/')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../models/')))

# Importa tus clases y módulos necesarios
import setup
import db.config as dbconfig
import db.database as db
from ant_colony import AntColony


def create_tables(config):
    conn = db.get_connection(config)

    query = """
        create table if not exists experimento_aco (
            id serial primary key,
            modelo text,
            experimento text,
            alpha decimal(15, 2),
            beta decimal(15, 2),
            rho decimal(15, 2),
            q decimal(15, 6),
            tau_min decimal(15, 6),
            tau_max decimal(15, 2),
            num_hormigas integer,
            max_iteraciones integer,
            x_optimo text,
            obj_optimo decimal(15, 2),
            tiempo_ejecucion decimal(15, 2),
            motivo_parada text,
            iteraciones_realizadas integer,
            historial_z text -- Para almacenar el JSON del historial de Z
        );
        """
    print("[data] Creating tables in database...")
    db.execute(conn, query)
    conn.close()
    print("[okay] Connection to database closed")

def log_aco_experiment(
        config,
        model_name,
        experiment_name,
        alpha, beta, rho, Q, tau_min, tau_max,
        num_ants, max_iterations,
        X_optimal, Z_optimal, 
        execution_time, 
        halting_condition, 
        iterations_performed,
        history_Z
    ):

    conn = db.get_connection(config)

    query = f"""
            insert into experimento_aco (
                modelo,
                experimento,
                alpha, beta, rho, q, tau_min, tau_max,
                num_hormigas, max_iteraciones,
                x_optimo, obj_optimo,
                tiempo_ejecucion, motivo_parada,
                iteraciones_realizadas, historial_z) 
            values (
                '{model_name}',
                '{experiment_name}',
                {alpha:.2f}, {beta:.2f}, {rho:.2f}, {Q:.6f}, {tau_min:.6f}, {tau_max:.2f},
                {num_ants}, {max_iterations},
                '{json.dumps(X_optimal.tolist()) if X_optimal is not None else 'null'}', {Z_optimal:.2f},
                {execution_time:.2f},
                '{halting_condition}',
                {iterations_performed},
                '{json.dumps(history_Z)}');
            """
    
    print("[data] Saving ACO experiment in database...")
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
    
    experiment_name = "favor_low_production"
    alpha_test = 0.5 
    beta_test = 3.0  
    rho_test = 0.3   
    num_ants_test = 100
    max_iterations_test = 100
    num_prod_levels = 500

    model_aco = AntColony(F, S, P, E, 
                          alpha=alpha_test, 
                          beta=beta_test, 
                          rho=rho_test,
                          num_prod_levels=num_prod_levels)
    
    print(f"\n--- Ejecutando Optimización con Colonia de Hormigas ---")
    print(f"Número de Hormigas: {num_ants_test}")
    print(f"Máximo de Iteraciones: {max_iterations_test}")
    print(f"Parámetros ACO: Alpha={alpha_test}, Beta={beta_test}, Rho={rho_test}")
    print(f"Q calculado: {model_aco.Q:.6f}, Tau_min: {model_aco.tau_min:.6f}, Tau_max: {model_aco.tau_max:.2f}")

    start_time = time.time()
    results_aco = model_aco.solve(num_ants=num_ants_test, 
                                 max_iterations=max_iterations_test)
    end_time = time.time()
    execution_time = end_time - start_time

    print(f"\n--- Resultados Finales de ACO ---")
    print(f"Condición de Parada: {results_aco['halting_condition']}")
    print(f"Iteraciones Realizadas: {results_aco['iterations']}")
    print(f"Tiempo de Ejecución: {execution_time:.2f} segundos")
    print(f"Mejor Solución de Producción (X_óptimo): {results_aco['X']}")
    print(f"Valor Óptimo de la Función Objetivo (Z_óptimo): {results_aco['Z']:.2f}")

    log_aco_experiment(
        config=config,
        model_name=model_aco.__class__.__name__,
        experiment_name=experiment_name,
        alpha=alpha_test, beta=beta_test, rho=rho_test,
        Q=model_aco.Q, tau_min=model_aco.tau_min, tau_max=model_aco.tau_max,
        num_ants=num_ants_test, max_iterations=max_iterations_test,
        X_optimal=results_aco["X"],
        Z_optimal=results_aco["Z"],
        execution_time=execution_time,
        halting_condition=results_aco["halting_condition"],
        iterations_performed=results_aco["iterations"],
        history_Z=results_aco["history_Z"]
    )
    print("[okay] Experiment logged to database.")

    db.dump("db/data/supply_chain_aco_results.sql", config)
    print("[okay] Database dumped.")

if __name__ == "__main__":
    main()