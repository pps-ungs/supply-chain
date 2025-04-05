import psycopg
from config import load_config
from connection import get_connection

def create_database() -> None:
    try:
        with psycopg.connect("dbname=postgres user=postgres") as conn:
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

def create_tables(conn: psycopg.Connection) -> None:
    try:
        with conn.cursor() as cur:
            cur.execute("""
                create table usuarie (
                    id serial primary key,
                    nombre text,
                    apellido text);

                create table escenario (
                    id serial primary key,
                    nombre text,
                    data text)
                """)
            conn.commit()
            print("[okay] Tables created")
    except (psycopg.DatabaseError, Exception) as e:
        print(f"?error creating tables: {e}")

if __name__ == "__main__":
    create_database()

    config = load_config()
    conn = get_connection(config)

    create_tables(conn)

    conn.close()
    print("[okay] Connection closed")