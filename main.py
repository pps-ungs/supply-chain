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
    
    print("E:",E)

    conn.close()
    print("[okay] Connection to supply_chain closed")

    ####################################################################
    # Parámetros
    ####################################################################

    m = get_margin_per_point_of_sale(P)
    ct = get_transportation_cost_from_fabrication_to_distribution(F, S)
    cv = get_transportation_cost_from_distribution_to_sale(S, P)
    pi = get_probability_of_occurrence(E)
    d = get_demand_per_point_of_sale(E, P)
    cf = get_distribution_curve_from_fabrication_to_distribution(F, S)
    cp = get_distribution_curve_from_distribution_to_sale(S, P)
    ps = get_distribution_curve_from_fabrication_to_sale(F, P)
    pdi = get_penalty_for_unsatisfied_demand(P)

    print("S:", S)
    print("P:", P)
    print("CP:", cp)
    print("CF:", cf)
    print("d:", d)

    X = optimization_heuristic(F, S, P, E, m, ct, cv, pi, d, cf, cp, ps, pdi)
    print("X:", X)

if __name__ == "__main__":
    main()
