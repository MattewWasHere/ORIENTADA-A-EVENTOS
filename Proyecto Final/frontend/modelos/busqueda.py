from .api_cliente import APIClient

class BusquedaModel:
    def __init__(self):
        self.api = APIClient()

    def buscar_herramientas(self, **params):
        query = "&".join([f"{k}={v}" for k, v in params.items()])
        return self.api.get(f"herramientas/?{query}")

    def buscar_prestamos(self, **params):
        query = "&".join([f"{k}={v}" for k, v in params.items()])
        return self.api.get(f"prestamos/?{query}")
