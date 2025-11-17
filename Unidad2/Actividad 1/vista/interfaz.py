import tkinter as tk
from tkinter.messagebox import askyesno
from controladores.validaciones import Validaciones

class Interfaz():
    def mostrar_interfaz():
        root = tk.Tk()
        root.title("Registro de Estudiantes")
        root.geometry("565x410")
        root.resizable(0,0)
        root.config(padx=5, pady=20)

        variables = {
            'nombre': tk.StringVar(root),
            'apellido': tk.StringVar(root),
            'correo': tk.StringVar(root),
            'fecha_matricula': tk.StringVar(root)
        }

        errores = {
            'nombre': tk.StringVar(root),
            'apellido': tk.StringVar(root),
            'correo': tk.StringVar(root),
            'fecha_matricula': tk.StringVar(root)
        }

        validador = Validaciones(variables, errores)
        
        def el_usuario_quiere_salir():
            if askyesno("Salir de la aplicación", "¿Estás seguro que quieres cerrar la aplicación?"):
                root.destroy()

        tk.Label(root, text="Nombre").grid(row=0, column=0, pady=(0, 20), sticky="w")
        entry_nombre = tk.Entry(root, textvariable=variables['nombre'])
        entry_nombre.grid(row=0, column=1, padx=(170, 0), pady=(0, 20), sticky="e")
        tk.Label(root, textvariable=errores['nombre'], fg="#c1121f").grid(row=1, column=1, sticky="w", pady=(0,6))

        tk.Label(root, text="Apellido").grid(row=2, column=0, pady=(0, 20), sticky="w")
        entry_apellido = tk.Entry(root, textvariable=variables['apellido'])
        entry_apellido.grid(row=2, column=1, pady=(0, 20), padx=(170, 0))
        tk.Label(root, textvariable=errores['apellido'], fg="#c1121f").grid(row=3, column=1, sticky="w", pady=(0,6))

        tk.Label(root, text="Correo Electrónico").grid(row=4, column=0, pady=(0, 20), sticky="w")
        entry_correo = tk.Entry(root, textvariable=variables['correo'])
        entry_correo.grid(row=4, column=1, pady=(0, 20), padx=(170, 0))
        tk.Label(root, textvariable=errores['correo'], fg="#c1121f").grid(row=5, column=1, sticky="w", pady=(0,6))

        tk.Label(root, text="Fecha de Matrícula").grid(row=6, column=0, pady=(0, 20), sticky="w")
        entry_fecha = tk.Entry(root, textvariable=variables['fecha_matricula'])
        entry_fecha.grid(row=6, column=1, pady=(0, 20), padx=(170, 0))
        tk.Label(root, textvariable=errores['fecha_matricula'], fg="#c1121f").grid(row=7, column=1, sticky="w", pady=(0,6))

        frame_botones = tk.Frame(root)
        frame_botones.grid(row=8, column=0, columnspan=2)
        
        frame_interno = tk.Frame(frame_botones)
        frame_interno.pack(expand=True)

        tk.Button(frame_interno, 
                 text="Registrar Estudiante",
                 command=validador.enviar,
                 bg="#4CAF50",
                 fg="white",
                 width=15,
                 height=1).pack(side=tk.LEFT, padx=10)

        tk.Button(frame_interno,
                 text="Limpiar",
                 command=validador.limpiar_campos_texto,
                 bg="#f44336",
                 fg="white",
                 width=15,
                 height=1).pack(side=tk.LEFT, padx=10)

        entry_nombre.bind("<KeyRelease>", lambda e: validador.val_nombre())
        entry_apellido.bind("<KeyRelease>", lambda e: validador.val_apellido())
        entry_correo.bind("<KeyRelease>", lambda e: validador.val_correo())
        entry_fecha.bind("<KeyRelease>", lambda e: validador.val_fecha_matricula())

        root.protocol("WM_DELETE_WINDOW", el_usuario_quiere_salir)

        root.mainloop()