from models.pedido import Pedido
from models.producto import Producto, ProductoElectronico, ProductoRopa
from models.usuario import Administrador, Cliente


class TiendaService:
    def __init__(self):
        self.usuarios = {}
        self.productos = {}
        self.pedidos = []

    # --- usuarios ---

    def registrar_usuario(self, tipo: str, nombre: str, email: str, direccion: str = ""):
        if tipo == "cliente":
            usuario = Cliente(nombre, email, direccion)
        elif tipo == "administrador":
            usuario = Administrador(nombre, email)
        else:
            print(f"Tipo de usuario no valido: {tipo}")
            return None

        self.usuarios[usuario.id] = usuario
        return usuario

    def obtener_usuario(self, usuario_id: str):
        return self.usuarios.get(usuario_id)

    def listar_usuarios(self) -> list:
        return list(self.usuarios.values())

    # --- productos ---

    def anadir_producto(self, categoria: str, nombre: str, precio: float, stock: int,
                         meses_garantia: int = 0, talla: str = "", color: str = ""):
        if categoria == "generico":
            producto = Producto(nombre, precio, stock)
        elif categoria == "electronico":
            producto = ProductoElectronico(nombre, precio, stock, meses_garantia)
        elif categoria == "ropa":
            producto = ProductoRopa(nombre, precio, stock, talla, color)
        else:
            print(f"Categoria de producto no valida: {categoria}")
            return None

        self.productos[producto.id] = producto
        return producto

    def obtener_producto(self, producto_id: str):
        return self.productos.get(producto_id)

    def eliminar_producto(self, producto_id: str) -> bool:
        if producto_id in self.productos:
            del self.productos[producto_id]
            return True
        return False

    def listar_productos(self) -> list:
        return list(self.productos.values())

    # --- pedidos ---

    def realizar_pedido(self, usuario_id: str, productos_solicitados: list):
        # productos_solicitados es una lista de tuplas (producto_id, cantidad)
        usuario = self.usuarios.get(usuario_id)
        if usuario is None:
            print("El usuario no existe")
            return None
        if not isinstance(usuario, Cliente):
            print("Solo los clientes pueden hacer pedidos")
            return None

        # comprobamos primero que todos los productos existen y hay stock
        lineas = []
        for producto_id, cantidad in productos_solicitados:
            producto = self.productos.get(producto_id)
            if producto is None:
                print("Un producto del pedido no existe")
                return None
            if not producto.hay_stock(cantidad):
                print(f"No hay stock suficiente de {producto.nombre}")
                return None
            lineas.append((producto, cantidad))

        # todo validado, ahora descontamos el stock
        for producto, cantidad in lineas:
            producto.actualizar_stock(-cantidad)

        pedido = Pedido(usuario, lineas)
        self.pedidos.append(pedido)
        return pedido

    def listar_pedidos_usuario(self, usuario_id: str) -> list:
        pedidos_usuario = [p for p in self.pedidos if p.cliente.id == usuario_id]
        return sorted(pedidos_usuario, key=lambda p: p.fecha)
