import uuid


class Producto:
    def __init__(self, nombre: str, precio: float, stock: int):
        # id unico generado automaticamente
        self.id = str(uuid.uuid4())
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def hay_stock(self, cantidad: int) -> bool:
        # comprueba si hay suficiente stock para la cantidad pedida
        return self.stock >= cantidad

    def actualizar_stock(self, cantidad: int) -> bool:
        # cantidad negativa = venta, positiva = reposicion
        if self.stock + cantidad < 0:
            print(f"No hay stock suficiente de {self.nombre}")
            return False
        self.stock += cantidad
        return True

    def __str__(self):
        return f"[{self.id}] {self.nombre} - {self.precio}€ (stock: {self.stock})"


class ProductoElectronico(Producto):
    def __init__(self, nombre: str, precio: float, stock: int, meses_garantia: int):
        super().__init__(nombre, precio, stock)
        self.meses_garantia = meses_garantia

    def __str__(self):
        return f"{super().__str__()} | Garantia: {self.meses_garantia} meses"


class ProductoRopa(Producto):
    def __init__(self, nombre: str, precio: float, stock: int, talla: str, color: str):
        super().__init__(nombre, precio, stock)
        self.talla = talla
        self.color = color

    def __str__(self):
        return f"{super().__str__()} | Talla: {self.talla} | Color: {self.color}"
