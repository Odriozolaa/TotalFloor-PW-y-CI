from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlmodel import Session, select, SQLModel

from .db import get_session
from .models import Cotizacion, CotizacionItem
from .auth import get_current_user
from .cotizaciones import ItemIn, CotizacionRead

router = APIRouter(prefix="/historial", tags=["historial"])


@router.get("/", response_model=List[CotizacionRead])
async def historial(
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    cotizaciones = session.exec(select(Cotizacion).where(Cotizacion.usuario_id == user.id)).all()
    result: List[CotizacionRead] = []
    for c in cotizaciones:
        items = session.exec(select(CotizacionItem).where(CotizacionItem.cotizacion_id == c.id)).all()
        items_out = [ItemIn(producto_id=i.producto_id, m2=i.m2) for i in items]
        result.append(CotizacionRead(id=c.id, fecha=c.fecha, total=c.total, items=items_out))
    return result
