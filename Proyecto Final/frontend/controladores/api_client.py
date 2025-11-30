import os, requests
API_URL = os.getenv('API_URL', 'http://127.0.0.1:8000/api')
TIMEOUT = 8

def get_herramientas():
    r = requests.get(f"{API_URL}/herramientas/", timeout=TIMEOUT); r.raise_for_status(); return r.json()

def create_herramienta(data):
    r = requests.post(f"{API_URL}/herramientas/", json=data, timeout=TIMEOUT); r.raise_for_status(); return r.json()

def update_herramienta(codigo, data):
    r = requests.put(f"{API_URL}/herramientas/{codigo}/", json=data, timeout=TIMEOUT); r.raise_for_status(); return r.json()

def delete_herramienta(codigo):
    r = requests.delete(f"{API_URL}/herramientas/{codigo}/", timeout=TIMEOUT); return r.status_code

def get_prestamos():
    r = requests.get(f"{API_URL}/prestamos/", timeout=TIMEOUT); r.raise_for_status(); return r.json()


def create_prestamo(data):
    data=dict(data)
    data.pop('consecutivo',None)
    r=requests.post(f"{API_URL}/prestamos/", json=data, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def update_prestamo(numero, data):
    r = requests.put(f"{API_URL}/prestamos/{numero}/", json=data, timeout=TIMEOUT); r.raise_for_status(); return r.json()

def delete_prestamo(numero):
    r = requests.delete(f"{API_URL}/prestamos/{numero}/", timeout=TIMEOUT); return r.status_code
