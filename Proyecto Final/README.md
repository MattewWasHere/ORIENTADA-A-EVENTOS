IHEP - Inventario de Herramientas y Préstamos (Entrega final - versión v5)
Generado: 2025-11-29T21:02:07.462677 UTC

Instrucciones para ejecutar en Visual Studio / Visual Studio Code:

1) Abrir la carpeta del proyecto (IHEP_Final_Entrega_v5) en VS Code.
2) Crear y activar un entorno virtual Python 3.10+:
   python -m venv .venv
   # Windows:
   .\.venv\Scripts\activate
   # mac/linux:
   source .venv/bin/activate
3) Instalar dependencias:
   pip install -r requirements.txt
4) Iniciar backend:
   cd backend
   python manage.py migrate
   python manage.py loaddata initial_data.json
   python manage.py runserver
5) Iniciar frontend (en otra terminal dentro del workspace raíz):
   cd frontend
   python -m frontend
6) Comprobar backups: revisa frontend/backups/*.json (se crean automáticamente según INTERVALO_BACKUP_SEG en frontend/config.json)

Notas importantes:
- El frontend usa tkinter y realiza validaciones de formulario (según PDF: validaciones en UI).
- El backend expone endpoints REST para CRUD sin lógica de negocio compleja.
- Para la sustentación, muestra los 5 registros pre-cargados en la base de datos (backend/initial_data.json).
