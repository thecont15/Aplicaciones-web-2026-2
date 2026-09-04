from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.crud import vendedor as repo
from src.database.database import get_db

router = APIRouter(prefix="/vendedores", tags=["vendedores"])


class VendedorBase(BaseModel):
    nombre: str
    apellido: str
    email: str
    telefono: str | None = None
    activo: bool = True


class VendedorCreate(VendedorBase):
    pass


class VendedorUpdate(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    email: str | None = None
    telefono: str | None = None
    activo: bool | None = None


class VendedorRead(VendedorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


@router.get("", response_model=list[VendedorRead])
def listar_vendedores(db: Session = Depends(get_db)):
    return repo.listar(db)


@router.get("/{vendedor_id}", response_model=VendedorRead)
def obtener_vendedor(vendedor_id: int, db: Session = Depends(get_db)):
    vendedor = repo.obtener(db, vendedor_id)
    if vendedor is None:
        raise HTTPException(status_code=404, detail="Vendedor no encontrado")
    return vendedor


@router.post("", response_model=VendedorRead, status_code=status.HTTP_201_CREATED)
def crear_vendedor(datos: VendedorCreate, db: Session = Depends(get_db)):
    try:
        return repo.crear(db, datos.model_dump())
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El email ya esta registrado")


@router.put("/{vendedor_id}", response_model=VendedorRead)
def actualizar_vendedor(
    vendedor_id: int,
    datos: VendedorUpdate,
    db: Session = Depends(get_db),
):
    vendedor = repo.obtener(db, vendedor_id)
    if vendedor is None:
        raise HTTPException(status_code=404, detail="Vendedor no encontrado")
    try:
        return repo.actualizar(db, vendedor, datos.model_dump(exclude_unset=True))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El email ya esta registrado")


@router.delete("/{vendedor_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_vendedor(vendedor_id: int, db: Session = Depends(get_db)):
    vendedor = repo.obtener(db, vendedor_id)
    if vendedor is None:
        raise HTTPException(status_code=404, detail="Vendedor no encontrado")
    repo.eliminar(db, vendedor)
