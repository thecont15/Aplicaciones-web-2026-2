import sys

from sqlalchemy import text

from src.database.database import engine


def main() -> int:
    try:
        with engine.connect() as conexion:
            if engine.dialect.name == "postgresql":
                version = conexion.execute(text("SELECT version()")).scalar()
                print(f"Conexion correcta. PostgreSQL: {version}")
            else:
                conexion.execute(text("SELECT 1"))
                print(f"Conexion correcta. Motor: {engine.dialect.name}")
    except Exception as error:
        print(f"ERROR: no se pudo conectar a la base de datos -> {error}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
