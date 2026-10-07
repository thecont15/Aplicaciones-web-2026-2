from decimal import Decimal
from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

T = TypeVar("T")


class RespuestaAPI(BaseModel, Generic[T]):
    data: T
    status: int
    message: str


class InventarioBase(BaseModel):
    sku: str = Field(min_length=1, max_length=50)
    nombre_producto: str = Field(min_length=1, max_length=150)
    descripcion: str | None = None
    categoria: str | None = Field(default=None, max_length=100)
    precio: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    cantidad: int = Field(default=0, ge=0)
    stock_minimo: int = Field(default=0, ge=0)
    activo: bool = True

    @field_validator("sku", "nombre_producto")
    @classmethod
    def validar_texto_requerido(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError("El valor no puede estar vacio")
        return valor

    @field_validator("descripcion", "categoria")
    @classmethod
    def normalizar_texto_opcional(cls, valor: str | None) -> str | None:
        if valor is None:
            return None
        valor = valor.strip()
        return valor or None


class InventarioCrear(InventarioBase):
    pass


class InventarioActualizar(BaseModel):
    sku: str | None = Field(default=None, min_length=1, max_length=50)
    nombre_producto: str | None = Field(default=None, min_length=1, max_length=150)
    descripcion: str | None = None
    categoria: str | None = Field(default=None, max_length=100)
    precio: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    cantidad: int | None = Field(default=None, ge=0)
    stock_minimo: int | None = Field(default=None, ge=0)
    activo: bool | None = None

    @field_validator("sku", "nombre_producto")
    @classmethod
    def validar_texto_requerido(cls, valor: str | None) -> str | None:
        if valor is None:
            raise ValueError("El valor no puede ser nulo")
        valor = valor.strip()
        if not valor:
            raise ValueError("El valor no puede estar vacio")
        return valor

    @field_validator("descripcion", "categoria")
    @classmethod
    def normalizar_texto_opcional(cls, valor: str | None) -> str | None:
        if valor is None:
            return None
        valor = valor.strip()
        return valor or None

    @model_validator(mode="after")
    def validar_cambios(self):
        if not self.model_fields_set:
            raise ValueError("Debe enviar al menos un campo para actualizar")
        for campo in ("precio", "cantidad", "stock_minimo", "activo"):
            if campo in self.model_fields_set and getattr(self, campo) is None:
                raise ValueError(f"{campo} no puede ser nulo")
        return self


class InventarioRespuesta(InventarioBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
