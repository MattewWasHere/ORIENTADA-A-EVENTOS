from .api_cliente import APIClient
from .herramienta import HerramientaModel

class PrestamoModel:
    def __init__(self):
        self.api = APIClient("http://127.0.0.1:8000/api/prestamos/")
        self.herr_model = HerramientaModel()

    def listar(self):
        try:
            data = self.api.get()
            return data, None
        except Exception as e:
            return [], str(e)

    def crear(self, data):
        try:
            herramienta, err = self.herr_model.obtener(data["herramienta_codigo"])
            if not herramienta:
                return None, "Herramienta no existe"

            payload = {
                "herramienta": herramienta["id"],
                "usuario": data["usuario"],
                "fecha_salida": data["fecha_salida"],
                "fecha_prevista": data["fecha_prevista"]
            }

            return self.api.post(payload), None
        except Exception as e:
            return None, str(e)

    def devolver(self, prestamo_id):
        try:
            return self.api.patch(prestamo_id, {"fecha_devolucion": "hoy"}), None
        except Exception as e:
            return None, str(e)
