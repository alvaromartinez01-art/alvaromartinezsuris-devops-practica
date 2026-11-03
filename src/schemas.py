from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator


class UsuarioCreate(BaseModel):
    tipo: Literal["cliente", "administrador"]
    nombre: str = Field(min_length=1)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    direccion: Optional[str] = None

    @model_validator(mode="after")
    def cliente_necesita_direccion(self):
        if self.tipo == "cliente" and not self.direccion:
            raise ValueError("Un cliente necesita direccion postal")
        return self


class UsuarioRead(BaseModel):
    id: str
    nombre: str
    email: str
    es_admin: bool


class ProductoCreate(BaseModel):
    tipo: Literal["generico", "electronico", "ropa"]
    nombre: str = Field(min_length=1)
    precio: float = Field(gt=0)
    stock: int = Field(ge=0)
    meses_garantia: Optional[int] = Field(default=None, ge=0)
    talla: Optional[str] = None
    color: Optional[str] = None

    @model_validator(mode="after")
    def atributos_segun_tipo(self):
        if self.tipo == "electronico" and self.meses_garantia is None:
            raise ValueError("Un producto electronico necesita meses_garantia")
        if self.tipo == "ropa" and not (self.talla and self.color):
            raise ValueError("Un producto de ropa necesita talla y color")
        return self


class ProductoRead(BaseModel):
    id: str
    tipo: str
    nombre: str
    precio: float
    stock: int
    meses_garantia: Optional[int] = None
    talla: Optional[str] = None
    color: Optional[str] = None


class PedidoItemCreate(BaseModel):
    producto_id: str
    cantidad: int = Field(gt=0)


class PedidoCreate(BaseModel):
    cliente_id: str
    items: list[PedidoItemCreate] = Field(min_length=1)


class PedidoItemRead(BaseModel):
    producto_id: str
    nombre: str
    precio_unitario: float
    cantidad: int
    subtotal: float


class PedidoRead(BaseModel):
    id: str
    fecha: datetime
    cliente: UsuarioRead
    total: float
    items: list[PedidoItemRead]
