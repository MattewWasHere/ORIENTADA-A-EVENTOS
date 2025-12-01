from frontend.controladores.api_client import (
    get_prestamos,
    create_prestamo,
    update_prestamo,
    delete_prestamo,
)


class PrestamoModel:
    def listar(self):
        return get_prestamos()

    def crear(self, data):
        return create_prestamo(data)

    def actualizar(self, pid, data):
        return update_prestamo(pid, data)

    def eliminar(self, pid):
        return delete_prestamo(pid)
