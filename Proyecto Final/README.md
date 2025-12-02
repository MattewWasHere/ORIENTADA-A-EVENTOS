IHEP – Sistema de Herramientas y Préstamos
Proyecto Final – Backend (Django) + Frontend (Tkinter)

Este proyecto implementa un sistema completo para la gestión de herramientas, registro de préstamos, devoluciones, inventario y respaldo automático.
Incluye un backend en Django (API REST) y un frontend en Tkinter.

1. Estructura del Proyecto
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

2. Requisitos

Python 3.10 o superior

pip

Git

Entorno virtual (recomendado)

Dependencias:

django
djangorestframework
requests
tkcalendar

3. Instalación
Crear entorno virtual

Windows:

python -m venv .venv
.venv\Scripts\activate


Linux/Mac:

python3 -m venv .venv
source .venv/bin/activate

4. Instalar dependencias
pip install django djangorestframework requests tkcalendar

5. Ejecutar Backend (Django)
cd backend
python manage.py migrate
python manage.py loaddata initial_data.json
python manage.py runserver


API disponible en:
http://127.0.0.1:8000/api/

6. Ejecutar Frontend (Tkinter)

Desde la raíz del proyecto:

python -m frontend.main

7. Funcionalidades

Gestión completa de herramientas

Registro de préstamos

Registro de devoluciones

Cambio automático de estado (disponible/prestada)

Búsqueda por código, nombre y estado

Respaldo automático cada 60 segundos (JSON)

Backups almacenados en:

frontend/backups/

8. Autores

Jhon Sebastian Bermúdez

Anyelo Jader Ladino
