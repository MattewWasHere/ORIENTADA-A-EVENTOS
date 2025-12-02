from frontend.controladores.api_client import get_herramientas, create_herramienta, update_herramienta, delete_herramienta

class HerramientaModel:
    def listar(self):
        return get_herramientas()

    def crear(self, data):
        return create_herramienta(data)

    def actualizar(self, codigo, data):
        return update_herramienta(codigo, data)

    def actualizar_estado(self, codigo, estado):
        return update_herramienta(codigo, {"estado": estado})

    def eliminar(self, codigo):
        return delete_herramienta(codigo)
