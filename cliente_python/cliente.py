import os
import sys

import requests


BASE_URL = "http://localhost:8000"
BASE_URL = os.getenv("TIENDA_API_URL", BASE_URL)
if len(sys.argv) > 1:
    BASE_URL = sys.argv[1]
BASE_URL = BASE_URL.rstrip("/")


def peticion(metodo: str, ruta: str, esperado: int, **kwargs):
    url = f"{BASE_URL}{ruta}"
    try:
        resp = requests.request(metodo, url, timeout=5, **kwargs)
    except requests.exceptions.RequestException as e:
        sys.exit(f"No se pudo conectar con {url}: {e}")

    ok = resp.status_code == esperado
    print(f"{'OK ' if ok else 'ERR'} {metodo} {ruta} -> {resp.status_code}")
    if not ok:
        sys.exit(f"Se esperaba {esperado}. Respuesta: {resp.text}")
    return resp.json() if resp.content else None


def main():
    print(f"API: {BASE_URL}\n")

    print("1. Crear usuario")
    cliente = peticion("POST", "/usuarios", 201, json={
        "tipo": "cliente", "nombre": "Ana Garcia",
        "email": "ana.garcia@gmail.com", "direccion": "Calle Mayor 1, Madrid"})
    print("  ", cliente)

    print("\n2. Lista de usuarios")
    for u in peticion("GET", "/usuarios", 200):
        print(f"   {u['id']} | {u['nombre']} | admin={u['es_admin']}")

    print("\n3. Crear productos")
    portatil = peticion("POST", "/productos", 201, json={
        "tipo": "electronico", "nombre": "Portatil", "precio": 899.99,
        "stock": 10, "meses_garantia": 24})
    camiseta = peticion("POST", "/productos", 201, json={
        "tipo": "ropa", "nombre": "Camiseta", "precio": 14.99,
        "stock": 50, "talla": "M", "color": "Blanco"})

    print("\n4. Lista de productos")
    for p in peticion("GET", "/productos", 200):
        print(f"   {p['id']} | {p['tipo']} | {p['nombre']} | {p['precio']}EUR | stock {p['stock']}")

    print("\n5. Crear pedido")
    pedido = peticion("POST", "/pedidos", 201, json={
        "cliente_id": cliente["id"],
        "items": [{"producto_id": portatil["id"], "cantidad": 1},
                  {"producto_id": camiseta["id"], "cantidad": 2}]})
    print(f"   Pedido {pedido['id']} | total {pedido['total']}EUR")

    print("\n6. Pedidos del usuario")
    for ped in peticion("GET", f"/usuarios/{cliente['id']}/pedidos", 200):
        detalle = ", ".join(f"{i['cantidad']}x {i['nombre']}" for i in ped["items"])
        print(f"   {ped['fecha']} | {detalle} | total {ped['total']}EUR")

    print("\n7. Comprobar un error (stock insuficiente -> 409)")
    peticion("POST", "/pedidos", 409, json={
        "cliente_id": cliente["id"],
        "items": [{"producto_id": portatil["id"], "cantidad": 999}]})


if __name__ == "__main__":
    main()
