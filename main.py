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

    F = db.read(conn, "SELECT * FROM centro_de_fabricacion").to_dict(orient='records')
    S = db.read(conn, "SELECT * FROM centro_de_distribucion").to_dict(orient='records')
    P = db.read(conn, "SELECT * FROM punto_de_venta").to_dict(orient='records')
    E = db.read(conn, "SELECT * FROM escenario").to_dict(orient='records')

    conn.close()
    print("[okay] Connection to supply_chain closed")

    t = time.time()

    # Instanciar el modelo HillClimbing
    model = HillClimbing(F, S, P, E)
    result = model.solve(step=936, initial_X=x_initial.get_initial_X_from_most_probable_scenario(model, F, E), max_iterations_allowed=100)

    print("############################### RESULTS ################################")
    print("X:", result["X"])
    print("Z:", result["Z"])
    print("Margin:", result["margin"])
    print("pStk:", result["pStk"])
    print("pDIn:", result["pDIn"])
    print("CTf2s:", result["CTf2s"])
    print("CTs2p:", result["CTs2p"])
    print("Iterations:", result.get("iterations"))
    print("Time:", time.time() - t)
    print("########################################################################")

if __name__ == "__main__":
    main()