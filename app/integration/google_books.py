import requests

class GoogleBooksClient:
    BASE_URL = "https://www.googleapis.com/books/v1/volumes"

    def buscar_libros(self, titulo, idioma='es', max_resultados=20):
        query = f"{self.BASE_URL}?q=intitle:{titulo.replace(' ', '+')}&langRestrict={idioma}&maxResults={max_resultados}"
        resp = requests.get(query)

        if resp.status_code != 200:
            print("Error al consultar Google Books API.")
            return []

        data = resp.json()
        items = data.get("items", [])
        resultados = []
        for item in items:
            info = item.get("volumeInfo", {})
            portada_url = info.get("imageLinks", {}).get("thumbnail") 
            resultados.append({
                "id": item.get("id"),
                "titulo": info.get("title", "Sin título"),
                "autor": ", ".join(info.get("authors", ["Desconocido"])),
                "fecha": info.get("publishedDate", "s/f"),
                "portada": portada_url 
            })

        return resultados

    def obtener_datos_libro(self, id_libro, formato_manual="físico"):
        url = f"{self.BASE_URL}/{id_libro}"
        resp = requests.get(url)
        if resp.status_code != 200:
            return None

        datos = resp.json()
        info = datos.get("volumeInfo", {})

        def extraer_isbn(info):
            for i in info.get("industryIdentifiers", []):
                if i.get("type") in ["ISBN_13", "ISBN_10"]:
                    return i.get("identifier")
            return None

        def extraer_portada(imagenes):
            return imagenes.get("thumbnail") if imagenes else None

        return {
            "id_libro": datos.get("id"),
            "titulo": info.get("title"),
            "idioma": info.get("language"),
            "formato": formato_manual,
            "fecha_publicacion": info.get("publishedDate"),
            "editorial": info.get("publisher"),
            "isbn": extraer_isbn(info),
            "descripcion": info.get("description"),
            "numero_paginas": info.get("pageCount"),
            "portada": extraer_portada(info.get("imageLinks"))
        }

    def buscar_categoria(self, titulo, autor):
        query = f"{self.BASE_URL}?q=intitle:{titulo.replace(' ', '+')}+inauthor:{autor.replace(' ', '+')}&maxResults=1"
        resp = requests.get(query)
        if resp.status_code != 200:
            return None

        data = resp.json()
        items = data.get("items", [])
        if not items:
            return None

        return items[0].get("volumeInfo", {}).get("categories", [])