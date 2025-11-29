import os, requests
API_URL = os.getenv('API_URL', 'http://127.0.0.1:8000/api')
TIMEOUT = 8

def obtener_herramienta():
    r = requests.get(f"{API_URL}/herramientas/", timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()

def crear_herramienta(data):
    r = requests.post(f"{API_URL}/herramientas/", json=data, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()

def actualizar_herramienta(codigo, data):
    r = requests.put(f"{API_URL}/herramientas/{codigo}/", json=data, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()

def eliminar_herramienta(codigo):
    r = requests.delete(f"{API_URL}/herramientas/{codigo}/", timeout=TIMEOUT)
    return r.status_code

def obtener_prestamos():
    r = requests.get(f"{API_URL}/prestamos/", timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()

def crear_prestamo(data):
    r = requests.post(f"{API_URL}/prestamos/", json=data, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()

def actualizar_prestamo(numero, data):
    r = requests.put(f"{API_URL}/prestamos/{numero}/", json=data, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()

def eliminar_prestamo(numero):
    r = requests.delete(f"{API_URL}/prestamos/{numero}/", timeout=TIMEOUT)
    return r.status_code
