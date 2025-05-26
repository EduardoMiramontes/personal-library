from app.logic.book_manager import BookManager

class BookManagerGUI(BookManager):
    def buscar_libros(self, titulo, autor):
        resultados = self.google.buscar_libros(f"{titulo} {autor}")
        return resultados[:10] if resultados else []

    def obtener_detalles_libro(self, libro_id):
        return self.google.obtener_datos_libro(libro_id)

    def obtener_formatos(self):
        with self.db as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_formato, nombre_formato FROM FORMATO ORDER BY id_formato;")
            formatos = cursor.fetchall()
            return [(f["id_formato"], f["nombre_formato"]) for f in formatos]
    
    def guardar_libro(self, detalles, autor, editorial, isbn, formato_id):
        # Obtener categoría automáticamente
        categorias = self.google.buscar_categoria(detalles["titulo"], autor)
        if not categorias:
            texto = f"{detalles['titulo']} por {autor}"
            clasificacion = self.huggingface.clasificar(texto)
            categorias = [clasificacion[0][0]] if clasificacion else []

        id_categorias = self._obtener_ids_categoria(categorias)

        # Buscar información del autor
        autor_info = self._buscar_datos_autor_openlibrary(autor)

        # Insertar en base de datos
        self._insertar_libro(
            detalles=detalles,
            nombre_autor=autor,
            autor_pais=autor_info.get("pais_origen", "Desconocido"),
            autor_nacimiento=autor_info.get("fecha_nacimiento"),
            categorias_ids=id_categorias,
            editorial=editorial,
            isbn=isbn,
            formato_id=formato_id
        )
        return True