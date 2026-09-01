from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.vendedor import router as vendedor_router
from src.database.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="API de Vendedores", lifespan=lifespan)
app.include_router(vendedor_router)


@app.get("/")
def inicio():
    return {"mensaje": "API de vendedores activa"}
