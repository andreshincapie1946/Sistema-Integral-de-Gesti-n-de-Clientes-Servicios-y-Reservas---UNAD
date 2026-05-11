from datetime import datetime
import os

class FileLogger:
    def __init__(self, archivo="logs/sistema.log"):
        self.archivo = archivo

        # Crear carpeta logs si no existe
        os.makedirs(os.path.dirname(self.archivo), exist_ok=True)

    def registrar_evento(self, mensaje):
        with open(self.archivo, "a", encoding="utf-8") as file:
            file.write(f"[EVENTO] {datetime.now()} - {mensaje}\n")

    def registrar_error(self, mensaje):
        with open(self.archivo, "a", encoding="utf-8") as file:
            file.write(f"[ERROR] {datetime.now()} - {mensaje}\n")

            # Excepciones de clientes
class ClienteInvalidoException(Exception):
    pass


# Excepciones de servicios
class ServicioNoDisponibleException(Exception):
    pass


# Excepciones de reservas
class ReservaInvalidaException(Exception):
    pass


# Excepción general del sistema
class SistemaException(Exception):
    pass

from utils.file_logger import FileLogger
from utils.excepciones import *

logger = FileLogger()


# =========================
# MOCKS / STUBS TEMPORALES
# =========================

class Cliente:
    def __init__(self, nombre, edad):
        if not nombre:
            raise ClienteInvalidoException("El nombre no puede estar vacío")

        if edad < 18:
            raise ClienteInvalidoException(
                "El cliente debe ser mayor de edad"
            )

        self.nombre = nombre
        self.edad = edad


class Servicio:
    def __init__(self, nombre, disponible=True):
        self.nombre = nombre
        self.disponible = disponible

    def validar_disponibilidad(self):
        if not self.disponible:
            raise ServicioNoDisponibleException(
                f"El servicio '{self.nombre}' no está disponible"
            )


class Reserva:
    def __init__(self, cliente, servicio):
        if cliente is None:
            raise ReservaInvalidaException(
                "La reserva requiere un cliente"
            )

        servicio.validar_disponibilidad()

        self.cliente = cliente
        self.servicio = servicio


# =========================
# MAIN PRINCIPAL
# =========================

def main():

    operaciones = [
        ("Juan", 20, "Sala VIP", True),
        ("", 28, "Sala A", True),
        ("Pedro", 15, "Sala B", True),
        ("Ana", 23, "Sala C", False),
        ("Luis", 30, "Sala D", True),
        ("Maria", 39, "Sala E", False),
        ("Carlos", 18, "Sala F", True),
        ("Laura", 16, "Sala G", True),
        ("Andres", 31, "Sala H", True),
        ("Sofia", 34, "Sala I", False)
    ]

    for i, op in enumerate(operaciones, start=1):

        print(f"\n--- Operación {i} ---")

        try:

            logger.registrar_evento(
                f"Iniciando operación {i}"
            )

            nombre, edad, nombre_servicio, disponible = op

            # Crear cliente
            cliente = Cliente(nombre, edad)

            logger.registrar_evento(
                f"Cliente creado: {cliente.nombre}"
            )

            # Crear servicio
            servicio = Servicio(
                nombre_servicio,
                disponible
            )

            logger.registrar_evento(
                f"Servicio creado: {servicio.nombre}"
            )

            # Crear reserva
            reserva = Reserva(cliente, servicio)

            logger.registrar_evento(
                f"Reserva exitosa para {cliente.nombre}"
            )

        except ClienteInvalidoException as e:

            logger.registrar_error(str(e))
            print(f"Error cliente: {e}")

        except ServicioNoDisponibleException as e:

            logger.registrar_error(str(e))
            print(f"Error servicio: {e}")

        except ReservaInvalidaException as e:

            logger.registrar_error(str(e))
            print(f"Error reserva: {e}")

        except Exception as e:

            # Encadenamiento de excepciones
            nueva = SistemaException(
                "Error general del sistema"
            )

            logger.registrar_error(str(nueva))

            raise nueva from e

        else:

            print("Operación completada correctamente")

        finally:

            logger.registrar_evento(
                f"Finalizó operación {i}"
            )

            print("Proceso finalizado")


if __name__ == "__main__":
    main()

    