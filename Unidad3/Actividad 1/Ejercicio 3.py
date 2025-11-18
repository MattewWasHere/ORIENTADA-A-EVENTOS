import threading
import random
import time

class Cuenta:
    def __init__(self, saldo_inicial=0):
        self.saldo = saldo_inicial
        self.lock = threading.Lock()

    def depositar(self, monto):
        with self.lock:  # Hace un Bloqueo mientras se actualiza el saldo
            saldo_anterior = self.saldo
            time.sleep(random.uniform(0.1, 0.3))  # Simula demora
            self.saldo = saldo_anterior + monto
            print(f"[Depósito] +${monto:.2f} | Saldo actual: ${self.saldo:.2f}")

    def retirar(self, monto):
        with self.lock:
            if self.saldo >= monto:
                saldo_anterior = self.saldo
                time.sleep(random.uniform(0.1, 0.3))
                self.saldo = saldo_anterior - monto
                print(f"[Retiro] -${monto:.2f} | Saldo actual: ${self.saldo:.2f}")
            else:
                print(f"[Retiro] Fondos insuficientes para retirar ${monto:.2f} | Saldo: ${self.saldo:.2f}")


class OperadorCuenta(threading.Thread):
    def __init__(self, cuenta, operaciones):
        super().__init__()
        self.cuenta = cuenta
        self.operaciones = operaciones  

    def run(self):
        for _ in range(self.operaciones):
            accion = random.choice(["depositar", "retirar"])
            monto = random.randint(10, 100)

            if accion == "depositar":
                self.cuenta.depositar(monto)
            else:
                self.cuenta.retirar(monto)

            time.sleep(random.uniform(0.30, 0.50))  # pequeña pausa entre operaciones


def main():
    # Crea una cuenta con saldo inicial
    cuenta = Cuenta(saldo_inicial=500)

    # Crea varios hilos operadores
    operadores = [OperadorCuenta(cuenta, operaciones=5) for _ in range(3)]

    # Inicia todos los hilos
    for op in operadores:
        op.start()

    # Espera a que todos terminen
    for op in operadores:
        op.join()

    print(f"\n[TODOS] Operaciones completadas. Saldo final: ${cuenta.saldo:.2f}\n")


if __name__ == "__main__":
    main()
