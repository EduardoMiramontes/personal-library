from app.database.connection import DatabaseConnection

class Reports:
    def __init__(self):
        self.db = DatabaseConnection()

    def libros_leidos(self):
        with self.db as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM libros_leidos ORDER BY fecha_registro DESC;")
            return cursor.fetchall()

    def libros_por_autor(self, autor):
        with self.db as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM libros_por_autor
                WHERE LOWER(autor) LIKE LOWER(%s)
                ORDER BY titulo;
            """, (f"%{autor}%",))
            return cursor.fetchall()

    def libros_por_categoria(self, categoria):
        with self.db as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM libros_por_categoria
                WHERE LOWER(nombre_categoria) LIKE LOWER(%s)
                ORDER BY titulo;
            """, (f"%{categoria}%",))
            return cursor.fetchall()

    def resumen_por_estatus(self):
        with self.db as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM resumen_por_estatus;")
            return cursor.fetchall()

    def estado_lectura_actual(self):
        with self.db as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM estado_lectura_actual ORDER BY fecha_registro DESC;")
            return cursor.fetchall()

    def libros_sin_comenzar(self):
        with self.db as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM libros_sin_comenzar ORDER BY titulo;")
            return cursor.fetchall()