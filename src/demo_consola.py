from services.tienda_service import TiendaService


def main():
    tienda = TiendaService()

    # registro 3 clientes y 1 administrador
    cliente1 = tienda.registrar_usuario("cliente", "Ana Garcia", "ana.garcia@gmail.com", "Calle Mayor 1, Madrid")
    cliente2 = tienda.registrar_usuario("cliente", "Luis Perez", "luis.perez@gmail.com", "Avenida del Puerto 2, Valencia")
    cliente3 = tienda.registrar_usuario("cliente", "Marta Ruiz", "marta.ruiz@gmail.com", "Calle Gran Via 3, Vigo")
    admin = tienda.registrar_usuario("administrador", "Alvaro Admin", "alvaro.admin@gmail.com")

    print("Usuarios registrados")
    for usuario in (cliente1, cliente2, cliente3, admin):
        print(usuario, "| Admin:", usuario.is_admin())
    print()

    # creo 5 productos distintos
    portatil = tienda.anadir_producto("electronico", "Portatil", 899.99, 10, meses_garantia=24)
    movil = tienda.anadir_producto("electronico", "iPhone", 549.00, 15, meses_garantia=12)
    camiseta = tienda.anadir_producto("ropa", "Camiseta", 14.99, 50, talla="M", color="Blanco")
    pantalon = tienda.anadir_producto("ropa", "Pantalon", 39.99, 30, talla="L", color="Azul")
    sudadera = tienda.anadir_producto("ropa", "Sudadera", 29.99, 20, talla="S", color="Negro")

    print("Inventario inicial")
    for producto in tienda.listar_productos():
        print(producto)
    print()

    # simulo 3 pedidos de distintos clientes
    pedido1 = tienda.realizar_pedido(cliente1.id, [(portatil.id, 1), (camiseta.id, 2)])
    pedido2 = tienda.realizar_pedido(cliente2.id, [(movil.id, 1), (pantalon.id, 1)])
    pedido3 = tienda.realizar_pedido(cliente3.id, [(sudadera.id, 3), (camiseta.id, 1)])

    print("Pedidos realizados")
    for pedido in (pedido1, pedido2, pedido3):
        print(pedido)
    print()

    print(f"Historico de pedidos de {cliente1.nombre}")
    for pedido in tienda.listar_pedidos_usuario(cliente1.id):
        print(pedido)
    print()

    print("Stock actualizado tras los pedidos")
    for producto in tienda.listar_productos():
        print(producto)


if __name__ == "__main__":
    main()
