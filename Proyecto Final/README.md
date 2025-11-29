
# IHEP - Inventario de Herramientas y Préstamos

## Resumen
Proyecto solicitado en RFP IHEP. Frontend en Tkinter y backend en Django REST Framework. No se usan llaves foráneas en la BD. Respaldo automático configurable.

## Requisitos
- Python 3.10+
- Django 4.x, djangorestframework
- requests (para frontend)

## Cómo ejecutar

1. Backend:
```bash
cd backend
python -m venv env
source env/bin/activate  # o .\env\Scripts\activate en Windows
pip install -r requirements.txt  # si existe; si no: pip install django djangorestframework
python manage.py migrate
python manage.py runserver
```

2. Frontend (en otra terminal, desde la raíz del proyecto):
```bash
python __main__.py
```

Variables de entorno:
- `BACKEND_URL` o `API_URL` (el frontend usa `BACKEND_URL`) para apuntar al backend si no es `http://127.0.0.1:8000/api/`
- `INTERVALO_BACKUP_SEG` intervalo en segundos para los respaldos (por defecto 60)

Los respaldos se almacenan en `frontend/backups/`. Se incluye `example_respaldo.json` como ejemplo.

## Notas
- La integridad entre herramientas y préstamos se valida en el backend y el frontend sin usar ForeignKey.
- El respaldo automático corre en un hilo separado para no bloquear la UI.
