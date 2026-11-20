from http import HTTPStatus

ORIGEN_FRONTEND = "http://localhost:4200"


def test_cors_permite_origen_del_frontend(client):
    respuesta = client.get("/productos", headers={"Origin": ORIGEN_FRONTEND})

    assert respuesta.status_code == HTTPStatus.OK
    assert respuesta.headers["access-control-allow-origin"] == ORIGEN_FRONTEND


def test_cors_preflight_permite_put_y_delete(client):
    respuesta = client.options(
        "/productos/1",
        headers={
            "Origin": ORIGEN_FRONTEND,
            "Access-Control-Request-Method": "PUT",
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert respuesta.status_code == HTTPStatus.OK
    assert respuesta.headers["access-control-allow-origin"] == ORIGEN_FRONTEND
    assert "PUT" in respuesta.headers["access-control-allow-methods"]


def test_cors_no_permite_otros_origenes(client):
    origen = "http://otro-sitio.com"
    respuesta = client.get("/productos", headers={"Origin": origen})

    assert "access-control-allow-origin" not in respuesta.headers
