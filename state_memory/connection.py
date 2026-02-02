import psycopg

def create_connection(db_url: str) -> psycopg.Connection:
    conn = psycopg.connect(db_url)
    return conn