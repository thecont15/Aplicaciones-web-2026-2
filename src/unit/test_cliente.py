from http import HTTPStatus

CLIENTE_VALIDO = {
    "nombre": "Carlos",
    "apellido": "Gomez",
    "email": "carlos.gomez@correo.com",
    "telefono": "3123456789",
    "activo": True,
}


def crear_cliente(client, **cambios):
    datos = {**CLIENTE_VALIDO, **cambios}
    respuesta = client.post("/clientes", json=datos)
    assert respuesta.status_code == HTTPStatus.CREATED
    return respuesta.json()


# ---------------------------------------------------------------------------
# 1. GET /clientes (Obtener lista)
# ---------------------------------------------------------------------------


def test_listar_clientes_correctamente(client):
    creado = crear_cliente(client)

    respuesta = client.get("/clientes")

    assert respuesta.status_code == HTTPStatus.OK
    cuerpo = respuesta.json()
    assert len(cuerpo) == 1
    assert cuerpo[0]["id"] == creado["id"]
    assert cuerpo[0]["email"] == CLIENTE_VALIDO["email"]


def test_listar_clientes_error_metodo_no_permitido(client):
    respuesta = client.patch("/clientes", json=CLIENTE_VALIDO)

    assert respuesta.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    assert respuesta.json() == {"detail": "Method Not Allowed"}


# ---------------------------------------------------------------------------
# 2. GET /clientes/{id} (Obtener registro por ID)
# ---------------------------------------------------------------------------


def test_obtener_cliente_correctamente(client):
    creado = crear_cliente(client)

    respuesta = client.get(f"/clientes/{creado['id']}")

    assert respuesta.status_code == HTTPStatus.OK
    assert respuesta.json() == creado


def test_obtener_cliente_error_id_inexistente(client):
    respuesta = client.get("/clientes/999999")

    assert respuesta.status_code == HTTPStatus.NOT_FOUND
    assert respuesta.json() == {"detail": "Cliente no encontrado"}


# ---------------------------------------------------------------------------
# 3. POST /clientes (Crear)
# ---------------------------------------------------------------------------


def test_crear_cliente_correctamente(client):
    respuesta = client.post("/clientes", json=CLIENTE_VALIDO)

    assert respuesta.status_code == HTTPStatus.CREATED
    cuerpo = respuesta.json()
    assert isinstance(cuerpo["id"], int)
    assert cuerpo["nombre"] == CLIENTE_VALIDO["nombre"]
    assert cuerpo["apellido"] == CLIENTE_VALIDO["apellido"]
    assert cuerpo["email"] == CLIENTE_VALIDO["email"]
    assert cuerpo["telefono"] == CLIENTE_VALIDO["telefono"]
    assert cuerpo["activo"] is True


def test_crear_cliente_error_campos_obligatorios_faltantes(client):
    # Faltan "nombre", "apellido" y "email" que son requeridos
    respuesta = client.post("/clientes", json={"telefono": "3100000000"})

    assert respuesta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    campos_con_error = {error["loc"][-1] for error in respuesta.json()["detail"]}
    assert campos_con_error == {"nombre", "apellido", "email"}


# ---------------------------------------------------------------------------
# 4. PUT /clientes/{id} (Actualizar)
# ---------------------------------------------------------------------------


def test_actualizar_cliente_correctamente(client):
    creado = crear_cliente(client)

    respuesta = client.put(
        f"/clientes/{creado['id']}",
        json={"telefono": "3009998877", "activo": False},
    )

    assert respuesta.status_code == HTTPStatus.OK
    cuerpo = respuesta.json()
    assert cuerpo["id"] == creado["id"]
    assert cuerpo["telefono"] == "3009998877"
    assert cuerpo["activo"] is False
    assert cuerpo["nombre"] == creado["nombre"]


def test_actualizar_cliente_error_id_inexistente(client):
    respuesta = client.put("/clientes/999999", json={"telefono": "3001112233"})

    assert respuesta.status_code == HTTPStatus.NOT_FOUND
    assert respuesta.json() == {"detail": "Cliente no encontrado"}


# ---------------------------------------------------------------------------
# 5. DELETE /clientes/{id} (Eliminar)
# ---------------------------------------------------------------------------


def test_eliminar_cliente_correctamente(client):
    creado = crear_cliente(client)

    respuesta = client.delete(f"/clientes/{creado['id']}")

    assert respuesta.status_code == HTTPStatus.NO_CONTENT
    assert respuesta.content == b""
    assert client.get(f"/clientes/{creado['id']}").status_code == HTTPStatus.NOT_FOUND


def test_eliminar_cliente_error_id_inexistente(client):
    existente = crear_cliente(client)

    respuesta = client.delete("/clientes/999999")

    assert respuesta.status_code == HTTPStatus.NOT_FOUND
    assert respuesta.json() == {"detail": "Cliente no encontrado"}
    assert client.get(f"/clientes/{existente['id']}").status_code == HTTPStatus.OK
