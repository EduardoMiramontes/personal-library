from PIL import Image, ImageTk
import urllib.request
import io
import tkinter as tk
from tkinter import messagebox
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.ui.book_manager_gui import BookManagerGUI

manager = BookManagerGUI()
libros = []

def buscar():
    titulo = titulo_entry.get()
    autor = autor_entry.get()
    if not titulo or not autor:
        messagebox.showwarning("Campos vacíos", "Debes ingresar título y autor.")
        return

    global libros
    libros = manager.buscar_libros(titulo, autor)
    lista_libros.delete(0, tk.END)

    if not libros:
        messagebox.showinfo("Sin resultados", "No se encontraron libros.")
        portada_label.configure(image='', text='')
    else:
        for i, libro in enumerate(libros):
            lista_libros.insert(tk.END, f"{libro['titulo']} - {libro['autor']} ({libro['fecha']})")
        actualizar_portada()  # Muestra la portada del primer libro por defecto

def guardar():
    seleccion = lista_libros.curselection()
    if not seleccion:
        messagebox.showwarning("Selección vacía", "Selecciona un libro de la lista.")
        return

    idx = seleccion[0]
    libro_id = libros[idx]["id"]
    detalles = manager.obtener_detalles_libro(libro_id)

    editorial = editorial_entry.get()
    isbn = isbn_entry.get()
    formato_nombre = formato_var.get()
    formato_id = formato_dict.get(formato_nombre)

    if not (editorial and isbn and formato_id):
        messagebox.showerror("Datos faltantes", "Completa todos los campos de edición.")
        return

    try:
        formato_id = int(formato_id)
    except ValueError:
        messagebox.showerror("Formato inválido", "Formato debe ser un número entero.")
        return

    try:
        manager.guardar_libro(detalles, autor=autor_entry.get(), editorial=editorial, isbn=isbn, formato_id=formato_id)
        messagebox.showinfo("Éxito", "Libro guardado exitosamente.")
    except Exception as e:
        messagebox.showerror("Error al guardar", str(e))

def mostrar_portada_desde_url(url):
    try:
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        im = Image.open(io.BytesIO(raw_data))
        im.thumbnail((150, 220))  # Tamaño ajustado
        imagen = ImageTk.PhotoImage(im)
        portada_label.configure(image=imagen, text='')
        portada_label.image = imagen
    except:
        portada_label.configure(image='', text="(Sin portada)")

def actualizar_portada(event=None):
    seleccion = lista_libros.curselection()
    if not seleccion:
        portada_label.configure(image='', text='')
        return
    idx = seleccion[0]
    portada_url = libros[idx].get("portada")
    if portada_url:
        mostrar_portada_desde_url(portada_url)
    else:
        portada_label.configure(image='', text="(Sin portada)")

# --- GUI ---
ventana = tk.Tk()
ventana.title("Biblioteca Personal")

tk.Label(ventana, text="Título").grid(row=0, column=0)
titulo_entry = tk.Entry(ventana, width=40)
titulo_entry.grid(row=0, column=1)

tk.Label(ventana, text="Autor").grid(row=1, column=0)
autor_entry = tk.Entry(ventana, width=40)
autor_entry.grid(row=1, column=1)

tk.Button(ventana, text="Buscar libros", command=buscar).grid(row=2, column=0, columnspan=2, pady=5)

lista_libros = tk.Listbox(ventana, width=70)
lista_libros.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
lista_libros.bind("<<ListboxSelect>>", actualizar_portada)

# Portada del libro
portada_label = tk.Label(ventana)
portada_label.grid(row=3, column=2, rowspan=4, padx=10, pady=10)

tk.Label(ventana, text="Editorial").grid(row=4, column=0)
editorial_entry = tk.Entry(ventana, width=40)
editorial_entry.grid(row=4, column=1)

tk.Label(ventana, text="ISBN").grid(row=5, column=0)
isbn_entry = tk.Entry(ventana, width=40)
isbn_entry.grid(row=5, column=1)

# Formato desplegable
tk.Label(ventana, text="Formato").grid(row=6, column=0)
formatos = manager.obtener_formatos()
formato_dict = {nombre: fid for fid, nombre in formatos}
formato_var = tk.StringVar()
if formatos:
    formato_var.set(formatos[0][1])  # Primer formato como default

formato_menu = tk.OptionMenu(ventana, formato_var, *formato_dict.keys())
formato_menu.config(width=37)
formato_menu.grid(row=6, column=1)

tk.Button(ventana, text="Guardar selección", command=guardar).grid(row=7, column=0, columnspan=2, pady=10)

ventana.mainloop()