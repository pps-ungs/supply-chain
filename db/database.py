import psycopg
import subprocess
import os
import csv
import json
import pandas as pd
import db.config as dbconfig


def create_supply_chain_database(config: dict) -> None:
    try:
        with get_connection(config) as conn:
            print("[okay] Connection to postgres established")
            conn.autocommit = True
            with conn.cursor() as cur:
                # Delete this line in production
                cur.execute("drop database if exists supply_chain;")

                cur.execute("""
                    create database supply_chain;
                """)

                print("[okay] Database supply_chain created")
    except (psycopg.DatabaseError, Exception) as e:
        print(f"?error creating database: {e}")
    finally:
        conn.close()
        print("[okay] Connection to postgres closed")


def get_connection(config: dict) -> psycopg.Connection:
    try:
        conn = psycopg.connect(**config)
        print("[okay] Connection established")
        return conn
    except (psycopg.DatabaseError, Exception) as e:
        print(f"?error loading configuration: {e}")
        return None


def create_tables(conn: psycopg.Connection) -> None:
    try:
        with conn.cursor() as cur:
            cur.execute("""
                create table centro_de_fabricacion (
                    id serial primary key,
                    nombre text,
                    data text
                );
                        
                create table centro_de_distribucion (
                    id serial primary key,
                    nombre text,
                    data text
                );
                        
                create table punto_de_venta (
                    id serial primary key,
                    nombre text,
                    data text
                );

                create table escenario (
                    id serial primary key,
                    nombre text,
                    data jsonb
                );
                """)
            conn.commit()
            print("[okay] Tables created")
    except (psycopg.DatabaseError, Exception) as e:
        print(f"?error creating tables: {e}")


# ?
def insert_data_from_csv(conn: psycopg.Connection, insert_statement: str, csv_file: str) -> None:
    try:
        with conn.cursor() as cur:
            with open(csv_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    cur.execute(insert_statement, row)
            conn.commit()
            print(f"[okay] Data inserted from {csv_file}")
    except (psycopg.DatabaseError, Exception) as e:
        print(f"?error inserting data: {e}")

# ?
def insert_data_from_csv_json(conn: psycopg.Connection, insert_statement: str, csv_file: str) -> None:
    try:
        with conn.cursor() as cur:
            with open(csv_file, 'r', newline='') as file:
                reader = csv.DictReader(file, quotechar='"')
                for row in reader:
                    nombre = row['nombre']
                    data_str = row['data']
                    data_json = json.loads(data_str)
                    cur.execute(insert_statement, (nombre, json.dumps(data_json)))
            conn.commit()
            print(f"[okay] Data inserted from {csv_file}")
    except (psycopg.DatabaseError, Exception) as e:
        print(f"?error inserting data: {e}")


########################################################################
# DONE
# This function reads data from a PostgreSQL database and returns it as
# a pandas DataFrame.
#
# conn: a psycopg.Connection object representing the connection to the
#       PostgreSQL database
# select_statement: a string containing the SQL select statement to be
#                   executed
# df: a pandas DataFrame containing the data returned by the query
def read(conn: psycopg.Connection, select_statement: str) -> pd.DataFrame:
    try:
        df = pd.read_sql_query(select_statement, conn)
        print("[okay] Data loaded into DataFrame")
        return df
    except (psycopg.DatabaseError, Exception) as e:
        print(f"?error reading data': {e}")
        return pd.DataFrame()
# 
########################################################################
    
# Not used?
def insert(conn: psycopg.Connection, insert_statement: str, data: list) -> None:
    try:
        with conn.cursor() as cur:
            cur.execute(insert_statement, data)  
            conn.commit()
            print("[okay] Data inserted")
    except (psycopg.DatabaseError, Exception) as e:
        print(f"?error inserting data: {e}")

def execute(conn: psycopg.Connection, statement: str) -> None:
    try:
        with conn.cursor() as cur:
            cur.execute(statement)
            conn.commit()
            print("[okay] Statement executed")
    except (psycopg.DatabaseError, Exception) as e:
        print(f"?error executing statement: {e}")

# FIXME
# def insert_data_from_dataframe(conn: psycopg.Connection, insert_statement: str, df: pd.DataFrame) -> None:
#     try:
#         with conn.cursor() as cur:
#             for index, row in df.iterrows():
#                 cur.execute(insert_statement, tuple(row))
#             conn.commit()
#             print("[okay] Data inserted from DataFrame")
#     except (psycopg.DatabaseError, Exception) as e:
#         print(f"?error inserting data: {e}")
#

def dump(filepath: str, config: dict) -> None:
    dbname = "supply_chain"
    user = config["user"]
    password = config["password"]

    env = os.environ.copy()
    env["PGPASSWORD"] = password

    command = [
        "pg_dump",
        "-U", user,
        dbname
    ]

    try:
        result = subprocess.run(
            command,
            env=env,
            check=True,
            capture_output=True,
            text=True,
            shell=(os.name == 'nt')
        )
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(result.stdout)
        print("[okay] database dumped")
    except subprocess.CalledProcessError as e:
        print(f"[error] Error ejecutando pg_dump: {e}")
        print(e.stderr)

def restore(filepath: str) -> None:
    config = dbconfig.load_config('db/database.ini', 'postgres')
    create_supply_chain_database(config)

    if os.name == 'posix':
        command = f"psql -U postgres supply_chain < {filepath}"
    elif os.name == 'nt':  # Windows?
        command = f"psql -U postgres supply_chain < {filepath}"  # Windows command?
    else:
        raise Exception("?unsupported operating system")

    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"?error executing command: {e}")
        print(e.stderr)
    finally:
        print("[okay] database restored")
