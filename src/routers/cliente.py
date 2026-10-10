from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.crud import cliente as repo
from src.database.database import get_db

router = APIRouter(prefix="/clientes", tags=["clientes"])


class ClienteBase(BaseModel):
    nombre: str
    apellido: str
    email: str
    telefono: str | None = None
    activo: bool = True


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    email: str | None = None
    telefono: str | None = None
    activo: bool | None = None


class ClienteRead(ClienteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


@router.get("", response_model=list[ClienteRead])
def listar_clientes(db: Session = Depends(get_db)):
    return repo.listar(db)


@router.get("/{cliente_id}", response_model=ClienteRead)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = repo.obtener(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.post("", response_model=ClienteRead, status_code=status.HTTP_201_CREATED)
def crear_cliente(datos: ClienteCreate, db: Session = Depends(get_db)):
    try:
        return repo.crear(db, datos.model_dump())
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El email ya esta registrado")


@router.put("/{cliente_id}", response_model=ClienteRead)
def actualizar_cliente(
    cliente_id: int,
    datos: ClienteUpdate,
    db: Session = Depends(get_db),
):
    cliente = repo.obtener(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    try:
        return repo.actualizar(db, cliente, datos.model_dump(exclude_unset=True))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El email ya esta registrado")


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = repo.obtener(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    repo.eliminar(db, cliente)
