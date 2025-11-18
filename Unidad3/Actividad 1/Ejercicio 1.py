import threading
import time

def tarea(nombre, duracion):
    print(f"[{nombre}] Iniciando tarea (durará {duracion} s)...")
    time.sleep(duracion)
    print(f"[{nombre}] Tarea finalizada.")

def main():
    # Se crean tres hilos con distintas duraciones
    hilo1 = threading.Thread(target=tarea, args=("Tarea-1", 1.2))
    hilo2 = threading.Thread(target=tarea, args=("Tarea-2", 0.8))
    hilo3 = threading.Thread(target=tarea, args=("Tarea-3", 1.5))

    # Aqui se inician todos los hilos
    hilo1.start()
    hilo2.start()
    hilo3.start()

    # Aqui se espera a que todos terminen
    hilo1.join()
    hilo2.join()
    hilo3.join()

    print("Todas las tareas fueron completadas correctamente.")
    print("©Jhon Sebastian Bermudez made this...©")

if __name__ == "__main__":
    main()
