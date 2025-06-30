from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str

    cotizaciones: List["Cotizacion"] = Relationship(back_populates="usuario")


class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    precio_m2: float
    segmento: Optional[str] = Field(default=None, index=True)


class Cotizacion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="user.id")
    fecha: datetime = Field(default_factory=datetime.utcnow)
    total: float

    usuario: Optional[User] = Relationship(back_populates="cotizaciones")
    items: List["CotizacionItem"] = Relationship(back_populates="cotizacion")


class CotizacionItem(SQLModel, table=True):
    cotizacion_id: int = Field(foreign_key="cotizacion.id", primary_key=True)
    producto_id: int = Field(foreign_key="producto.id", primary_key=True)
    m2: float

    producto: Optional[Producto] = Relationship()
    cotizacion: Optional[Cotizacion] = Relationship(back_populates="items")
