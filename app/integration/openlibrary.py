import requests

class OpenLibraryClient:
    def buscar_autor(self, nombre_autor, max_resultados=5):
        query = f"https://openlibrary.org/search/authors.json?q={nombre_autor.replace(' ', '+')}"
        resp = requests.get(query)
        if resp.status_code != 200:
            return []

        data = resp.json()
        return data.get("docs", [])[:max_resultados]

    def obtener_datos_autor(self, olid):
        url = f"https://openlibrary.org/authors/{olid}.json"
        resp = requests.get(url)
        if resp.status_code != 200:
            return None

        datos = resp.json()

        def separar_nombre_completo(nombre):
            partes = nombre.split()
            if len(partes) > 1:
                return ' '.join(partes[:-1]), partes[-1]
            return nombre, ""

        nombre_completo = datos.get("name", "")
        nombre, apellido = separar_nombre_completo(nombre_completo)

        return {
            "id_autor": olid,
            "nombre": nombre,
            "apellido": apellido,
            "pais_origen": datos.get("location"),
            "fecha_nacimiento": datos.get("birth_date"),
            "fecha_muerte": datos.get("death_date")
        }