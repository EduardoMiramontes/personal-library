import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()  # Cargar variables del archivo .env

class DatabaseConnection:
    def __init__(self):
        self.config = {
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
        }
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.config, cursor_factory=RealDictCursor)
            return self.conn
        except Exception as e:
            print("Error al conectar con la base de datos:", e)
            return None

    def close(self):
        if self.conn:
            self.conn.close()

    def test_connection(self):
        conn = self.connect()
        if conn:
            print("Conexión exitosa a la base LIBRARY")
            self.close()

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()