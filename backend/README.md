# Backend Cotizador Inteligente

Este proyecto contiene un backend basado en FastAPI para el cotizador que será consumido por un frontend Angular.

## Puesta en marcha

1. Crear un entorno virtual y activar.
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Iniciar el servidor:
   ```bash
   uvicorn app.main:app --reload
   ```

El servidor levanta la documentación Swagger automáticamente en `http://localhost:8000/docs`.

## Ejemplo de uso

Crear una cotización enviando items:

```bash
curl -X POST http://localhost:8000/cotizaciones \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"items":[{"producto_id":1,"m2":250}]}'
```
