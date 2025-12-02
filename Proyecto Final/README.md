# IHEP – Sistema de Herramientas y Préstamos  
Proyecto Final (Backend Django + Frontend Tkinter)

  
## Descripción

Este proyecto implementa un sistema completo para la gestión de herramientas, registro de préstamos, devoluciones, inventario y copias de seguridad automáticas.  
Incluye un **backend REST en Django (API REST)** y un **frontend de escritorio en Tkinter**.

No se usan llaves foráneas; las relaciones se manejan mediante campos de texto como `herramienta_codigo`.

  
## Estructura del Proyecto (rutas dentro del ZIP)
Proyecto Final/
├── backend/
│ ├── api/ # Modelos, views, serializers, urls
│ ├── manage.py
│ ├── db.sqlite3 # Base de datos precargada (opcional)
│ └── api/fixtures/initial_data.json # Datos iniciales
│
├── frontend/
│ ├── vista/ # Interfaz gráfica (Tkinter)
│ ├── modelos/ # Conexión con el backend
│ ├── controladores/ # Lógica de respaldo y API client
│ └── backups/ # Respaldos automáticos JSON
│
└── README.md


  
## Requisitos

- Python 3.10 o superior  
- pip  
- Git (opcional)  
- Entorno virtual recomendado  

### Dependencias:
- django  
- djangorestframework  
- requests  
- tkcalendar  

  
## Instalación y Ejecución (Windows)

### 1. Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\activate

### 2. Instalar dependencias
pip install django djangorestframework requests tkcalendar

### 3. Preparar y arrancar el backend
cd backend
python manage.py migrate
python manage.py loaddata api/fixtures/initial_data.json # opcional si tienes DB vacía
python manage.py runserver
Backend disponible en:  
**http://127.0.0.1:8000/**

### 4. Ejecutar frontend (desde raíz del proyecto)
python -m frontend.main


  
## Notas importantes

- Si `loaddata` falla, revisa que las fechas del JSON estén en formato `YYYY-MM-DD`.  
- Si migraciones fallan, puedes borrar `db.sqlite3` y correr:
python manage.py makemigrations
python manage.py migrate
- Asegura que el backend esté ejecutándose antes del frontend.  
- Los respaldos automáticos se guardan cada 60 segundos en `frontend/backups/`.

........................................  
## Rutas API

### Herramientas
- `GET /api/herramientas/`
- `POST /api/herramientas/`
- `PUT /api/herramientas/{codigo}/`
- `DELETE /api/herramientas/{codigo}/`

### Préstamos
- `GET /api/prestamos/`
- `POST /api/prestamos/`
- `PUT /api/prestamos/{id}/`
- `DELETE /api/prestamos/{id}/`

........................................  
## Funciones principales del sistema

### Herramientas
- Crear, editar, eliminar herramientas.  
- Campos: código, nombre, tipo, ubicación, estado.

### Préstamos
- Registrar préstamo usando el código de herramienta.  
- Definir persona que entrega, persona que recibe, fecha de salida y fecha prevista.  
- Registrar devolución → cambia el estado y fecha de devolución.

### Búsqueda
- Buscar por código, nombre o estado.

### Respaldo automático
- Guarda un archivo JSON cada 60 segundos en `/frontend/backups/`.

  
## Solución de problemas comunes

- **Error 400 al registrar préstamo**: faltan campos requeridos (`responsable` o inconsistencia de estado).  
- **Error 500**: revisar consola donde corre `runserver`.  
- **Error al actualizar herramienta**: revisar que el serializer acepte los campos enviados.  
- **Errores de migración**: borrar DB, hacer `makemigrations` → `migrate` → `loaddata`.

  
## Autores

- Jhon Sebastian Bermúdez  
- Anyelo Jader Ladino  







