import tkinter as tk
from tkinter import ttk, simpledialog
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.logic.reports import Reports

rep = Reports()

def mostrar_resultado(nombre, datos):
    ventana = tk.Toplevel()
    ventana.title(nombre)

    if not datos:
        tk.Label(ventana, text="Sin resultados").pack(padx=20, pady=20)
        return

    cols = list(datos[0].keys())
    tabla = ttk.Treeview(ventana, columns=cols, show="headings")

    for col in cols:
        tabla.heading(col, text=col)
        tabla.column(col, width=120)

    for fila in datos:
        tabla.insert('', 'end', values=[fila[col] for col in cols])

    tabla.pack(fill="both", expand=True)

def libros_leidos(): mostrar_resultado("Libros leídos", rep.libros_leidos())
def libros_por_autor():
    autor = simpledialog.askstring("Buscar por autor", "Nombre del autor:")
    if autor:
        mostrar_resultado(f"Libros por autor: {autor}", rep.libros_por_autor(autor))
def libros_por_categoria():
    cat = simpledialog.askstring("Buscar por categoría", "Nombre de la categoría:")
    if cat:
        mostrar_resultado(f"Libros por categoría: {cat}", rep.libros_por_categoria(cat))
def resumen_por_estatus(): mostrar_resultado("Resumen por estatus", rep.resumen_por_estatus())
def estado_lectura_actual(): mostrar_resultado("Estado de lectura actual", rep.estado_lectura_actual())
def libros_sin_comenzar(): mostrar_resultado("Libros sin comenzar", rep.libros_sin_comenzar())

ventana = tk.Tk()
ventana.title("Reportes de Biblioteca")

tk.Label(ventana, text="Selecciona un reporte:", font=("Arial", 14)).pack(pady=10)

opciones = [
    ("📘 Libros leídos", libros_leidos),
    ("👤 Libros por autor", libros_por_autor),
    ("🏷️ Libros por categoría", libros_por_categoria),
    ("📊 Resumen por estatus", resumen_por_estatus),
    ("📖 Estado de lectura actual", estado_lectura_actual),
    ("🚫 Libros sin comenzar", libros_sin_comenzar),
]

for texto, accion in opciones:
    tk.Button(ventana, text=texto, width=30, command=accion).pack(pady=3)

ventana.mainloop()