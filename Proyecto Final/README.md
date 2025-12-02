
INSTRUCCIONES RÁPIDAS:

📦 IHEP – Sistema de Herramientas y Préstamos
Proyecto Final – Gestión de Herramientas, Préstamos y Respaldos Automáticos

Este proyecto implementa un sistema completo para la gestión de herramientas, registro de préstamos, devoluciones, inventario y copias de seguridad automáticas.
Incluye backend en Django (API REST) y frontend en Tkinter, con respaldo automático cada 60 segundos.

📁 Estructura General
Proyecto Final/
│── backend/          # API REST en Django
│   ├── api/          # Modelos, views, serializers, URLs
│   ├── db.sqlite3    # Base de datos precargada
│   └── manage.py
│
│── frontend/
│   ├── vista/        # Interfaz gráfica Tkinter
│   ├── modelos/      # Conexión al backend
│   ├── controladores/# Lógica de respaldo
│   └── backups/      # Respaldos automáticos
│
│── initial_data.json # Datos iniciales (fixtures)
│── README.md         # Documento actual

🚀 Instalación y Ejecución del Proyecto
1️. Crear y activar entorno virtual
Windows
python -m venv .venv
.venv\Scripts\activate

Linux / Mac
python3 -m venv .venv
source .venv/bin/activate

2️. Instalar dependencias
pip install django djangorestframework requests tkcalendar

3️. Iniciar el Backend (API Django)

4: Ir a la carpeta del backend:

cd backend


5: Ejecutar migraciones:

python manage.py migrate


6: Cargar los datos iniciales:

python manage.py loaddata initial_data.json


7: Iniciar servidor backend:

python manage.py runserver


📌 El backend queda activo en:
  http://127.0.0.1:8000/api/

 8: Ejecutar el Frontend (Interfaz Gráfica)

Desde la raíz del proyecto:

python -m frontend.main

🖥️ Funcionalidades del Sistema
🔧 Gestión de Herramientas

✔ Agregar herramientas
✔ Editar campo por campo
✔ Eliminar herramientas
✔ Actualización de estado (“disponible” / “prestada”)
✔ Campos soportados:

Código

Nombre

Tipo

Ubicación

Estado

📚 Gestión de Préstamos

✔ Registrar un préstamo
✔ Validación: solo permite prestar herramientas disponibles
✔ Registrar devolución
✔ Cambiar automáticamente el estado de la herramienta

🔍 Búsqueda Inteligente

✔ Buscar por:

Código

Nombre

Estado
✔ Tabla filtrada en tiempo real

💾 Sistema de Respaldo Automático

Una copia de seguridad se genera cada 60 segundos en:

frontend/backups/


El archivo generado incluye:

Todas las herramientas

Todos los préstamos

Fecha del respaldo

🛠️ Tecnologías Utilizadas
Backend

Django 5+

Django REST Framework

SQLite

Frontend

Tkinter

ttk Theme (estilo profesional)

tkcalendar (selector de fechas)

Otros

Requests (consumo de API)

JSON backups automáticos

📌 Notas Importantes

No se usan llaves foráneas:
El modelo Prestamo referencia herramientas usando el campo herramienta_codigo.

La base de datos incluida (db.sqlite3) ya tiene datos de prueba.

Compatible con Python 3.10+.

👥 Autores
Nombre	Rol
Jhon Sebastian Bermúdez	Desarrollo Backend & API
Anyelo Jader Ladino	Desarrollo Frontend & Lógica
(Asistencia Técnica) ChatGPT	Correcciones & Diagnóstico
📄 Licencia

Proyecto académico — uso educativo.
