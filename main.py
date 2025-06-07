#!/usr/bin/env python

import time, sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "models/")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "experiments/")))
from hill_climbing import HillClimbing
import db.database as db
import db.config as dbconfig
import x_initial

def main():
    ####################################################################
    # Conjuntos
    ####################################################################

    config = dbconfig.load_config('db/database.ini', 'supply_chain')
    conn = db.get_connection(config)

    F = db.read(conn, "SELECT * FROM fabrication_centers").to_dict(orient='records')
    S = db.read(conn, "SELECT * FROM distribution_centers").to_dict(orient='records')
    P = db.read(conn, "SELECT * FROM points_of_sale").to_dict(orient='records')
    E = db.read(conn, "SELECT * FROM scenarios").to_dict(orient='records')

    conn.close()
    print("[okay] Connection to supply_chain closed")

    t = time.time()

    # Instanciar el modelo HillClimbing
    model = HillClimbing(F, S, P, E)
    result = model.solve(step=20, epsilon=1e-3, max_iterations_allowed=100, x_initial=x_initial.get_initial_X_from_most_probable_scenario(model, F, E), max_stuck_allowed=1000)

    print("############################### RESULTS ################################")
    print("X:", result["X"])
    print("Z:", result["Z"]) # Objective function value
    # Si quieres imprimir los componentes, puedes obtenerlos así:
    margin, pStk, pDIn, CTf2s, CTs2p = model.get_objective_function_values(F, S, P, E, result["X"])
    print("Margin:", margin)
    print("pStk:", pStk)
    print("pDIn:", pDIn)
    print("CTf2s:", CTf2s)
    print("CTs2p:", CTs2p)
    print("Iterations:", result.get("iterations"))
    print("Time:", time.time() - t)
    print("########################################################################")

if __name__ == "__main__":
    main()