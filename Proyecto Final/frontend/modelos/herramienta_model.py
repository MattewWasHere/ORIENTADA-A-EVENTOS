from frontend.controladores.api_client import (
    get_herramientas,
    create_herramienta,
    update_herramienta,
    delete_herramienta,
)


class HerramientaModel:
    def listar(self):
        return get_herramientas()

    def crear(self, data):
        return create_herramienta(data)

    def eliminar(self, codigo):
        return delete_herramienta(codigo)

    def actualizar_estado(self, codigo, estado):
        try:
            herrs = get_herramientas()
            for h in herrs:
                if h.get("codigo") == codigo:
                    h["estado"] = estado
                    update_herramienta(codigo, h)
                    return True
        except Exception:
            pass
        return False
