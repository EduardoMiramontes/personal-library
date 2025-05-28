import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
from database.connection import DatabaseConnection

# Cargar variables del entorno
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

SQL_DIR = os.path.join(os.path.dirname(__file__), "database")
SQL_FILES = [
    "schema.sql",
    "triggers.sql",
    "procedures.sql",
    "functions.sql",
    "seeds.sql",
    "views.sql"
]

def create_database_if_not_exists():
    try:
        # Conexión al sistema (base de datos postgres)
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Comprobar si la base de datos ya existe
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = %s;", (DB_NAME,))
        exists = cur.fetchone()

        if not exists:
            print(f"🛠️  Creando base de datos '{DB_NAME}'...")
            cur.execute(f"CREATE DATABASE {DB_NAME};")
            print(f"✅ Base de datos '{DB_NAME}' creada.")
        else:
            print(f"ℹ️  La base de datos '{DB_NAME}' ya existe.")

        cur.close()
        conn.close()

    except Exception as e:
        print("❌ Error verificando o creando la base de datos:", e)
        exit(1)

def execute_sql_file(cursor, path):
    with open(path, "r", encoding="utf-8") as file:
        sql_code = file.read()
        cursor.execute(sql_code)

def main():
    create_database_if_not_exists()

    db = DatabaseConnection()
    conn = db.connect()
    if not conn:
        print("❌ No se pudo conectar a la base de datos.")
        return

    try:
        with conn.cursor() as cur:
            for file in SQL_FILES:
                path = os.path.join(SQL_DIR, file)
                print(f"→ Ejecutando: {file}")
                execute_sql_file(cur, path)
        conn.commit()
        print("✅ Base de datos inicializada correctamente.")
    except Exception as e:
        print("❌ Error ejecutando archivos SQL:", e)
    finally:
        db.close()

if __name__ == "__main__":
    main()