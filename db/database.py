import psycopg
import subprocess
import os
import csv
import json


def create_supply_chain_database(config: dict) -> None:
    try:
        with get_connection(config=config) as conn:
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
        # conn.close()
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
                create table escenario (
                    id serial primary key,
                    nombre text,
                    data jsonb
                );
                
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
                """)
            conn.commit()
            print("[okay] Tables created")
    except (psycopg.DatabaseError, Exception) as e:
        print(f"?error creating tables: {e}")


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

import pandas as pd

def read(conn: psycopg.Connection, select_statement: str) -> pd.DataFrame:
    try:
        df = pd.read_sql_query(select_statement, conn)
        print(f"[okay] Data loaded into DataFrame")
        return df
    except (psycopg.DatabaseError, Exception) as e:
        print(f"?error reading data': {e}")
        return pd.DataFrame()

def dump(filepath: str) -> None:
    if os.name == 'posix':
        command = f"pg_dump -U postgres supply_chain"
    elif os.name == 'nt':  # Windows?
        command = f"pg_dump -U postgres supply_chain"  # Windows command?
    else:
        raise Exception("?unsupported operating system")

    try:
        database_dump = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(database_dump.stdout)
        with open(filepath, "w") as f:
            f.write(database_dump.stdout)
    except subprocess.CalledProcessError as e:
        print(f"?error executing command: {e}")
        print(e.stderr)
    finally:
        print("[okay] database dumped")


def restore(filepath: str) -> None:
    create_supply_chain_database()

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
