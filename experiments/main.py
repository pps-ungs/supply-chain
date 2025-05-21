#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../db')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../modelo')))

## viva peron ##########################################################
# Si agrego esto, no me tira error de importación
import db.config as dbconfig
import db.database as db
## viva peron ##########################################################

from db.database import *
from model import *
import experiments.run_experiments as neighborhood

def main():
    ## viva peron ##########################################################
    # modifiqué esta línea y ahora no me tire error de importación
    conn = db.get_connection(dbconfig.load_config('../db/database.ini', 'supply_chain')) # el path "../db/database.ini" es la clave
    ## viva peron ##########################################################

    F = read_fabrication_centers(conn)
    S = read_distribution_centers(conn)
    P = read_points_of_sale(conn)
    E = read_scenarios(conn)

    conn.close()
    print("[okay] Connection to supply_chain closed")

    #neighborhood.run_creation_neighbors_experiment(F=F, S=S, P=P, E=E)
    #neighborhood.run_eval_neighbors_experiment(F=F, S=S, P=P, E=E)
    neighborhood.run_creation_aval_neighbors_experiment(F=F, S=S, P=P, E=E)



if __name__ == "__main__":
    main()
