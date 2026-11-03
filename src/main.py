import os

import uvicorn
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware

from models.producto import ProductoElectronico, ProductoRopa
from models.usuario import Cliente
from schemas import (PedidoCreate, PedidoRead, ProductoCreate, ProductoRead,
                     UsuarioCreate, UsuarioRead)
from services.tienda_service import TiendaService

app = FastAPI(title="Tienda online", version="1.0")


app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

tienda = TiendaService()


def a_usuario_read(u) -> UsuarioRead:
    return UsuarioRead(id=u.id, nombre=u.nombre, email=u.email, es_admin=u.is_admin())


def a_producto_read(p) -> ProductoRead:
    datos = dict(id=p.id, nombre=p.nombre, precio=p.precio, stock=p.stock, tipo="generico")
    if isinstance(p, ProductoElectronico):
        datos.update(tipo="electronico", meses_garantia=p.meses_garantia)
    elif isinstance(p, ProductoRopa):
        datos.update(tipo="ropa", talla=p.talla, color=p.color)
    return ProductoRead(**datos)


def a_pedido_read(ped) -> PedidoRead:
    items = [dict(producto_id=p.id, nombre=p.nombre, precio_unitario=p.precio,
                  cantidad=c, subtotal=round(p.precio * c, 2)) for p, c in ped.lineas]
    return PedidoRead(id=ped.id, fecha=ped.fecha, cliente=a_usuario_read(ped.cliente),
                      total=round(ped.calcular_total(), 2), items=items)


@app.post("/usuarios", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(datos: UsuarioCreate):
    usuario = tienda.registrar_usuario(datos.tipo, datos.nombre, datos.email, datos.direccion or "")
    if usuario is None:
        raise HTTPException(400, "No se pudo crear el usuario")
    return a_usuario_read(usuario)


@app.get("/usuarios", response_model=list[UsuarioRead])
def listar_usuarios():
    return [a_usuario_read(u) for u in tienda.listar_usuarios()]


@app.get("/usuarios/{usuario_id}", response_model=UsuarioRead)
def obtener_usuario(usuario_id: str):
    usuario = tienda.obtener_usuario(usuario_id)
    if usuario is None:
        raise HTTPException(404, "Usuario no encontrado")
    return a_usuario_read(usuario)


@app.post("/productos", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def crear_producto(datos: ProductoCreate):
    producto = tienda.anadir_producto(
        datos.tipo, datos.nombre, datos.precio, datos.stock,
        meses_garantia=datos.meses_garantia or 0,
        talla=datos.talla or "", color=datos.color or "")
    if producto is None:
        raise HTTPException(400, "No se pudo crear el producto")
    return a_producto_read(producto)


@app.get("/productos", response_model=list[ProductoRead])
def listar_productos():
    return [a_producto_read(p) for p in tienda.listar_productos()]


@app.get("/productos/{producto_id}", response_model=ProductoRead)
def obtener_producto(producto_id: str):
    producto = tienda.obtener_producto(producto_id)
    if producto is None:
        raise HTTPException(404, "Producto no encontrado")
    return a_producto_read(producto)


@app.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(producto_id: str):
    if not tienda.eliminar_producto(producto_id):
        raise HTTPException(404, "Producto no encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/pedidos", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
def crear_pedido(datos: PedidoCreate):
    cliente = tienda.obtener_usuario(datos.cliente_id)
    if cliente is None:
        raise HTTPException(404, "Cliente no encontrado")
    if not isinstance(cliente, Cliente):
        raise HTTPException(400, "Solo los clientes pueden hacer pedidos")


    cantidades = {}
    for item in datos.items:
        cantidades[item.producto_id] = cantidades.get(item.producto_id, 0) + item.cantidad

    for producto_id, cantidad in cantidades.items():
        producto = tienda.obtener_producto(producto_id)
        if producto is None:
            raise HTTPException(404, f"Producto no encontrado: {producto_id}")
        if not producto.hay_stock(cantidad):
            raise HTTPException(409, f"Stock insuficiente de '{producto.nombre}' "
                                     f"(disponible: {producto.stock})")

    pedido = tienda.realizar_pedido(datos.cliente_id, list(cantidades.items()))
    if pedido is None:
        raise HTTPException(400, "No se pudo crear el pedido")
    return a_pedido_read(pedido)


@app.get("/usuarios/{cliente_id}/pedidos", response_model=list[PedidoRead])
def pedidos_de_cliente(cliente_id: str):
    if tienda.obtener_usuario(cliente_id) is None:
        raise HTTPException(404, "Usuario no encontrado")
    return [a_pedido_read(p) for p in tienda.listar_pedidos_usuario(cliente_id)]


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", "8000")))
