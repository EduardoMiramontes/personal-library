from app.integration.google_books import GoogleBooksClient
from app.integration.openlibrary import OpenLibraryClient
from app.integration.huggingface import HuggingFaceClassifier
from app.database.connection import DatabaseConnection

from datetime import datetime

class BookManager:
    def __init__(self):
        self.google = GoogleBooksClient()
        self.openlibrary = OpenLibraryClient()
        self.huggingface = HuggingFaceClassifier()
        self.db = DatabaseConnection()

    def agregar_libro(self, titulo, nombre_autor):
        # Buscar usando título + autor para resultados más precisos
        resultados = self.google.buscar_libros(f"{titulo} {nombre_autor}")
        if not resultados:
            print("No se encontraron libros.")
            return

        print("\nLibros encontrados:")
        for idx, libro in enumerate(resultados[:5]):
            print(f"{idx + 1}. {libro['titulo']} – {libro['autor']} ({libro['fecha']})")

        try:
            seleccion = int(input("Selecciona un número: ")) - 1
            if not 0 <= seleccion < len(resultados):
                print("Selección fuera de rango.")
                return
        except ValueError:
            print("Entrada inválida.")
            return

        libro_id = resultados[seleccion]["id"]
        detalles = self.google.obtener_datos_libro(libro_id)
        if not detalles:
            print("Error al obtener detalles del libro.")
            return

        # Solicitar al usuario los datos específicos de la edición
        editorial = input("Editorial: ").strip()
        isbn = input("ISBN: ").strip()
        formato_id = self._seleccionar_formato()

        # Categoría: Google Books o Hugging Face
        categorias = self.google.buscar_categoria(detalles["titulo"], nombre_autor)
        if not categorias:
            texto = f"{detalles['titulo']} por {nombre_autor}"
            clasificacion = self.huggingface.clasificar(texto)
            categorias = [clasificacion[0][0]] if clasificacion else []

        id_categorias = self._obtener_ids_categoria(categorias)

        # Obtener datos del autor automáticamente desde OpenLibrary
        autor_info = self._buscar_datos_autor_openlibrary(nombre_autor)

        # Insertar en base de datos
        self._insertar_libro(
            detalles=detalles,
            nombre_autor=nombre_autor,
            autor_pais=autor_info.get("pais_origen", "Desconocido"),
            autor_nacimiento=autor_info.get("fecha_nacimiento"),
            categorias_ids=id_categorias,
            editorial=editorial,
            isbn=isbn,
            formato_id=formato_id
        )
        print("Libro insertado exitosamente.")

    def _seleccionar_formato(self):
        with self.db as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_formato, nombre_formato FROM FORMATO ORDER BY id_formato;")
            formatos = cursor.fetchall()

            print("Selecciona el formato:")
            for formato in formatos:
                print(f"{formato['id_formato']}. {formato['nombre_formato']}")

            while True:
                opcion = input("Opción (número): ").strip()
                try:
                    opcion = int(opcion)
                    for formato in formatos:
                        if formato["id_formato"] == opcion:
                            return opcion
                    print("Formato no válido. Intenta de nuevo.")
                except ValueError:
                    print("Entrada inválida. Ingresa un número.")

    def _buscar_datos_autor_openlibrary(self, nombre_autor):
        candidatos = self.openlibrary.buscar_autor(nombre_autor)
        if not candidatos:
            return {}

        olid = candidatos[0].get("key").split("/")[-1]
        return self.openlibrary.obtener_datos_autor(olid) or {}

    
    def _insertar_libro(self, detalles, nombre_autor, autor_pais, autor_nacimiento,
                        categorias_ids, editorial, isbn, formato_id):
        def parse_fecha(fecha_str):
            if not fecha_str:
                return None
            try:
                return datetime.strptime(fecha_str, "%Y-%m-%d").date()
            except ValueError:
                try:
                    # Si solo viene el año: "1960"
                    return datetime.strptime(fecha_str, "%Y").replace(month=1, day=1).date()
                except ValueError:
                    try:
                        # Si viene solo año y mes: "1960-05"
                        return datetime.strptime(fecha_str, "%Y-%m").replace(day=1).date()
                    except:
                        return None

        with self.db as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CALL insertar_libro_completo(
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s
                )
                """, [
                    detalles["titulo"],
                    detalles.get("descripcion") or None,
                    int(detalles.get("numero_paginas")) if detalles.get("numero_paginas") else None,
                    detalles.get("portada") or None,
                    str(nombre_autor),
                    autor_pais or "Desconocido",
                    parse_fecha(autor_nacimiento),
                    str(editorial),
                    parse_fecha(detalles.get("fecha_publicacion")),
                    detalles.get("idioma") or "es",
                    str(isbn),
                    int(formato_id),
                    categorias_ids
                ]
            )
            conn.commit()

    def _obtener_ids_categoria(self, nombres_categoria):
        """
        Devuelve una lista de IDs de categorías.
        Inserta automáticamente aquellas que no existan.
        """
        ids = []
        with self.db as conn:
            cursor = conn.cursor()
            for nombre in nombres_categoria:
                cursor.execute("SELECT id_categoria FROM CATEGORIA WHERE LOWER(nombre_categoria) = LOWER(%s)", (nombre,))
                resultado = cursor.fetchone()
                if resultado:
                    ids.append(resultado["id_categoria"])
                else:
                    # Insertar nueva categoría
                    cursor.execute(
                        "INSERT INTO CATEGORIA (nombre_categoria) VALUES (%s) RETURNING id_categoria;",
                        (nombre,)
                    )
                    nuevo_id = cursor.fetchone()["id_categoria"]
                    ids.append(nuevo_id)
            conn.commit()
        return ids
    
