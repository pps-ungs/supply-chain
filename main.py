from db.config import *
from db.database import *
from modelo import *


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

    X, Y, margin, pStk, pDIn, CTf2s, CTs2p = optimization_heuristic(F, S, P, E, 0.5)

    print("################ RESULT ################")
    print("X:", X)
    print("Y:", Y)
    print("Margin:", margin)
    print("pStk:", pStk)
    print("pDIn:", pDIn)
    print("CTf2s:", CTf2s)
    print("CTs2p:", CTs2p)
    print("########################################")

if __name__ == "__main__":
    main()
