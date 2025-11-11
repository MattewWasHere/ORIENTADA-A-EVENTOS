Proyecto Estudiantes - Estructura y ejecución

Estructura principal:
proyecto_estudiantes/
├─ backend/                <-- carpeta del backend Django
│  ├─ manage.py
│  └─ backend_django/      <-- settings, urls, wsgi
│  └─ estudiantes/         <-- app con modelos y API
└─ frontend/
   └─ main.py              <-- GUI Tkinter con Treeview

Cómo ejecutar en Windows (sin entorno virtual):
1) Abrir terminal y situarse en la carpeta 'backend':
   cd path\to\proyecto_estudiantes\backend
2) Instalar dependencias si no las tienes:
   pip install django djangorestframework requests
3) Crear migraciones y aplicar:
   python manage.py makemigrations
   python manage.py migrate
4) Correr el servidor:
   python manage.py runserver
5) En otra terminal, ejecutar la GUI (desde la raíz del proyecto):
   python frontend\main.py

Nota: si usas entorno virtual, actívalo antes de instalar dependencias.
