from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.cliente import router as cliente_router
from src.api.inventario import router as inventario_router
from src.api.producto import router as producto_router
from src.api.vendedor import router as vendedor_router
from src.database.database import Base, engine
from src.entities import cliente as _cliente_model  # noqa: F401
from src.entities import inventario as _inventario_model  # noqa: F401
from src.entities import producto as _producto_model  # noqa: F401
from src.entities import vendedor as _vendedor_model  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="API de la Clase", lifespan=lifespan)
app.include_router(vendedor_router)
app.include_router(cliente_router)
app.include_router(inventario_router)
app.include_router(producto_router)


@app.get("/")
def inicio():
    return {"mensaje": "API de la Clase activa"}
