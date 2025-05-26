import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.logic.status_tracker import StatusTracker
from app.database.connection import DatabaseConnection

tracker = StatusTracker()
db = DatabaseConnection()
libros = []

def cargar_libros():
    with db as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id_libro, titulo FROM LIBRO ORDER BY titulo;")
        rows = cursor.fetchall()
        libros.clear()
        lista_libros.delete(0, tk.END)
        for row in rows:
            libros.append(row)
            lista_libros.insert(tk.END, f"{row['titulo']} (ID: {row['id_libro']})")

def registrar_estado():
    seleccion = lista_libros.curselection()
    if not seleccion:
        messagebox.showwarning("Selecciona un libro", "Debes seleccionar un libro.")
        return

    idx = seleccion[0]
    id_libro = libros[idx]["id_libro"]

    estatus = estatus_var.get()
    comentario = comentario_entry.get("1.0", tk.END).strip()
    calificacion_txt = calificacion_var.get()

    if estatus == "leído":
        if not calificacion_txt:
            messagebox.showerror("Calificación requerida", "Ingresa una calificación para un libro leído.")
            return
        try:
            calificacion = int(calificacion_txt)
        except ValueError:
            messagebox.showerror("Formato inválido", "La calificación debe ser un número entero.")
            return
    else:
        calificacion = None

    try:
        tracker.registrar_estado(id_libro, estatus, calificacion, comentario)
        messagebox.showinfo("Éxito", "Estado registrado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI
ventana = tk.Tk()
ventana.title("Registrar estado de lectura")
ventana.geometry("600x500")

tk.Button(ventana, text="🔄 Cargar libros", command=cargar_libros).pack(pady=10)

lista_libros = tk.Listbox(ventana, width=60, height=10)
lista_libros.pack()

# Estatus
tk.Label(ventana, text="Estatus de lectura").pack()
estatus_var = tk.StringVar(value="sin comenzar")
estatus_menu = tk.OptionMenu(ventana, estatus_var, "sin comenzar", "leyendo", "pausado", "leído", "abandonado")
estatus_menu.pack()

# Calificación
tk.Label(ventana, text="Calificación (solo si es 'leído')").pack()
calificacion_var = tk.StringVar()
tk.Entry(ventana, textvariable=calificacion_var).pack()

# Comentario
tk.Label(ventana, text="Comentario (opcional)").pack()
comentario_entry = tk.Text(ventana, height=5, width=50)
comentario_entry.pack(pady=10)

tk.Button(ventana, text="✅ Registrar estado", command=registrar_estado).pack(pady=10)

ventana.mainloop()