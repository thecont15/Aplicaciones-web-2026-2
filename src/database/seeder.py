from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.database import Base, SessionLocal, engine
from src.entities.cliente import Cliente
from src.entities.vendedor import Vendedor

VENDEDORES_SEMILLA = [
    {
        "nombre": "Ana",
        "apellido": "Pérez",
        "email": "ana.perez@empresa.com",
        "telefono": "3001112233",
        "activo": True,
    },
    {
        "nombre": "Carlos",
        "apellido": "Ramirez",
        "email": "carlos.ramirez@empresa.com",
        "telefono": "3002223344",
        "activo": True,
    },
    {
        "nombre": "Laura",
        "apellido": "Gomez",
        "email": "laura.gomez@empresa.com",
        "telefono": "3003334455",
        "activo": True,
    },
]

CLIENTES_SEMILLA = [
    {
        "nombre": "Maria",
        "apellido": "Lopez",
        "email": "maria.lopez@correo.com",
        "telefono": "3101112233",
        "activo": True,
    },
    {
        "nombre": "Pedro",
        "apellido": "Martinez",
        "email": "pedro.martinez@correo.com",
        "telefono": "3102223344",
        "activo": True,
    },
    {
        "nombre": "Sofia",
        "apellido": "Rodriguez",
        "email": "sofia.rodriguez@correo.com",
        "telefono": "3103334455",
        "activo": True,
    },
]


def crear_tablas() -> None:
    """Crea las tablas que aun no existen. No modifica las que ya estan."""
    Base.metadata.create_all(bind=engine)
    print("Tablas verificadas/creadas.")


def sembrar_vendedores(db: Session) -> int:
    insertadas = 0

    for datos in VENDEDORES_SEMILLA:
        existe = db.scalar(select(Vendedor).where(Vendedor.email == datos["email"]))
        if existe is not None:
            print(f"Ya existe: {datos['email']}")
            continue

        db.add(Vendedor(**datos))
        insertadas += 1
        print(f"Insertado: {datos['nombre']} {datos['apellido']}")

    db.commit()
    return insertadas


def sembrar_clientes(db: Session) -> int:
    insertadas = 0

    for datos in CLIENTES_SEMILLA:
        existe = db.scalar(select(Cliente).where(Cliente.email == datos["email"]))
        if existe is not None:
            print(f"Ya existe: {datos['email']}")
            continue

        db.add(Cliente(**datos))
        insertadas += 1
        print(f"Insertado: {datos['nombre']} {datos['apellido']}")

    db.commit()
    return insertadas


def main() -> None:
    crear_tablas()

    db = SessionLocal()
    try:
        total_vendedores = sembrar_vendedores(db)
        total_clientes = sembrar_clientes(db)
    finally:
        db.close()

    print(f"Seeder terminado. Vendedores nuevos: {total_vendedores}")
    print(f"Seeder terminado. Clientes nuevos: {total_clientes}")


if __name__ == "__main__":
    main()
