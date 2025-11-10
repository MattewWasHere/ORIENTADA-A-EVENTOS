import threading
import queue
import time
import random

class GeneradorTareas(threading.Thread):
    def __init__(self, q, n, consumidores):
        super().__init__()
        self.q = q
        self.n = n
        self.consumidores = consumidores

    def run(self):
        for i in range(1, self.n + 1):
            print(f"[Productor] Generando número: {i}")
            self.q.put(i)
            time.sleep(random.uniform(0.3, 0.7))  

        
        for _ in range(self.consumidores):
            self.q.put(None)

        print("[Productor] Producción finalizada. Se enviaron centinelas.")


class Trabajador(threading.Thread):
    def __init__(self, q, nombre):
        super().__init__()
        self.q = q
        self.nombre = nombre

    def run(self):
        while True:
            item = self.q.get()  # Espera por un número o un centinela
            if item is None:     # Si recibe el centinela, termina
                print(f"[{self.nombre}] Recibió centinela. Finalizando.")
                self.q.task_done()
                break

            resultado = item ** 2
            print(f"[{self.nombre}] Procesó {item} --> {resultado}")
            time.sleep(random.uniform(0.5, 1.0))  # Simula trabajo de procesamiento
            self.q.task_done()


def main():
    q = queue.Queue()
    n = 10
    num_consumidores = 3

    productor = GeneradorTareas(q, n, num_consumidores)
    consumidores = [Trabajador(q, f"Consumidor-{i+1}") for i in range(num_consumidores)]

    # Inicia los hilos
    productor.start()
    for c in consumidores:
        c.start()

    # Espera a que todos los trabajos finalicen
    productor.join()
    q.join()  # Espera a que todos los ítems sean procesados

    print("\n[TODOS] Todas las tareas fueron procesadas correctamente.\n")


if __name__ == "__main__":
    main()
