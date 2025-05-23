from app.logic.reports import Reports

r = Reports()

print("=== Libros leídos ===")
for row in r.libros_leidos():
    print(f"- {row['titulo']} ({row['fecha_registro']})")

print("\n=== Libros de Rosa Beltrán ===")
for row in r.libros_por_autor("Rosa Beltrán"):
    print(f"- {row['titulo']}")

print("\n=== Libros por categoría: Filosofía ===")
for row in r.libros_por_categoria("Filosofía"):
    print(f"- {row['titulo']}")

print("\n=== Estado actual de lectura ===")
for row in r.estado_lectura_actual():
    print(f"- {row['titulo']} ({row['estatus']})")

print("\n=== Resumen por estatus ===")
for row in r.resumen_por_estatus():
    print(f"{row['estatus']}: {row['total']}")

print("\n=== Libros sin comenzar ===")
for row in r.libros_sin_comenzar():
    print(f"- {row['titulo']}")