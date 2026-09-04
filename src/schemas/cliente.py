from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    apellido: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., max_length=255)
    telefono: str | None = Field(None, max_length=30)
    activo: bool = True


class ClienteCrear(ClienteBase):
    pass


class ClienteActualizar(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=100)
    apellido: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = Field(None, max_length=255)
    telefono: str | None = Field(None, max_length=30)
    activo: bool | None = None


class ClienteRespuesta(ClienteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
