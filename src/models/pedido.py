import uuid
from datetime import datetime


class Pedido:
    def __init__(self, cliente, lineas: list):
        # lineas es una lista de tuplas (producto, cantidad)
        self.id = str(uuid.uuid4())
        self.cliente = cliente
        self.lineas = lineas
        self.fecha = datetime.now()

    def calcular_total(self) -> float:
        total = 0
        for producto, cantidad in self.lineas:
            total += producto.precio * cantidad
        return total

    def __str__(self):
        detalle = ", ".join(f"{cantidad}x {producto.nombre}" for producto, cantidad in self.lineas)
        return f"Pedido [{self.id}] de {self.cliente.nombre} -> {detalle} | Total: {self.calcular_total()}€"
