from http import HTTPStatus

VENDEDOR_VALIDO = {
    "nombre": "Ana Perez",
    "apellido": "Gomez",
    "email": "ana.gomez@correo.com",
    "telefono": "3001234567",
    "activo": True,
}

VENDEDOR_ACTUALIZADO = {
    "nombre": "Ana Gomez",
    "apellido": "Pérez",
    "email": "ana.perez@correo.com",
    "telefono": "3007654321",
    "activo": False,
}


def _crear_vendedor(cliente, datos=None):
    respuesta = cliente.post("/vendedores", json=datos or VENDEDOR_VALIDO)
    assert respuesta.status_code == HTTPStatus.CREATED.value
    return respuesta.json()


def test_listar_vendedores_devuelve_200_y_una_lista(cliente):
    _crear_vendedor(cliente)
    respuesta = cliente.get("/vendedores")

    assert respuesta.status_code == HTTPStatus.OK.value
    cuerpo = respuesta.json()
    assert isinstance(cuerpo, list)
    assert len(cuerpo) == 1
    assert cuerpo[0]["nombre"] == VENDEDOR_VALIDO["nombre"]


def test_listar_vendedores_vacio_devuelve_200_y_lista_vacia(cliente):
    respuesta = cliente.get("/vendedores")

    assert respuesta.status_code == HTTPStatus.OK.value
    assert respuesta.json() == []


def test_obtener_vendedor_devuelve_200(cliente):
    creado = _crear_vendedor(cliente)
    respuesta = cliente.get(f"/vendedores/{creado['id']}")

    assert respuesta.status_code == HTTPStatus.OK.value
    cuerpo = respuesta.json()
    assert cuerpo["id"] == creado["id"]
    assert cuerpo["nombre"] == VENDEDOR_VALIDO["nombre"]
    assert cuerpo["apellido"] == VENDEDOR_VALIDO["apellido"]
    assert cuerpo["email"] == VENDEDOR_VALIDO["email"]


def test_obtener_vendedor_inexistente_devuelve_404(cliente):
    respuesta = cliente.get("/vendedores/999999")

    assert respuesta.status_code == HTTPStatus.NOT_FOUND.value
    assert respuesta.json()["detail"] == "Vendedor no encontrado"


def test_crear_vendedor_devuelve_201(cliente):
    respuesta = cliente.post("/vendedores", json=VENDEDOR_VALIDO)

    assert respuesta.status_code == HTTPStatus.CREATED.value
    cuerpo = respuesta.json()
    assert "id" in cuerpo
    assert cuerpo["nombre"] == VENDEDOR_VALIDO["nombre"]
    assert cuerpo["apellido"] == VENDEDOR_VALIDO["apellido"]
    assert cuerpo["email"] == VENDEDOR_VALIDO["email"]


def test_crear_vendedor_con_email_repetido_devuelve_409(cliente):
    cliente.post("/vendedores", json=VENDEDOR_VALIDO)
    respuesta = cliente.post("/vendedores", json=VENDEDOR_VALIDO)

    assert respuesta.status_code == HTTPStatus.CONFLICT.value
    assert respuesta.json()["detail"] == "El email ya esta registrado"


def test_actualizar_vendedor_devuelve_200(cliente):
    creado = _crear_vendedor(cliente)
    respuesta = cliente.put(
        f"/vendedores/{creado['id']}",
        json=VENDEDOR_ACTUALIZADO,
    )

    assert respuesta.status_code == HTTPStatus.OK.value
    cuerpo = respuesta.json()
    assert cuerpo["id"] == creado["id"]
    assert cuerpo["nombre"] == VENDEDOR_ACTUALIZADO["nombre"]
    assert cuerpo["apellido"] == VENDEDOR_ACTUALIZADO["apellido"]
    assert cuerpo["email"] == VENDEDOR_ACTUALIZADO["email"]
    assert cuerpo["activo"] is False


def test_actualizar_vendedor_inexistente_devuelve_404(cliente):
    respuesta = cliente.put("/vendedores/999999", json=VENDEDOR_ACTUALIZADO)

    assert respuesta.status_code == HTTPStatus.NOT_FOUND.value
    assert respuesta.json()["detail"] == "Vendedor no encontrado"


def test_borrar_vendedor_creado_devuelve_204(cliente):
    creado = _crear_vendedor(cliente)

    respuesta = cliente.delete(f"/vendedores/{creado['id']}")

    assert respuesta.status_code == HTTPStatus.NO_CONTENT.value
    consulta = cliente.get(f"/vendedores/{creado['id']}")
    assert consulta.status_code == HTTPStatus.NOT_FOUND.value


def test_borrar_vendedor_inexistente_devuelve_404(cliente):
    respuesta = cliente.delete("/vendedores/999999")

    assert respuesta.status_code == HTTPStatus.NOT_FOUND.value
    assert respuesta.json()["detail"] == "Vendedor no encontrado"
