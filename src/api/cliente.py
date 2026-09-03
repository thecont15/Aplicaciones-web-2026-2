from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.crud import cliente as cliente_crud
from src.database.database import get_db
from src.entities.cliente import Cliente

router = APIRouter(prefix="/clientes", tags=["Clientes"])


class ClienteBase(BaseModel):
    nombre: str
    apellido: str
    email: str
    telefono: str | None = None
    activo: bool = True


class ClienteCrear(ClienteBase):
    pass


class ClienteActualizar(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    email: str | None = None
    telefono: str | None = None
    activo: bool | None = None


class ClienteRespuesta(ClienteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


@router.get("", response_model=list[ClienteRespuesta])
def listar_clientes(db: Session = Depends(get_db)):
    return cliente_crud.consultar_todos(db)


@router.get("/{cliente_id}", response_model=ClienteRespuesta)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = cliente_crud.buscar_por_id(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.post("", response_model=ClienteRespuesta, status_code=status.HTTP_201_CREATED)
def crear_cliente(datos: ClienteCrear, db: Session = Depends(get_db)):
    try:
        return cliente_crud.registrar(db, datos.model_dump())
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El email ya esta registrado")


@router.put("/{cliente_id}", response_model=ClienteRespuesta)
def actualizar_cliente(
    cliente_id: int,
    datos: ClienteActualizar,
    db: Session = Depends(get_db),
):
    cliente = cliente_crud.buscar_por_id(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    try:
        return cliente_crud.modificar(
            db, cliente, datos.model_dump(exclude_unset=True)
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El email ya esta registrado")


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = cliente_crud.buscar_por_id(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    cliente_crud.dar_de_baja(db, cliente)
