IHEP – Sistema de Herramientas y Préstamos
Proyecto Final – Backend (Django) + Frontend (Tkinter)

Este proyecto implementa un sistema completo para la gestión de herramientas, registro de préstamos, devoluciones, inventario y copias de seguridad automáticas. Incluye un backend en Django (API REST) y un frontend en Tkinter.

1. Estructura del Proyecto
##
Proyecto Final/
│── backend/
│   ├── api/                     # API REST (views, serializers, URLs)
│   ├── db.sqlite3               # Base de datos precargada
│   ├── manage.py
│
│── frontend/
│   ├── vista/                   # Interfaz gráfica Tkinter
│   ├── modelos/                 # Conexión con el backend
│   ├── controladores/           # Lógica de respaldo
│   ├── backups/                 # Respaldos automáticos JSON
│
│── initial_data.json            # Datos iniciales (fixtures)
│── README.md
##
3. Requisitos

Python 3.10 o superior

pip

Git

Entorno virtual (opcional pero recomendado)

Dependencias:

django
djangorestframework
requests
tkcalendar

3. Instalación del Proyecto
3.1 Crear y activar entorno virtual

Windows:

python -m venv .venv
.venv\Scripts\activate


Linux / Mac:

python3 -m venv .venv
source .venv/bin/activate

4. Instalar dependencias
pip install django djangorestframework requests tkcalendar

5. Ejecutar el Backend

Entrar al backend:

cd backend


Aplicar migraciones:

python manage.py migrate


Cargar datos iniciales:

python manage.py loaddata initial_data.json


Iniciar el servidor:

python manage.py runserver


API disponible en:
http://127.0.0.1:8000/api/

6. Ejecutar el Frontend

Desde la raíz del proyecto:

python -m frontend.main

7. Funcionalidades del Sistema
7.1 Herramientas

Crear, editar y eliminar herramientas.

Cambios automáticos de estado.

Campos: código, nombre, tipo, ubicación, estado.

7.2 Préstamos

Registrar préstamos.

Validación de estado “disponible”.

Registrar devoluciones.

Cambio automático de estado de herramienta.

7.3 Buscador

Búsqueda por código, nombre o estado.

Resultados en tabla filtrada.

7.4 Respaldo Automático

Se genera un backup cada 60 segundos.

Ubicación:

frontend/backups/


El respaldo incluye:

Herramientas

Préstamos

Marca de tiempo

8. Diseño sin Llaves Foráneas

Según requisitos del proyecto, no se usan llaves foráneas.
Los préstamos referencian herramientas mediante:

herramienta_codigo

9. Base de Datos Incluida

db.sqlite3 contiene:

Herramientas de prueba

Préstamos de prueba

Si deseas recargar los datos iniciales:

python manage.py loaddata initial_data.json

10. Autores

Jhon Sebastian Bermúdez

Anyelo Jader Ladino

11. Licencia

Proyecto académico para fines educativos.
