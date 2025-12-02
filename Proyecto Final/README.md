IHEP - Sistema de Herramientas y Préstamos. Proyecto Final (Backend Django + Frontend Tkinter).
........................................
Descripción.
Este proyecto implementa un sistema para gestionar herramientas y préstamos. Incluye un backend REST en Django y un frontend de escritorio con Tkinter. Tiene respaldo automático (JSON) y carga de datos precargados (fixtures / db.sqlite3). No usa llaves foráneas; las relaciones se manejan por código (ej.: 'herramienta_codigo' en prestamos).
........................................
Estructura principal de carpetas y archivos (rutas relativas dentro del ZIP).
backend/. (proyecto Django).
backend/api/ (app con models, views, serializers, urls, admin).
backend/manage.py.
backend/db.sqlite3 (opcional - base de datos precargada).
backend/api/fixtures/initial_data.json (datos iniciales).
frontend/. (app Tkinter).
frontend/vista/ o frontend/vistas/ (interfaz gráfica).
frontend/modelos/ (adaptadores para llamar al API).
frontend/controladores/ (backup, api_client, etc).
frontend/backups/ (respaldos automáticos).
README.md (este archivo).
........................................
Requisitos mínimos.
- Python 3.10+ instalado.
- pip.
- Git (opcional para control de versiones).
- Entorno virtual recomendado (.venv).
Dependencias principales: django, djangorestframework, requests, tkcalendar.
........................................
Instalación y puesta en marcha (Windows). Ejecutar desde la raíz del proyecto.
1) Crear y activar entorno virtual:
   python -m venv .venv
   .venv\Scripts\activate
2) Instalar dependencias:
   pip install django djangorestframework requests tkcalendar
3) Preparar y arrancar backend:
   cd backend
   python manage.py migrate
   python manage.py loaddata api/fixtures/initial_data.json   (si tienes fixtures)
   python manage.py runserver
   (Backend en http://127.0.0.1:8000/)
4) Ejecutar frontend (desde la raíz del proyecto):
   python -m frontend.main
   (La interfaz conectará contra http://127.0.0.1:8000/api/ por defecto).
........................................
Notas útiles si algo falla.
- Si el comando `loaddata` falla por campos de fecha o campos faltantes revisa `backend/api/models.py` y `backend/api/fixtures/initial_data.json` para que los nombres de campo coincidan exactamente y las fechas de DateField estén en formato YYYY-MM-DD.
- Si migraciones o modelos cambian: desde backend ejecutar:
   python manage.py makemigrations
   python manage.py migrate
- Si la API devuelve 500 o 400: revisar la consola donde corre `python manage.py runserver` para ver el traceback y qué campo pide el serializer.
- Si borraste `db.sqlite3` y quieres cargar fixtures: borra migraciones antiguas si es necesario, luego `makemigrations` → `migrate` → `loaddata`.
- Asegúrate de tener el servidor Django corriendo antes de iniciar el frontend. Los errores de conexión (WinError 10061) aparecen cuando el frontend no encuentra el backend.
........................................
Funcionamiento principal en la interfaz.
- Pestaña "Herramientas": crear / editar / eliminar herramientas. Campos: codigo, nombre, tipo, ubicacion, estado.
- Pestaña "Préstamos": registrar préstamo (herramienta por su código), persona entrega, persona recibe, fecha_entrega, fecha_prevista. Al devolver se registra fecha_devolucion y cambia el estado de la herramienta a disponible.
- Pestaña "Búsqueda": buscar por código, nombre o estado.
- Respaldo automático: se guarda un JSON en frontend/backups/ cada 60 segundos (o según configuración).
........................................
Rutas API esperadas (por defecto).
GET  /api/herramientas/          -> listar herramientas.
POST /api/herramientas/          -> crear herramienta.
PUT  /api/herramientas/{codigo}/ -> actualizar por codigo.
DELETE /api/herramientas/{codigo}/ -> eliminar.
GET  /api/prestamos/             -> listar prestamos.
POST /api/prestamos/             -> crear prestamo.
PUT  /api/prestamos/{id}/        -> actualizar prestamo (devolucion).
DELETE /api/prestamos/{id}/      -> eliminar prestamo.
........................................
Precargado de datos.
- Si quieres que la app abra con datos precargados hay dos opciones:
  1) Mantener `backend/db.sqlite3` ya pre-cargado en la carpeta backend/ (no necesitas `loaddata`).
  2) Si no hay db precargada, ejecutar en backend:
     python manage.py migrate
     python manage.py loaddata api/fixtures/initial_data.json
  - Asegúrate que `initial_data.json` use los nombres de campo y formatos correctos para tus modelos.
  - Fixtures: al usar DateField las fechas deben ser YYYY-MM-DD. Datetimes deben coincidir con DateTimeField si los usas.
........................................
Consejos rápidos para depuración.
- Si el frontend da 400 al crear un préstamo: revisa la respuesta JSON del backend (la consola del runserver mostrará qué campo falta). Muchos errores vienen por campos requeridos en serializers (ej: 'responsable' obligatorio).
- Si el backend da error de columna no encontrada: puede que debas volver a crear la DB o aplicar migraciones (migrate). Borrar `db.sqlite3` y re-migrar+loaddata suele arreglar discrepancias.
- Para editar ubicaciones o campos: comprueba que el serializer permita esos campos (no sean read_only) y que el frontend envíe exactamente las claves esperadas.
........................................
Autores.
Jhon Sebastian Bermúdez.
Anyelo Jader Ladino.
........................................
Licencia / Nota final.
Este proyecto es entrega final para la asignatura. Está pensado para uso local y pruebas. No desplegar en producción sin cambios adicionales de seguridad y configuración.
........................................
Pasos resumen rápido (copy-paste).
1) python -m venv .venv
2) .venv\Scripts\activate
3) pip install django djangorestframework requests tkcalendar
4) cd backend
5) python manage.py migrate
6) python manage.py loaddata api/fixtures/initial_data.json
7) python manage.py runserver
8) desde la raíz: python -m frontend.main
........................................
Fin del README.

