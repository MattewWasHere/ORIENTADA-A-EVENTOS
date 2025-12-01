
from frontend.controladores.api_client import get_herramientas, create_herramienta, update_herramienta, delete_herramienta
class HerramientaModel:
    def listar(self):
        return get_herramientas()
    def crear(self, data):
        return create_herramienta(data)
    def actualizar(self, codigo, data):
        return update_herramienta(codigo, data)
    def eliminar(self, codigo):
        return delete_herramienta(codigo)
    def actualizar_estado(self, codigo, estado):
        herrs = self.listar()
        for h in herrs:
            if h.get('codigo') == codigo:
                h['estado'] = estado
                try:
                    return update_herramienta(codigo, h)
                except Exception:
                    return None
        return None
