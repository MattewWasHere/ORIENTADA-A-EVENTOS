import json, os
from datetime import datetime
from threading import Lock

# ============================================================
#   CONFIGURACIÓN DE DIRECTORIO DE RESPALDOS
# ============================================================
# Se crea automáticamente la carpeta /backups/ si no existe.
# Aquí se almacenarán todos los archivos JSON generados.
BACKUP_DIR = os.path.join(os.path.dirname(__file__), "..", "backups")
os.makedirs(BACKUP_DIR, exist_ok=True)

# Evita que dos hilos accedan al backup al mismo tiempo.
LOCK = Lock()


# ============================================================
#                 CONTROLADOR DE RESPALDOS
# ============================================================
class BackupController:
    """
    Controlador encargado de generar respaldos locales.
    Este módulo:

    - Solicita los datos al modelo de Herramientas y Préstamos.
    - Crea un archivo JSON con la información completa.
    - Incluye un timestamp ISO para identificar el respaldo.
    - Funciona de forma segura gracias a un candado (LOCK).
    """

    def __init__(self, herr_model, pres_model):
        """
        Inicializa el controlador con los modelos necesarios.

        :param herr_model: Modelo de herramientas con método listar()
        :param pres_model: Modelo de préstamos con método listar()
        """
        self.herr_model = herr_model
        self.pres_model = pres_model

    # ------------------------------------------------------------
    # Métodos públicos
    # ------------------------------------------------------------
    def ejecutar_backup(self):
        """Alias público. Ejecuta un respaldo inmediatamente."""
        return self._hacer()

    def hacer_backup(self):
        """Segundo alias público para compatibilidad."""
        return self._hacer()

    # ------------------------------------------------------------
    # Lógica principal del backup (método privado)
    # ------------------------------------------------------------
    def _hacer(self):
        """
        Ejecuta el proceso completo de creación del archivo JSON.

        - Bloquea la operación para evitar conflictos entre hilos.
        - Obtiene datos de herramientas y préstamos.
        - Construye un contenedor estructurado.
        - Genera un archivo timestamped en /backups/.
        - Retorna la ruta del archivo creado.
        """

        with LOCK:  # Garantiza seguridad si el hilo automático está activo
            # Obtener datos desde los modelos
            h = self.herr_model.listar()
            p = self.pres_model.listar()

            # Construcción de estructura JSON final
            data = {
                "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "herramientas": h,
                "prestamos": p
            }

            # Nombre del archivo con timestamp YYYYMMDD_HHMMSS
            path = os.path.join(
                BACKUP_DIR,
                f"backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
            )

            # Escritura del archivo JSON
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return path
