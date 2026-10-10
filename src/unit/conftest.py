import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")

import pytest
from fastapi.testclient import TestClient

from src.database import database as database_module
from src.main import app


@pytest.fixture(scope="function", autouse=True)
def reset_db():
    database_module.Base.metadata.drop_all(bind=database_module.engine)
    database_module.Base.metadata.create_all(bind=database_module.engine)
    yield
    database_module.Base.metadata.drop_all(bind=database_module.engine)


@pytest.fixture()
def cliente():
    with TestClient(app) as client:
        yield client
