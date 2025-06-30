from typing import Iterable, Mapping


def calcular_total(items: Iterable[Mapping], productos: Mapping[int, float]) -> float:
    """Calcula el total de una cotizacion.

    items: iterable de dicts con keys ``producto_id`` y ``m2``.
    productos: mapping de producto_id a precio_m2.
    """
    total = 0.0
    for item in items:
        precio = productos.get(item["producto_id"], 0)
        m2 = item["m2"]
        subtotal = precio * m2
        if m2 >= 200:
            subtotal *= 0.95  # 5% descuento
        total += round(subtotal, 2)
    return round(total, 2)
