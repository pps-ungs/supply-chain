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

    X = [100, 200, 300, 400, 500, 100, 200, 300, 400, 500]
    wDS = generate_products_to_distribution_center(X, S, cf)

    print("wDS:", wDS)

    wDP = generate_products_to_points_of_sale(F, S, P, wDS, cp)

    Y, Z = generate_stock_and_unsatisfied_demand(S, P, d, wDP)
    print("Y:", Y)
    print("Z:", Z)

    supply_chain(objective_function, m, ct, cv, pi, d, cf, cp, ps, pdi)


if __name__ == "__main__":
    main()
