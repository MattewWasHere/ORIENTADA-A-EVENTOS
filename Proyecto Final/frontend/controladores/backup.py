import json, os
from datetime import datetime
from threading import Lock

BACKUP_DIR = os.path.join(os.path.dirname(__file__), "..", "backups")
os.makedirs(BACKUP_DIR, exist_ok=True)
LOCK = Lock()

class BackupController:
    def __init__(self, herr_model, pres_model):
        self.herr_model = herr_model
        self.pres_model = pres_model

    def ejecutar_backup(self):
        return self._hacer()

    def hacer_backup(self):
        return self._hacer()

    def _hacer(self):
        with LOCK:
            h = self.herr_model.listar()
            p = self.pres_model.listar()
            data = {
                "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "herramientas": h,
                "prestamos": p
            }
            path = os.path.join(BACKUP_DIR, f"backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return path
