from pydantic import BaseModel, Field
from typing import List


class ProductoPedido(BaseModel):
    producto_id: str
    cantidad: int = Field(..., gt=0)


class PedidoCreate(BaseModel):
    usuario: str = Field(..., min_length=2, max_length=100)
    correo: str = Field(..., pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    productos: List[ProductoPedido] = Field(..., min_length=1)

class ProductoDetallePedido(BaseModel):
    producto_id: str
    nombre: str
    cantidad: int
    precio_unitario: float


class PedidoResponse(BaseModel):
    id: str
    usuario: str
    correo: str = Field(..., pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    productos: List[ProductoDetallePedido]
    total: float = Field(..., ge=0)


class PedidoResumen(BaseModel):
    usuario: str
    correo: str = Field(..., pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    cantidad_pedidos: int = Field(..., ge=0)
    total_compras: float = Field(..., ge=0)