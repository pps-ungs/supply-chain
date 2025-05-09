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
    X, Y, margin, pStk, pDIn, CTf2s, CTs2p, objective_value, limit_is_not_reached = optimization_heuristic_with_strategy(F, S, P, E, 0.5, 100000)

    print("################ RESULT ################")
    print("X:", X)
    print("Y:", Y)
    print("Margin:", margin)
    print("pStk:", pStk)
    print("pDIn:", pDIn)
    print("CTf2s:", CTf2s)
    print("CTs2p:", CTs2p)
    print("Objective value:", objective_value)
    print("Limit is not reached:", limit_is_not_reached)
    print("Time:", time.time() - t)
    print("########################################")

if __name__ == "__main__":
    main()
