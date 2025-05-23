from app.logic.status_tracker import StatusTracker

tracker = StatusTracker()
tracker.registrar_estado(3, str("leyendo"), int(1), str("Inicio hoy."))