from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.database import Base, SessionLocal, engine
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


def main() -> None:
    crear_tablas()

    db = SessionLocal()
    try:
        total = sembrar_vendedores(db)
    finally:
        db.close()

    print(f"Seeder terminado. Filas nuevas: {total}")


if __name__ == "__main__":
    main()
