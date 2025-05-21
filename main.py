#!/usr/bin/env python

import time

import model
import db.database as db
import db.config as dbconfig


def main():
    ####################################################################
    # Conjuntos
    ####################################################################

    config = dbconfig.load_config('db/database.ini', 'supply_chain')
    conn = db.get_connection(config)

    F = db.read(conn, model.fabrication_centers_read()).to_dict(orient='records')
    S = db.read(conn, model.distribution_centers_read()).to_dict(orient='records')
    P = db.read(conn, model.points_of_sale_read()).to_dict(orient='records')
    E = db.read(conn, model.scenarios_read()).to_dict(orient='records')

    conn.close()
    print("[okay] Connection to supply_chain closed")

    t = time.time()
    X, Z, margin, pStk, pDIn, CTf2s, CTs2p, halting_condition = model.optimization_heuristic(F=F, S=S, P=P, E=E, step=20, epsilon=1e-3, max_iterations_allowed=100, max_stuck_allowed=1)

    print("############################### RESULTS ################################")
    print("X:", X)
    print("Z:", Z) # Objective function value
    print("Margin:", margin)
    print("pStk:", pStk)
    print("pDIn:", pDIn)
    print("CTf2s:", CTf2s)
    print("CTs2p:", CTs2p)
    print("Halting condition:", halting_condition)
    print("Time:", time.time() - t)
    print("########################################################################")

if __name__ == "__main__":
    main()
