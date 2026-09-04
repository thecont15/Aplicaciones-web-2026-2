from sqlalchemy import select
from sqlalchemy.orm import Session

from src.entities.vendedor import Vendedor


def listar(db: Session) -> list[Vendedor]:
    return list(db.scalars(select(Vendedor).order_by(Vendedor.id)))


def obtener(db: Session, vendedor_id: int) -> Vendedor | None:
    return db.get(Vendedor, vendedor_id)


def crear(db: Session, datos: dict) -> Vendedor:
    vendedor = Vendedor(**datos)
    db.add(vendedor)
    db.commit()
    db.refresh(vendedor)
    return vendedor


def actualizar(db: Session, vendedor: Vendedor, datos: dict) -> Vendedor:
    for campo, valor in datos.items():
        setattr(vendedor, campo, valor)
    db.commit()
    db.refresh(vendedor)
    return vendedor


def eliminar(db: Session, vendedor: Vendedor) -> None:
    db.delete(vendedor)
    db.commit()
