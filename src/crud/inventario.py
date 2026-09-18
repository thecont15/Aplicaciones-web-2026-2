from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.entities.inventario import Inventario


def listar(db: Session) -> list[Inventario]:
    return list(db.scalars(select(Inventario).order_by(Inventario.id)))


def obtener(db: Session, inventario_id: UUID) -> Inventario | None:
    return db.get(Inventario, inventario_id)


def crear(db: Session, datos: dict) -> Inventario:
    inventario = Inventario(**datos)
    db.add(inventario)
    db.commit()
    db.refresh(inventario)
    return inventario


def actualizar(db: Session, inventario: Inventario, datos: dict) -> Inventario:
    for campo, valor in datos.items():
        setattr(inventario, campo, valor)
    db.commit()
    db.refresh(inventario)
    return inventario


def eliminar(db: Session, inventario: Inventario) -> None:
    db.delete(inventario)
    db.commit()
