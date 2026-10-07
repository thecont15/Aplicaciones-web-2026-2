import os

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ.setdefault("DATABASE_URL", "sqlite://")

from src.database.database import Base, get_db
from src.routers.cliente import router as cliente_router
from src.routers.inventario import router as inventario_router
from src.routers.producto import router as producto_router
from src.routers.vendedor import router as vendedor_router


@pytest.fixture
def db_engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    try:
        yield engine
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def db_session(db_engine):
    testing_session = sessionmaker(bind=db_engine, autoflush=False, autocommit=False)
    with testing_session() as db:
        yield db


@pytest.fixture
def client(db_engine):
    testing_session = sessionmaker(bind=db_engine, autoflush=False, autocommit=False)
    app = FastAPI()
    app.include_router(vendedor_router)
    app.include_router(inventario_router)
    app.include_router(cliente_router)
    app.include_router(producto_router)

    def override_get_db():
        with testing_session() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
