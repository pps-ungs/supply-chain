#!/usr/bin/env python3

import models.model as model
import db.config as dbconfig
import db.database as db

def create_database(config):
    ####################################################################
    # DB
    db.create_supply_chain_database(config)
    conn = db.get_connection(config)

    db.create_tables(conn)

    ####################################################################
    # Centros de fabricación
    db.insert_data_from_csv(conn, model.fabrication_centers_write(), "./db/data/conjuntos/fabrication_centers.csv")
    # Centros de distribución
    db.insert_data_from_csv(conn, model.distribution_centers_write(), "./db/data/conjuntos/distribution_centers.csv")
    # Puntos de venta
    db.insert_data_from_csv(conn, model.points_of_sale_write(), "./db/data/conjuntos/points_of_sale.csv")
    # Escenarios
    db.insert_data_from_csv_json(conn, model.scenarios_write(), "./db/data/conjuntos/scenarios-normal.csv")
    ####################################################################
    print("[okay] Database created")

    conn.close()
    print("[okay] Connection closed")
    #
    ####################################################################

    # Dump the database
    ans = input("Do you want to dump (backup to a file) the database? (y/n): ")
    if ans == "y":
        db.dump("db/data/supply_chain_dump.sql", config)
        print("[okay] Database dumped to db/data/supply_chain_dump.sql")
    else:
        print("[okay] Database not dumped")

def restore_database(config):
    db.restore("db/data/supply_chain_dump.sql")
    print("[okay] Database restored from db/data/supply_chain_dump.sql")

def read_database(config):
    conn = db.get_connection(config)
    F = db.read(conn, "SELECT * FROM centro_de_fabricacion").to_dict(orient='records')
    S = db.read(conn, "SELECT * FROM centro_de_distribucion").to_dict(orient='records')
    P = db.read(conn, "SELECT * FROM punto_de_venta").to_dict(orient='records')
    E = db.read(conn, "SELECT * FROM escenario").to_dict(orient='records')
    
    return {
        "F": F,
        "S": S,
        "P": P,
        "E": E
    }
