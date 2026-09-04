from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.database import engine
from src.entities.inventario import Inventario
from src.entities.vendedor import Vendedor
from src.routers.inventario import router as inventario_router
from src.routers.vendedor import router as vendedor_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Vendedor.metadata.create_all(bind=engine)
    Inventario.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="API de Vendedores", lifespan=lifespan)
app.include_router(vendedor_router)
app.include_router(inventario_router)


@app.get("/")
def inicio():
    return {"mensaje": "API de vendedores activa"}
