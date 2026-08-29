from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.crud import inventario as inventario_crud
from src.database.database import get_db
from src.entities.inventario import Inventario

router = APIRouter(prefix="/inventarios", tags=["Inventario"])


class InventarioBase(BaseModel):
    sku: str
    nombre_producto: str
    descripcion: str | None = None
    categoria: str | None = None
    precio: float
    cantidad: int = 0
    stock_minimo: int = 0
    activo: bool = True


class InventarioCrear(InventarioBase):
    pass


class InventarioActualizar(BaseModel):
    sku: str | None = None
    nombre_producto: str | None = None
    descripcion: str | None = None
    categoria: str | None = None
    precio: float | None = None
    cantidad: int | None = None
    stock_minimo: int | None = None
    activo: bool | None = None


class InventarioRespuesta(InventarioBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


@router.get("", response_model=list[InventarioRespuesta])
def listar_inventarios(db: Session = Depends(get_db)):
    return inventario_crud.listar(db)


@router.get("/{inventario_id}", response_model=InventarioRespuesta)
def obtener_inventario(inventario_id: UUID, db: Session = Depends(get_db)):
    inventario = inventario_crud.obtener(db, inventario_id)
    if inventario is None:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return inventario


@router.post(
    "", response_model=InventarioRespuesta, status_code=status.HTTP_201_CREATED
)
def crear_inventario(datos: InventarioCrear, db: Session = Depends(get_db)):
    try:
        return inventario_crud.crear(db, datos.model_dump())
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El sku ya esta registrado")


@router.put("/{inventario_id}", response_model=InventarioRespuesta)
def actualizar_inventario(
    inventario_id: UUID,
    datos: InventarioActualizar,
    db: Session = Depends(get_db),
):
    inventario = inventario_crud.obtener(db, inventario_id)
    if inventario is None:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    try:
        return inventario_crud.actualizar(
            db, inventario, datos.model_dump(exclude_unset=True)
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El sku ya esta registrado")


@router.delete("/{inventario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_inventario(inventario_id: UUID, db: Session = Depends(get_db)):
    inventario = inventario_crud.obtener(db, inventario_id)
    if inventario is None:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    inventario_crud.eliminar(db, inventario)
