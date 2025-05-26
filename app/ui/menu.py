import tkinter as tk
import subprocess

def abrir_registro():
    subprocess.Popen(["python3", "app/ui/gui.py"])

def abrir_reportes():
    subprocess.Popen(["python3", "app/ui/reports_gui.py"])

def abrir_estado():
    subprocess.Popen(["python3", "app/ui/status_gui.py"])

ventana = tk.Tk()
ventana.title("Menú de Biblioteca Personal")
ventana.geometry("300x200")

tk.Label(ventana, text="¿Qué deseas hacer?", font=("Arial", 14)).pack(pady=20)

tk.Button(ventana, text="📚 Registrar nuevo libro", width=25, command=abrir_registro).pack(pady=10)
tk.Button(ventana, text="📌 Estado de lectura", width=25, command=abrir_estado).pack(pady=10)
tk.Button(ventana, text="📊 Ver reportes", width=25, command=abrir_reportes).pack(pady=10)

ventana.mainloop()