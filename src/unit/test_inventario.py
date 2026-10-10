from http import HTTPStatus
from uuid import uuid4


def crear_inventario(client):
    respuesta = client.post(
        "/inventarios",
        json={
            "sku": f"SKU-{uuid4().hex[:8]}",
            "nombre_producto": "Teclado",
            "descripcion": "Teclado mecanico",
            "categoria": "Perifericos",
            "precio": 89.99,
            "cantidad": 12,
            "stock_minimo": 2,
            "activo": True,
        },
    )
    assert respuesta.status_code == HTTPStatus.CREATED
    return respuesta.json()


def test_listar_inventarios_correctamente(client):
    creado = crear_inventario(client)

    respuesta = client.get("/inventarios")

    assert respuesta.status_code == HTTPStatus.OK
    assert len(respuesta.json()) == 1
    assert respuesta.json()[0]["id"] == creado["id"]


def test_listar_inventarios_control_sin_registros(client):
    respuesta = client.get("/inventarios")

    assert respuesta.status_code == HTTPStatus.OK
    assert respuesta.json() == []


def test_obtener_inventario_correctamente(client):
    creado = crear_inventario(client)

    respuesta = client.get(f"/inventarios/{creado['id']}")

    assert respuesta.status_code == HTTPStatus.OK
    assert respuesta.json()["sku"] == creado["sku"]


def test_obtener_inventario_control_inexistente(client):
    respuesta = client.get(f"/inventarios/{uuid4()}")

    assert respuesta.status_code == HTTPStatus.NOT_FOUND
    assert respuesta.json()["detail"] == "Inventario no encontrado"


def test_crear_inventario_correctamente(client):
    respuesta = client.post(
        "/inventarios",
        json={
            "sku": f"SKU-{uuid4().hex[:8]}",
            "nombre_producto": "Monitor",
            "precio": 249.50,
        },
    )

    assert respuesta.status_code == HTTPStatus.CREATED
    assert respuesta.json()["nombre_producto"] == "Monitor"
    assert respuesta.json()["cantidad"] == 0


def test_crear_inventario_control_datos_invalidos(client):
    respuesta = client.post(
        "/inventarios",
        json={"sku": "SKU-INCOMPLETO", "precio": 10.00},
    )

    assert respuesta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_actualizar_inventario_correctamente(client):
    creado = crear_inventario(client)

    respuesta = client.put(
        f"/inventarios/{creado['id']}",
        json={"cantidad": 20, "precio": 95.00},
    )

    assert respuesta.status_code == HTTPStatus.OK
    assert respuesta.json()["cantidad"] == 20
    assert respuesta.json()["precio"] == 95.0


def test_actualizar_inventario_control_inexistente(client):
    respuesta = client.put(f"/inventarios/{uuid4()}", json={"cantidad": 20})

    assert respuesta.status_code == HTTPStatus.NOT_FOUND
    assert respuesta.json()["detail"] == "Inventario no encontrado"


def test_eliminar_inventario_correctamente(client):
    creado = crear_inventario(client)

    respuesta = client.delete(f"/inventarios/{creado['id']}")

    assert respuesta.status_code == HTTPStatus.NO_CONTENT
    assert (
        client.get(f"/inventarios/{creado['id']}").status_code == HTTPStatus.NOT_FOUND
    )


def test_eliminar_inventario_control_inexistente(client):
    respuesta = client.delete(f"/inventarios/{uuid4()}")

    assert respuesta.status_code == HTTPStatus.NOT_FOUND
    assert respuesta.json()["detail"] == "Inventario no encontrado"
