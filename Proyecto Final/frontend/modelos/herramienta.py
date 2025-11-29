import requests


class HerramientaModel:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/api/"

    def listar(self):
        try:
            response = requests.get(f"{self.base_url}herramientas/")
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print("Error al listar herramientas:", e)
            return []

    def crear(self, datos):
        try:
            response = requests.post(
                f"{self.base_url}herramientas/",
                json=datos
            )
            return response.status_code in (200, 201)
        except Exception as e:
            print("Error al crear herramienta:", e)
            return False

    def eliminar(self, herramienta_id):
        try:
            response = requests.delete(
                f"{self.base_url}herramientas/{herramienta_id}/"
            )
            return response.status_code == 204
        except Exception as e:
            print("Error al eliminar herramienta:", e)
            return False

    def actualizar_estado(self, herramienta_id, nuevo_estado):
        try:
            response = requests.patch(
                f"{self.base_url}herramientas/{herramienta_id}/",
                json={"estado": nuevo_estado}
            )

            if response.status_code not in (200, 204):
                print("Respuesta:", response.text)
                return False

            return True
        except Exception as e:
            print("Error al actualizar estado:", str(e))
            return False
