from app.logic.book_manager import BookManager

def main():
    print("\n=== Biblioteca Personal ===")
    titulo = input("Título del libro: ").strip()
    autor = input("Autor o autora: ").strip()

    if not titulo or not autor:
        print("El título y el autor son obligatorios.")
        return

    manager = BookManager()
    manager.agregar_libro(titulo, autor)

if __name__ == "__main__":
    main()