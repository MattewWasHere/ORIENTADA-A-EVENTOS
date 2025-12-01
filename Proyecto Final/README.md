
IHEP - Proyecto final entregable (JSON backup)

INSTRUCCIONES RÁPIDAS:

1) Crear y activar virtualenv
   python -m venv .venv
   .\.venv\Scripts\activate    (Windows)
   source .venv/bin/activate     (Linux/Mac)

2) Instalar dependencias:
   pip install django djangorestframework requests tkcalendar

3) Ejecutar backend:
   cd backend
   python manage.py migrate
   python manage.py loaddata initial_data.json

   python manage.py runserver

4) Ejecutar frontend (desde la raíz del ZIP):
   python -m frontend.main

Notas:
- El archivo db.sqlite3 ya está pre-cargado en backend/
- Las copias de seguridad automáticas se guardan en frontend/backups/backup.json
- No se usan llaves foráneas: Prestamo referencia herramientas por 'herramienta_codigo'



##  Autores
- Jhon Sebastian Bermúdez  
- Anyelo Jader Ladino

---

##  Requisitos
- Python 3.10 o superior  
- pip  
- Git  
- Entorno virtual (recomendado)
