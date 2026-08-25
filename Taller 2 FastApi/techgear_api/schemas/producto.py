from pydantic import BaseModel, Field


class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: str = Field(..., min_length=5, max_length=500)
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    categoria: str = Field(..., min_length=2, max_length=50)


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=2, max_length=100)
    descripcion: str | None = Field(None, min_length=5, max_length=500)
    precio: float | None = Field(None, gt=0)
    stock: int | None = Field(None, ge=0)
    categoria: str | None = Field(None, min_length=2, max_length=50)


class ProductoResponse(ProductoBase):
    id: str