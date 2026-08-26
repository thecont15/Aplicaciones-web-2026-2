from sqlalchemy import select
from sqlalchemy.orm import Session

from src.entities.cliente import Cliente


def consultar_todos(db: Session) -> list[Cliente]:
    return list(db.scalars(select(Cliente).order_by(Cliente.id)))


def buscar_por_id(db: Session, cliente_id: int) -> Cliente | None:
    return db.get(Cliente, cliente_id)


def registrar(db: Session, datos: dict) -> Cliente:
    cliente = Cliente(**datos)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def modificar(db: Session, cliente: Cliente, datos: dict) -> Cliente:
    for campo, valor in datos.items():
        setattr(cliente, campo, valor)
    db.commit()
    db.refresh(cliente)
    return cliente


def dar_de_baja(db: Session, cliente: Cliente) -> None:
    db.delete(cliente)
    db.commit()
