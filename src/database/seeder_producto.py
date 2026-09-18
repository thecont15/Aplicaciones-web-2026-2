"""Migracion y seeder de la entidad Producto (integrante: Daproyect).

Crea la tabla 'productos' si no existe y siembra 4 productos de ejemplo.
Es idempotente: si un producto ya existe por nombre, lo salta.
"""

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.database import SessionLocal, engine
from src.entities.producto import Producto

PRODUCTOS_SEMILLA = [
    {
        "nombre": "Teclado Mecanico K80",
        "descripcion": "Teclado mecanico con switches rojos",
        "precio": Decimal("89.90"),
        "stock": 15,
        "activo": True,
    },
    {
        "nombre": "Mouse Inalambrico M720",
        "descripcion": "Mouse ergonomico multi-dispositivo",
        "precio": Decimal("45.50"),
        "stock": 30,
        "activo": True,
    },
    {
        "nombre": "Monitor 27 pulgadas QHD",
        "descripcion": "Monitor IPS 144 Hz",
        "precio": Decimal("230.00"),
        "stock": 8,
        "activo": True,
    },
    {
        "nombre": "Webcam Full HD C920",
        "descripcion": "Webcam 1080p con microfono dual",
        "precio": Decimal("65.00"),
        "stock": 12,
        "activo": True,
    },
]


def migrar_tabla_producto() -> None:
    """Crea la tabla productos si aun no existe. No toca las demas tablas."""
    Producto.__table__.create(bind=engine, checkfirst=True)
    print("Tabla 'productos' verificada/creada.")


def sembrar_productos(db: Session) -> int:
    insertadas = 0

    for datos in PRODUCTOS_SEMILLA:
        existe = db.scalar(
            select(Producto).where(Producto.nombre == datos["nombre"])
        )
        if existe is not None:
            print(f"Ya existe: {datos['nombre']}")
            continue

        db.add(Producto(**datos))
        insertadas += 1
        print(f"Insertado: {datos['nombre']}")

    db.commit()
    return insertadas


def main() -> None:
    migrar_tabla_producto()

    db = SessionLocal()
    try:
        total = sembrar_productos(db)
    finally:
        db.close()

    print(f"Seeder de productos terminado. Filas nuevas: {total}")


if __name__ == "__main__":
    main()
