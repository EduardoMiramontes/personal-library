from app.database.connection import DatabaseConnection

class StatusTracker:
    def __init__(self):
        self.db = DatabaseConnection()

    def registrar_estado(self, id_libro, estatus, calificacion, comentario):
        if calificacion is not None and estatus != "leído":
            raise ValueError("Solo puedes registrar calificación si el estatus es 'leído'.")

        with self.db as conn:
            cursor = conn.cursor()
            cursor.execute(
                "CALL registrar_estado_lectura(%s::INT, %s::VARCHAR, %s::SMALLINT, %s::TEXT);",
                (id_libro, estatus, calificacion, comentario)
            )
            conn.commit()
            print("Estado registrado correctamente.")

    def actualizar_estado(self, id_historial, nuevo_estatus):
        with self.db as conn:
            cursor = conn.cursor()
            cursor.execute(
                "CALL actualizar_estado_lectura(%s, %s);",
                (id_historial, nuevo_estatus)
            )
            conn.commit()
            print("Estado actualizado.")

    def marcar_leido_hoy(self, id_libro, calificacion, comentario):
        with self.db as conn:
            cursor = conn.cursor()
            cursor.execute(
                "CALL marcar_leido_hoy(%s, %s, %s);",
                (id_libro, calificacion, comentario)
            )
            conn.commit()
            print("Libro marcado como 'leído' con fecha de hoy.")

    def ver_historial(self):
        with self.db as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT H.id_historial, L.titulo, H.estatus, H.calificación_personal,
                       H.fecha_registro, H.comentario
                FROM HISTORIAL H
                JOIN LIBRO L ON H.id_libro = L.id_libro
                ORDER BY H.fecha_registro DESC;
            """)
            resultados = cursor.fetchall()
            for row in resultados:
                print(f"[{row['id_historial']}] {row['titulo']} - {row['estatus']} ({row['fecha_registro']})")
                if row['comentario']:
                    print(f"   Comentario: {row['comentario']}")