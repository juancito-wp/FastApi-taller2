from pydantic import BaseModel, Field
from typing import List


class ProductoPedido(BaseModel):
    producto_id: str
    cantidad: int = Field(..., gt=0)


class PedidoCreate(BaseModel):
    usuario: str = Field(..., min_length=2, max_length=100)
    correo: str
    productos: List[ProductoPedido]

class ProductoDetallePedido(BaseModel):
    producto_id: str
    nombre: str
    cantidad: int
    precio_unitario: float


class PedidoResponse(BaseModel):
    id: str
    usuario: str
    correo: str
    productos: List[ProductoPedido]
    total: float