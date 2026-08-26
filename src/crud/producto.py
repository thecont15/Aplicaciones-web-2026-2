from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.entities.producto import Producto


def listar(db: Session) -> list[Producto]:
    return list(db.scalars(select(Producto).order_by(Producto.id)))


def obtener(db: Session, producto_id: int) -> Producto | None:
    return db.get(Producto, producto_id)


def crear(db: Session, datos: dict) -> Producto:
    producto = Producto(**datos)
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


def actualizar(db: Session, producto: Producto, datos: dict) -> Producto:
    for campo, valor in datos.items():
        setattr(producto, campo, valor)
    db.commit()
    db.refresh(producto)
    return producto


def eliminar(db: Session, producto: Producto) -> None:
    db.delete(producto)
    db.commit()