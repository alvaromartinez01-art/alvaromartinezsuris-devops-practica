# alvaromartinez01-art-devops-practica

Proyecto: Tienda online (API REST con FastAPI)

Autor: Álvaro Martínez Suris

Descripcion: aplicacion Python que gestiona una tienda online. Permite registrar usuarios (clientes y administradores), gestionar un catalogo de productos (genericos, electronicos y ropa) y realizar pedidos con control de stock. Se expone mediante una API REST desarrollada con FastAPI y los datos se guardan en memoria.

## Estructura

- `src/`             API FastAPI (`main.py`, `schemas.py`, `models/`, `services/` con `TiendaService`)
- `cliente_python/`  cliente de prueba (`cliente.py`)
- `frontend/`        interfaz web (`index.html`)
- `Dockerfile`       definicion de la imagen
- `.dockerignore`    ficheros excluidos del contexto de construccion
- `requirements.txt` dependencias con versiones fijadas

## Ejecucion sin Docker

    pip install -r requirements.txt
    cd src
    python main.py

Documentacion: http://localhost:8000/docs

## Docker

### Construir la imagen

    docker build -t alvaromartinezsuris/tienda-online:1.0 .
    docker tag alvaromartinezsuris/tienda-online:1.0 alvaromartinezsuris/tienda-online:latest

### Ejecutar el contenedor

    docker run --rm -p 8000:8000 alvaromartinezsuris/tienda-online:1.0

En segundo plano:

    docker run -d --name tienda -p 8000:8000 alvaromartinezsuris/tienda-online:1.0
    docker logs tienda
    docker stop tienda && docker rm tienda

Con otro puerto publicado en el equipo (el 9000 del equipo apunta al 8000 del contenedor):

    docker run --rm -p 9000:8000 alvaromartinezsuris/tienda-online:1.0

Con otro puerto dentro del contenedor:

    docker run --rm -e PORT=9000 -p 9000:9000 alvaromartinezsuris/tienda-online:1.0

### Variables de entorno

| Variable | Valor por defecto en la imagen | Descripcion |
|----------|--------------------------------|-------------|
| `HOST`   | `0.0.0.0`                      | Direccion en la que escucha la API |
| `PORT`   | `8000`                         | Puerto en el que escucha la API |

### Salida esperada y pasos de prueba

Al arrancar el contenedor se debe imprimir algo similar a:

    INFO:     Started server process [1]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

Pruebas:

1. Abrir http://localhost:8000/docs y comprobar que se muestra la documentacion Swagger.
2. Listar productos (devuelve `[]` al inicio):

        curl http://localhost:8000/productos

3. Crear un producto (devuelve 201 con el producto creado):

        curl -X POST http://localhost:8000/productos -H "Content-Type: application/json" -d '{"tipo":"ropa","nombre":"Camiseta","precio":14.99,"stock":50,"talla":"M","color":"Blanco"}'

4. Ejecutar el cliente de prueba contra el contenedor (con el contenedor en marcha):

        pip install requests
        python cliente_python/cliente.py http://localhost:8000

   Debe mostrar `OK` en cada peticion y terminar tras comprobar el error 409 por stock insuficiente.

Nota: los datos se guardan en memoria y se pierden al detener el contenedor.

### Publicar y descargar la imagen

    docker login
    docker push alvaromartinezsuris/tienda-online:1.0
    docker push alvaromartinezsuris/tienda-online:latest

Para descargarla y ejecutarla en cualquier equipo:

    docker pull alvaromartinezsuris/tienda-online:1.0
    docker run --rm -p 8000:8000 alvaromartinezsuris/tienda-online:1.0

## Flujo de trabajo Git

- `main`: rama principal, protegida (cambios solo mediante Pull Request).
- `feature/docker`: contenerizacion de la aplicacion.
