#!/usr/bin/env python3

import models.model as model
import db.database as db
import db.queries as queries

def create_database(config):
    ####################################################################
    # DB
    db.create_supply_chain_database(config)
    conn = db.get_connection(config)

    db.create_tables(conn)

    ####################################################################
    # Centros de fabricación
    db.insert_data_from_csv(conn, "insert into centro_de_fabricacion (nombre, data) values (%s, %s);", "./db/data/sets/fabrication_centers.csv")
    # Centros de distribución
    db.insert_data_from_csv(conn, "insert into centro_de_distribucion (nombre, data) values (%s, %s);", "./db/data/sets/distribution_centers.csv")
    # Puntos de venta
    db.insert_data_from_csv(conn,  "insert into punto_de_venta (nombre, data) values (%s, %s);", "./db/data/sets/points_of_sale.csv")
    # Escenarios
    db.insert_data_from_csv_json(conn, "insert into escenario (nombre, data) values (%s, %s);", "./db/data/sets/scenarios-normal.csv")
    ####################################################################
    print("[okay] Database created")

    conn.close()
    print("[okay] Connection closed")
    #
    ####################################################################

    # Dump the database
    ans = input("Do you want to dump (backup to a file) the database? (y/n): ")
    if ans == "y":
        db.dump("db/data/dumps/supply-chain-dump.sql", config)
        print("[okay] Database dumped to db/data/dumps/supply-chain-dump.sql")
    else:
        print("[okay] Database not dumped")

def restore_database():
    db.restore("db/data/dumps/supply-chain-dump.sql")
    print("[okay] Database restored from db/data/dumps/supply-chain-dump.sql")

def read_database(config):
    conn = db.get_connection(config)
    F = db.read(conn, queries.get_fabrication_centers_query()).to_dict(orient='records')
    S = db.read(conn, queries.get_distribution_centers_query()).to_dict(orient='records')
    P = db.read(conn, queries.get_points_of_sale_query()).to_dict(orient='records')
    E = db.read(conn, queries.get_scenarios_query()).to_dict(orient='records')
    
    print("[okay] Data read from database")
    conn.close()
    print("[okay] Connection closed")
    
    return {
        "F": F,
        "S": S,
        "P": P,
        "E": E
    }
