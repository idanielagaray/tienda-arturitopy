"""Alertas de stock (M3) y cierre del día (M4)."""

import datetime

from tabulate import tabulate

from inventario import formato_cop


def alertas_stock(inventario):
    """Lista los productos con stock <= stock mínimo, agrupados por proveedor."""
    print("\n--- ALERTAS DE STOCK ---")
    por_proveedor = {}
    for p in inventario.values():
        if p["stock"] <= p["stock_minimo"]:
            if p["proveedor"] not in por_proveedor:
                por_proveedor[p["proveedor"]] = []
            por_proveedor[p["proveedor"]].append(p)

    if len(por_proveedor) == 0:
        print("No hay productos por reabastecer. Todo en orden.")
        return

    for proveedor in sorted(por_proveedor):
        print(f"\nProveedor: {proveedor}")
        filas = []
        for p in por_proveedor[proveedor]:
            if p["stock"] == 0:
                estado = "AGOTADO"
            else:
                estado = "Stock bajo"
            filas.append([p["codigo"], p["nombre"], p["stock"], p["stock_minimo"], estado])
        print(tabulate(filas, headers=["Código", "Nombre", "Stock", "Mínimo", "Estado"], tablefmt="grid"))


def cierre_del_dia(inventario, ventas):
    """Resumen de las ventas de hoy."""
    hoy = datetime.date.today().isoformat()
    print(f"\n--- CIERRE DEL DÍA ({hoy}) ---")

    ventas_hoy = []
    for v in ventas:
        if v["fecha"] == hoy:
            ventas_hoy.append(v)

    total_vendido = 0.0
    unidades = {}  # codigo -> unidades vendidas hoy
    for v in ventas_hoy:
        total_vendido = total_vendido + v["total"]
        for codigo, cantidad in v["items"].items():
            unidades[codigo] = unidades.get(codigo, 0) + cantidad

    numero_ventas = len(ventas_hoy)
    if numero_ventas > 0:
        ticket_promedio = total_vendido / numero_ventas
    else:
        ticket_promedio = 0.0

    if len(unidades) > 0:
        codigo_top = max(unidades, key=unidades.get)
        if codigo_top in inventario:
            nombre_top = inventario[codigo_top]["nombre"]
        else:
            nombre_top = codigo_top
        mas_vendido = f"{nombre_top} ({unidades[codigo_top]} unidades)"
    else:
        mas_vendido = "Sin ventas"

    filas = [
        ["Total vendido", formato_cop(total_vendido)],
        ["Número de ventas", numero_ventas],
        ["Ticket promedio", formato_cop(ticket_promedio)],
        ["Producto más vendido", mas_vendido],
    ]
    print(tabulate(filas, tablefmt="grid"))

    # Productos sin ventas hoy
    sin_ventas = []
    for codigo, p in inventario.items():
        if codigo not in unidades:
            sin_ventas.append([codigo, p["nombre"]])
    print("\nProductos sin ventas hoy:")
    if len(sin_ventas) == 0:
        print("  (todos los productos tuvieron ventas)")
    else:
        print(tabulate(sin_ventas, headers=["Código", "Nombre"], tablefmt="grid"))

    # Categorías con movimiento
    categorias = []
    for codigo in unidades:
        if codigo in inventario:
            categoria = inventario[codigo]["categoria"]
            if categoria not in categorias:
                categorias.append(categoria)
    print("\nCategorías con movimiento:")
    if len(categorias) == 0:
        print("  (ninguna)")
    else:
        print("  " + ", ".join(categorias))
