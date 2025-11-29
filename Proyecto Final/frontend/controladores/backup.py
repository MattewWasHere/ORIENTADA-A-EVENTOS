import json
import os
from datetime import datetime


class BackupController:
    def __init__(self, herramienta_model, prestamo_model):
        self.herr_model = herramienta_model
        self.pres_model = prestamo_model
        self.ruta_backup = "backups"

        if not os.path.exists(self.ruta_backup):
            os.makedirs(self.ruta_backup)

    def ejecutar_backup(self):
        try:
            herramientas = self.herr_model.listar()
            prestamos = self.pres_model.listar()

            if isinstance(herramientas, tuple):
                herramientas = herramientas[0]

            if isinstance(prestamos, tuple):
                prestamos = prestamos[0]

            datos = {
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "herramientas": herramientas,
                "prestamos": prestamos
            }

            nombre = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            ruta = os.path.join(self.ruta_backup, nombre)

            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)

        except Exception as e:
            print(f"Error backup: {e}")
