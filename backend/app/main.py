from fastapi import FastAPI

from .db import engine
from sqlmodel import SQLModel
from .auth import router as auth_router
from .productos import router as productos_router
from .cotizaciones import router as cotizaciones_router
from .historial import router as historial_router

app = FastAPI(title="Cotizador Inteligente")

SQLModel.metadata.create_all(engine)

app.include_router(auth_router)
app.include_router(productos_router)
app.include_router(cotizaciones_router)
app.include_router(historial_router)


@app.get("/")
async def read_root():
    return {"message": "Backend del cotizador funcionando"}
