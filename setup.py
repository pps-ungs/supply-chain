#!/usr/bin/env python3

import model
import db.config as dbconfig
import db.database as db

####################################################################
# DB
config = dbconfig.load_config('db/database.ini', 'postgres')
db.create_supply_chain_database(config)

config = dbconfig.load_config('db/database.ini', 'supply_chain')
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

conn.close()
print("[okay] Connection closed")
#
####################################################################

# Dump the database
ans = input("Do you want to dump (backup to a file) the database? (y/n): ")
if ans == "y":
    db.dump("db/data/supply_chain_dump.sql", {
        "user": "postgres",
        "password": "postgres"
    })
    print("[okay] Database dumped to db/data/supply_chain_dump.sql")
else:
    print("[okay] Database not dumped")

# Restore the database
ans = input("Do you want to restore the database from the dump file? (y/n): ")
if ans == "y":
    db.restore("db/data/supply_chain_dump.sql")
    print("[okay] Database restored from db/data/supply_chain_dump.sql")
else:
    print("[okay] Database not restored")
