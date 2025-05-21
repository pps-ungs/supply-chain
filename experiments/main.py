#!/usr/bin/env python

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../db")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../modelo")))

## viva peron ##########################################################
# Si agrego esto, no me tira error de importación
import db.config as dbconfig
import db.database as db
import experiments.run_experiments as nh
import model
## viva peron ##########################################################


def main():
    ## viva peron ##########################################################
    # modifiqué esta línea y ahora no me tire error de importación
    conn = db.get_connection(dbconfig.load_config("../db/database.ini", "supply_chain"))  # el path "../db/database.ini" es la clave
    ## viva peron ##########################################################

    F = db.read(conn, model.fabrication_centers_read()).to_dict(orient="records")
    S = db.read(conn, model.distribution_centers_read()).to_dict(orient="records")
    P = db.read(conn, model.points_of_sale_read()).to_dict(orient="records")
    E = db.read(conn, model.scenarios_read()).to_dict(orient="records")

    conn.close()
    print("[okay] Connection to supply_chain closed")

    dir = "experiments/results_new_db/creation_evaluation_neighbors"
    # run_creation_neighbors_experiment(dir=dir, F=F, S=S, P=P, E=E)
    # run_eval_neighbors_experiment(dir=dir, F=F, S=S, P=P, E=E)
    nh.run_creation_eval_neighbors_experiment(dir=dir, F=F, S=S, P=P, E=E)

if __name__ == "__main__":
    main()
