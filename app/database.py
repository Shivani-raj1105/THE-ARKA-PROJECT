import psycopg2
import psycopg2.extras
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@plant_db:5432/plants")


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    return conn


def get_cursor(conn):
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
