from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.crud import inventario as inventario_crud
from src.database.database import get_db
from src.schemas.inventario import (
    InventarioActualizar,
    InventarioCrear,
    InventarioRespuesta,
    RespuestaAPI,
)

router = APIRouter(prefix="/inventarios", tags=["Inventario"])


@router.get("", response_model=RespuestaAPI[list[InventarioRespuesta]])
def listar_inventarios(db: Session = Depends(get_db)):
    inventarios = inventario_crud.listar(db)
    return {
        "data": inventarios,
        "status": status.HTTP_200_OK,
        "message": "Inventarios obtenidos correctamente",
    }


@router.get("/{inventario_id}", response_model=RespuestaAPI[InventarioRespuesta])
def obtener_inventario(inventario_id: UUID, db: Session = Depends(get_db)):
    inventario = inventario_crud.obtener(db, inventario_id)
    if inventario is None:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return {
        "data": inventario,
        "status": status.HTTP_200_OK,
        "message": "Inventario obtenido correctamente",
    }


@router.post(
    "",
    response_model=RespuestaAPI[InventarioRespuesta],
    status_code=status.HTTP_201_CREATED,
)
def crear_inventario(datos: InventarioCrear, db: Session = Depends(get_db)):
    try:
        inventario = inventario_crud.crear(db, datos.model_dump())
        return {
            "data": inventario,
            "status": status.HTTP_201_CREATED,
            "message": "Inventario creado correctamente",
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El sku ya esta registrado")


@router.put("/{inventario_id}", response_model=RespuestaAPI[InventarioRespuesta])
def actualizar_inventario(
    inventario_id: UUID,
    datos: InventarioActualizar,
    db: Session = Depends(get_db),
):
    inventario = inventario_crud.obtener(db, inventario_id)
    if inventario is None:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    try:
        inventario_actualizado = inventario_crud.actualizar(
            db, inventario, datos.model_dump(exclude_unset=True)
        )
        return {
            "data": inventario_actualizado,
            "status": status.HTTP_200_OK,
            "message": "Inventario actualizado correctamente",
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El sku ya esta registrado")


@router.delete("/{inventario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_inventario(inventario_id: UUID, db: Session = Depends(get_db)):
    inventario = inventario_crud.obtener(db, inventario_id)
    if inventario is None:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    inventario_crud.eliminar(db, inventario)
