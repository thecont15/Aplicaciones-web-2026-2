from http import HTTPStatus

PRODUCTO_VALIDO = {
    "nombre": "Mouse inalambrico",
    "descripcion": "Mouse optico 2.4GHz",
    "precio": 45.5,
    "stock": 10,
    "activo": True,
}


def crear_producto(client, **cambios):
    respuesta = client.post("/productos", json={**PRODUCTO_VALIDO, **cambios})
    assert respuesta.status_code == HTTPStatus.CREATED
    return respuesta.json()


# GET /productos


def test_listar_productos_correctamente(client):
    creado = crear_producto(client)

    respuesta = client.get("/productos")

    assert respuesta.status_code == HTTPStatus.OK
    assert len(respuesta.json()) == 1
    assert respuesta.json()[0]["id"] == creado["id"]
    assert respuesta.json()[0]["nombre"] == PRODUCTO_VALIDO["nombre"]


def test_listar_productos_error_metodo_no_permitido(client):
    respuesta = client.patch("/productos", json=PRODUCTO_VALIDO)

    assert respuesta.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    assert respuesta.json() == {"detail": "Method Not Allowed"}


# GET /productos/{id}


def test_obtener_producto_correctamente(client):
    creado = crear_producto(client)

    respuesta = client.get(f"/productos/{creado['id']}")

    assert respuesta.status_code == HTTPStatus.OK
    assert respuesta.json() == creado


def test_obtener_producto_error_id_inexistente(client):
    respuesta = client.get("/productos/999999")

    assert respuesta.status_code == HTTPStatus.NOT_FOUND
    assert respuesta.json() == {"detail": "Producto no encontrado"}


# POST /productos


def test_crear_producto_correctamente(client):
    respuesta = client.post("/productos", json=PRODUCTO_VALIDO)

    assert respuesta.status_code == HTTPStatus.CREATED
    cuerpo = respuesta.json()
    assert isinstance(cuerpo["id"], int)
    assert cuerpo["nombre"] == PRODUCTO_VALIDO["nombre"]
    assert cuerpo["precio"] == PRODUCTO_VALIDO["precio"]
    assert cuerpo["stock"] == PRODUCTO_VALIDO["stock"]
    assert cuerpo["activo"] is True


def test_crear_producto_error_datos_invalidos(client):
    # Falta "nombre" (obligatorio), "precio" es negativo y "stock" no es entero.
    respuesta = client.post(
        "/productos", json={"precio": -5, "stock": "muchos"}
    )

    assert respuesta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    campos_con_error = {error["loc"][-1] for error in respuesta.json()["detail"]}
    assert campos_con_error == {"nombre", "precio", "stock"}
    assert client.get("/productos").json() == []


# PUT /productos/{id}


def test_actualizar_producto_correctamente(client):
    creado = crear_producto(client)

    respuesta = client.put(
        f"/productos/{creado['id']}", json={"precio": 60.0, "stock": 25}
    )

    assert respuesta.status_code == HTTPStatus.OK
    cuerpo = respuesta.json()
    assert cuerpo["id"] == creado["id"]
    assert cuerpo["precio"] == 60.0
    assert cuerpo["stock"] == 25
    assert cuerpo["nombre"] == creado["nombre"]


def test_actualizar_producto_error_id_inexistente(client):
    respuesta = client.put("/productos/999999", json={"stock": 5})

    assert respuesta.status_code == HTTPStatus.NOT_FOUND
    assert respuesta.json() == {"detail": "Producto no encontrado"}


# DELETE /productos/{id}


def test_eliminar_producto_correctamente(client):
    creado = crear_producto(client)

    respuesta = client.delete(f"/productos/{creado['id']}")

    assert respuesta.status_code == HTTPStatus.NO_CONTENT
    assert respuesta.content == b""
    assert client.get(f"/productos/{creado['id']}").status_code == HTTPStatus.NOT_FOUND


def test_eliminar_producto_error_id_inexistente(client):
    existente = crear_producto(client)

    respuesta = client.delete("/productos/999999")

    assert respuesta.status_code == HTTPStatus.NOT_FOUND
    assert respuesta.json() == {"detail": "Producto no encontrado"}
    assert client.get(f"/productos/{existente['id']}").status_code == HTTPStatus.OK
