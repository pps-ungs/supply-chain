#!/usr/bin/env python

import time
from db.config import *
from db.database import *
from model import *


def main():

    ####################################################################
    # Conjuntos
    ####################################################################

    config = load_config('db/database.ini', 'supply_chain')
    conn = get_connection(config)

    F = read_fabrication_centers(conn)
    S = read_distribution_centers(conn)
    P = read_points_of_sale(conn)
    E = read_scenarios(conn)

    conn.close()
    print("[okay] Connection to supply_chain closed")

    t = time.time()
    X, Z, margin, pStk, pDIn, CTf2s, CTs2p, halting_condition = optimization_heuristic(F=F, S=S, P=P, E=E, step=20, epsilon=1e-3, max_iterations_allowed=1e1000, max_stuck_allowed=1)

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
