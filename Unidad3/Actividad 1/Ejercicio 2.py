import threading
import time

class Temporizador(threading.Thread):
    def __init__(self, limite, reset_event, stop_event):
        super().__init__()
        self.limite = limite
        self.reset_event = reset_event
        self.stop_event = stop_event

    def run(self):
        contador = 0
        while not self.stop_event.is_set():
            print(f"[Temporizador] Tiempo: {contador}s", end="\r", flush=True)
            time.sleep(1)
            contador += 1

            # si el usuario presiona Enter, se reinicia el contador
            if self.reset_event.is_set():
                print("\n[Temporizador] Reinicio solicitado.")
                contador = 0
                self.reset_event.clear()

            # si llega al limite se detiene
            if contador >= self.limite:
                print(f"\n[Temporizador] ¡Límite de {self.limite}s alcanzado!")
                self.stop_event.set()


class Reseteichon(threading.Thread):
    def __init__(self, reset_event):
        super().__init__(daemon=True)  # Daemon para no bloquear el cierre
        self.reset_event = reset_event

    def run(self):
        while True:
            input()  # Si presiona Enter el usuario
            self.reset_event.set()


def main():
    limite = 10  #segundinhos

    # Crear los eventos de  la sincronización
    reset_event = threading.Event()
    stop_event = threading.Event()

    # Crear los hilos
    temporizador = Temporizador(limite, reset_event, stop_event)
    escucha = Reseteichon(reset_event)


    # Para iniciar hilos
    escucha.start()
    temporizador.start()

    # Esperar a que el temporizador termine
    temporizador.join()

    print("\n[TODOS] El temporizador ha finalizado.\n")


if __name__ == "__main__":
    main()
