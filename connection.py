""""
import psycopg
from config import load_config

def get_connection(config : dict) -> psycopg.Connection:
    try:
        conn = psycopg.connect(**config)
        print("[okay] Connection established")
        return conn
    except (psycopg.DatabaseError, Exception) as e:
        print(f"?error loading configuration: {e}")
        return None

if __name__ == "__main__":
    config = load_config()
    conn = get_connection(config)
    conn.close()
    print("[okay] Connection closed")

""""