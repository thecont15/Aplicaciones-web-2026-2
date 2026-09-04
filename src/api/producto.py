from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from src.crud import producto as producto_crud
from src.database.database import get_db

router = APIRouter(prefix="/productos", tags=["Productos"])


class ProductoBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=255)
    precio: float = Field(gt=0)
    stock: int = Field(default=0, ge=0)
    activo: bool = True


class ProductoCrear(ProductoBase):
    pass


class ProductoActualizar(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=255)
    precio: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    activo: bool | None = None


class ProductoRespuesta(ProductoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


@router.get("", response_model=list[ProductoRespuesta])
def listar_productos(db: Session = Depends(get_db)):
    return producto_crud.listar(db)


@router.get("/{producto_id}", response_model=ProductoRespuesta)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = producto_crud.obtener(db, producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.post("", response_model=ProductoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_producto(datos: ProductoCrear, db: Session = Depends(get_db)):
    return producto_crud.crear(db, datos.model_dump())


@router.put("/{producto_id}", response_model=ProductoRespuesta)
def actualizar_producto(
    producto_id: int,
    datos: ProductoActualizar,
    db: Session = Depends(get_db),
):
    producto = producto_crud.obtener(db, producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto_crud.actualizar(
        db, producto, datos.model_dump(exclude_unset=True)
    )


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = producto_crud.obtener(db, producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto_crud.eliminar(db, producto)
