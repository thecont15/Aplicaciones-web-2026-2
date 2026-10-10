import os

import pytest
from fastapi.testclient import TestClient


def pytest_configure():
    os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")


@pytest.fixture()
def app():
    from src.main import app as application

    return application


@pytest.fixture(scope="function", autouse=True)
def reset_db(app):
    from src.database import database as database_module

    database_module.Base.metadata.drop_all(bind=database_module.engine)
    database_module.Base.metadata.create_all(bind=database_module.engine)
    yield
    database_module.Base.metadata.drop_all(bind=database_module.engine)


@pytest.fixture()
def client(app):
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def cliente(client):
    return client
