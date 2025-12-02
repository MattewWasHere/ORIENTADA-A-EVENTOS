IHEP - Sistema de Herramientas y Préstamos. Proyecto Final (Backend Django + Frontend Tkinter).
##

##
Descripción.
Este proyecto implementa un sistema para gestionar herramientas y préstamos. Incluye un backend REST en Django y un frontend de escritorio con Tkinter. Tiene respaldo automático (JSON) y carga de datos precargados (fixtures / db.sqlite3). No usa llaves foráneas; las relaciones se manejan por código (ej.: 'herramienta_codigo' en préstamos).
##

##
Estructura principal de carpetas y archivos (rutas relativas dentro del ZIP).
##
backend/. (proyecto Django)
backend/api/ (app con models, views, serializers, urls, admin)
backend/manage.py
backend/db.sqlite3 (base de datos precargada)
backend/api/fixtures/initial_data.json (datos iniciales)
frontend/. (aplicación Tkinter)
frontend/vista/ o frontend/vistas/ (interfaz gráfica)
frontend/modelos/ (adaptadores hacia la API REST)
frontend/controladores/ (backup, api_client, lógica)
frontend/backups/ (respaldos automáticos JSON)
README.md (este archivo)
##

##
Requisitos mínimos.
##
Python 3.10 o superior  
pip  
Git  
Entorno virtual recomendado (.venv)

##
Dependencias principales:  
##
django, djangorestframework, requests, tkcalendar

##
Instalación y puesta en marcha (Windows).
1) Crear y activar entorno virtual desde la raíz del proyecto:
   python -m venv .venv
   .venv\Scripts\activate

2) Instalar dependencias:
   pip install django djangorestframework requests tkcalendar

3) Preparar y arrancar backend:
   cd backend
   python manage.py migrate
   python manage.py loaddata api/fixtures/initial_data.json   (si existe)
   python manage.py runserver
   (Backend en: http://127.0.0.1:8000/)

4) Ejecutar frontend (desde la raíz del proyecto):
   python -m frontend.main
   ##


##
Notas útiles de ejecución.
- Si el comando `loaddata` falla, revisa las fechas y los campos del modelo.  
- Si cambiaste modelos, ejecuta:
      python manage.py makemigrations
      python manage.py migrate
- Si el frontend no abre datos, verifica que el backend esté encendido.  
- Si ves error 400 en préstamos, falta algún campo obligatorio.  
........................................
Funcionamiento general de la interfaz.
- Herramientas:
  Crear / editar / eliminar herramientas  
  Campos: código, nombre, tipo, ubicación, estado

- Préstamos:
  Registrar préstamo (por código de herramienta)
  Registrar devolución
  Fechas automáticas, estado actualizado en base de datos

- Búsqueda:
  Buscar herramientas por código, nombre o estado

- Respaldo automático:
  Guarda un backup JSON cada 60 segundos en:
     frontend/backups/
##

##
Rutas REST del backend.
GET    /api/herramientas/  
POST   /api/herramientas/  
PUT    /api/herramientas/{codigo}/  
DELETE /api/herramientas/{codigo}/  

GET    /api/prestamos/  
POST   /api/prestamos/  
PUT    /api/prestamos/{id}/  
DELETE /api/prestamos/{id}/  
##

##
Precargado de datos.
- Puedes usar la base de datos incluida (db.sqlite3).  
- Si quieres regenerar desde cero:
      python manage.py migrate
      python manage.py loaddata api/fixtures/initial_data.json

El fixture debe usar campos correctos y formato de fecha YYYY-MM-DD.
##


##
Depuración rápida.
- Error 400 → falta un campo en el POST/PUT.  
- Error 500 → revisar consola del runserver.  
- Error al editar ubicación → revisar serializer permita escritura.  
- Error de conexión → backend apagado.  
##

##
Autores.
Jhon Sebastian Bermúdez  
Anyelo Jader Ladino  
##


##
Pasos ultra rápidos.
1) python -m venv .venv
2) .venv\Scripts\activate
3) pip install django djangorestframework requests tkcalendar
4) cd backend
5) python manage.py migrate
6) python manage.py loaddata api/fixtures/initial_data.json
7) python manage.py runserver
8) python -m frontend.main
##

JhoonyWasHere 


