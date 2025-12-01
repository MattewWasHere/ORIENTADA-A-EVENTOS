from frontend.vista.interfaz_principal import InterfazPrincipal

def iniciar_aplicacion():
    app = InterfazPrincipal()
    app.mainloop()

if __name__ == '__main__':
    iniciar_aplicacion()
