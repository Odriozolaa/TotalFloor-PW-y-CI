from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, SQLModel, Field

from .db import get_session
from .models import Producto
from .auth import get_current_user

router = APIRouter(prefix="/productos", tags=["productos"])


class ProductoBase(SQLModel):
    nombre: str
    precio_m2: float
    segmento: Optional[str] = None


class ProductoCreate(ProductoBase):
    pass


class ProductoRead(ProductoBase):
    id: int


@router.post("/", response_model=ProductoRead)
async def create_producto(
    producto: ProductoCreate,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    db_producto = Producto.from_orm(producto)
    session.add(db_producto)
    session.commit()
    session.refresh(db_producto)
    return db_producto


@router.get("/", response_model=List[ProductoRead])
async def list_productos(
    segmento: Optional[str] = None,
    precio_max: Optional[float] = None,
    session: Session = Depends(get_session),
):
    query = select(Producto)
    if segmento:
        query = query.where(Producto.segmento == segmento)
    if precio_max:
        query = query.where(Producto.precio_m2 <= precio_max)
    productos = session.exec(query).all()
    return productos


@router.get("/{producto_id}", response_model=ProductoRead)
async def get_producto(producto_id: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.put("/{producto_id}", response_model=ProductoRead)
async def update_producto(
    producto_id: int,
    producto_in: ProductoCreate,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for k, v in producto_in.dict().items():
        setattr(producto, k, v)
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


@router.delete("/{producto_id}")
async def delete_producto(
    producto_id: int,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    session.delete(producto)
    session.commit()
    return {"ok": True}
