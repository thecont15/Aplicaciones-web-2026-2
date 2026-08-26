from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.producto import router as producto_router
from src.api.vendedor import router as vendedor_router
from src.database.database import Base, engine
from src.entities import producto as _producto_model
from src.entities import vendedor as _vendedor_model


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="API de Vendedores y Productos", lifespan=lifespan)
app.include_router(vendedor_router)
app.include_router(producto_router)


@app.get("/")
def inicio():
    return {"mensaje": "API de vendedores y productos activa"}
