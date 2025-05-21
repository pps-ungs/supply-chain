#!/usr/bin/env python

import time

import model
from db.config import load_config
from db.database import get_connection


def main():
    ####################################################################
    # Conjuntos
    ####################################################################

    config = load_config('db/database.ini', 'supply_chain')
    conn = get_connection(config)

    F = model.read_fabrication_centers(conn)
    S = model.read_distribution_centers(conn)
    P = model.read_points_of_sale(conn)
    E = model.read_scenarios(conn)

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
