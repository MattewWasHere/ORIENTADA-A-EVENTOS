import json
import os
from datetime import datetime
from threading import Lock

# Ruta a la carpeta de backups
BACKUP_DIR = os.path.join(os.path.dirname(__file__), "..", "backups")
os.makedirs(BACKUP_DIR, exist_ok=True)

# Lock para evitar que varios hilos escriban a la vez
LOCK = Lock()


class BackupController:
    def __init__(self, herr_model, pres_model):
        self.herr_model = herr_model
        self.pres_model = pres_model

    def _generar_respaldo(self):
        """Genera el contenido del backup (herramientas + préstamos)."""
        herramientas = self.herr_model.listar()
        prestamos = self.pres_model.listar()

        return {
            "herramientas": herramientas,
            "prestamos": prestamos,
            "generado": datetime.utcnow().isoformat()
        }

    def hacer_backup(self):
        """Método llamado desde la interfaz."""
        return self.ejecutar_backup()

    def ejecutar_backup(self):
        """Crea el archivo JSON de respaldo y devuelve la ruta."""
        with LOCK:
            data = self._generar_respaldo()

            filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            path = os.path.join(BACKUP_DIR, filename)

            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return path
