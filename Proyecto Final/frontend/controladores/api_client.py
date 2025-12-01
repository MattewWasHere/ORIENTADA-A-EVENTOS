import os
import requests

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/api")
TIMEOUT = 6


def get_herramientas():
    r = requests.get(f"{API_URL}/herramientas/", timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def create_herramienta(data):
    r = requests.post(f"{API_URL}/herramientas/", json=data, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def update_herramienta(codigo, data):
    r = requests.patch(f"{API_URL}/herramientas/{codigo}/", json=data, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def delete_herramienta(codigo):
    r = requests.delete(f"{API_URL}/herramientas/{codigo}/", timeout=TIMEOUT)
    return r.status_code


def get_prestamos():
    r = requests.get(f"{API_URL}/prestamos/", timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()

def create_prestamo(data):
    import json
    print("\n\n========== DEBUG CREAR PRESTAMO ==========")
    print("DATA ENVIADA:")
    print(json.dumps(data, indent=2))

    url = f"{API_URL}/prestamos/"
    print("URL:", url)

    r = requests.post(url, json=data)

    print("STATUS CODE:", r.status_code)
    print("RESPUESTA BACKEND:")
    try:
        print(r.json())
    except:
        print(r.text)

    print("==========================================\n\n")

    r.raise_for_status()
    return r.json()






def update_prestamo(pid, data):
    # Use PATCH to allow partial updates (fecha_devolucion solo)
    r = requests.patch(f"{API_URL}/prestamos/{pid}/", json=data, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def delete_prestamo(pid):
    r = requests.delete(f"{API_URL}/prestamos/{pid}/", timeout=TIMEOUT)
    return r.status_code
