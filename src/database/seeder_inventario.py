"""Migracion y seeder de la entidad Inventario.

Crea la tabla 'inventarios' si no existe y siembra registros de ejemplo.
Es idempotente: si un registro ya existe por SKU, lo salta.
"""

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.database import SessionLocal, engine
from src.entities.inventario import Inventario

INVENTARIOS_SEMILLA = [
    {
        "sku": "TEC-K80-001",
        "nombre_producto": "Teclado Mecanico K80",
        "descripcion": "Teclado mecanico con switches rojos",
        "categoria": "Perifericos",
        "precio": Decimal("89.90"),
        "cantidad": 15,
        "stock_minimo": 5,
        "activo": True,
    },
    {
        "sku": "MOU-M720-001",
        "nombre_producto": "Mouse Inalambrico M720",
        "descripcion": "Mouse ergonomico multi-dispositivo",
        "categoria": "Perifericos",
        "precio": Decimal("45.50"),
        "cantidad": 30,
        "stock_minimo": 10,
        "activo": True,
    },
    {
        "sku": "MON-QHD27-001",
        "nombre_producto": "Monitor 27 pulgadas QHD",
        "descripcion": "Monitor IPS 144 Hz",
        "categoria": "Monitores",
        "precio": Decimal("230.00"),
        "cantidad": 8,
        "stock_minimo": 3,
        "activo": True,
    },
    {
        "sku": "WEB-C920-001",
        "nombre_producto": "Webcam Full HD C920",
        "descripcion": "Webcam 1080p con microfono dual",
        "categoria": "Camaras",
        "precio": Decimal("65.00"),
        "cantidad": 12,
        "stock_minimo": 4,
        "activo": True,
    },
]


def migrar_tabla_inventario() -> None:
    """Crea la tabla inventarios si aun no existe."""
    Inventario.__table__.create(bind=engine, checkfirst=True)
    print("Tabla 'inventarios' verificada/creada.")


def sembrar_inventarios(db: Session) -> int:
    insertadas = 0

    for datos in INVENTARIOS_SEMILLA:
        existe = db.scalar(select(Inventario).where(Inventario.sku == datos["sku"]))
        if existe is not None:
            print(f"Ya existe: {datos['sku']}")
            continue

        db.add(Inventario(**datos))
        insertadas += 1
        print(f"Insertado: {datos['sku']} - {datos['nombre_producto']}")

    db.commit()
    return insertadas


def main() -> None:
    migrar_tabla_inventario()

    db = SessionLocal()
    try:
        total = sembrar_inventarios(db)
    finally:
        db.close()

    print(f"Seeder de inventario terminado. Filas nuevas: {total}")


if __name__ == "__main__":
    main()
