from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, SQLModel

from .db import get_session
from .models import Cotizacion, CotizacionItem, Producto
from .auth import get_current_user
from .rules.engine import calcular_total

router = APIRouter(prefix="/cotizaciones", tags=["cotizaciones"])


class ItemIn(SQLModel):
    producto_id: int
    m2: float


class CotizacionCreate(SQLModel):
    items: List[ItemIn]


class CotizacionRead(SQLModel):
    id: int
    fecha: datetime
    total: float
    items: List[ItemIn]


@router.post("/", response_model=CotizacionRead)
async def crear_cotizacion(
    cotizacion_in: CotizacionCreate,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    producto_ids = [i.producto_id for i in cotizacion_in.items]
    productos = session.exec(select(Producto).where(Producto.id.in_(producto_ids))).all()
    if len(productos) != len(producto_ids):
        raise HTTPException(status_code=400, detail="Producto no existe")
    precios = {p.id: p.precio_m2 for p in productos}
    total = calcular_total([i.dict() for i in cotizacion_in.items], precios)

    cotizacion = Cotizacion(usuario_id=user.id, total=total)
    session.add(cotizacion)
    session.commit()
    session.refresh(cotizacion)

    for item in cotizacion_in.items:
        ci = CotizacionItem(cotizacion_id=cotizacion.id, producto_id=item.producto_id, m2=item.m2)
        session.add(ci)
    session.commit()

    return CotizacionRead(id=cotizacion.id, fecha=cotizacion.fecha, total=total, items=cotizacion_in.items)


@router.get("/{cotizacion_id}", response_model=CotizacionRead)
async def leer_cotizacion(
    cotizacion_id: int,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    cotizacion = session.get(Cotizacion, cotizacion_id)
    if not cotizacion or cotizacion.usuario_id != user.id:
        raise HTTPException(status_code=404, detail="Cotizacion no encontrada")
    items = session.exec(select(CotizacionItem).where(CotizacionItem.cotizacion_id == cotizacion.id)).all()
    items_out = [ItemIn(producto_id=i.producto_id, m2=i.m2) for i in items]
    return CotizacionRead(id=cotizacion.id, fecha=cotizacion.fecha, total=cotizacion.total, items=items_out)
