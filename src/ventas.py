"""Carrito, descuentos y cambio (M2)."""

import datetime

from tabulate import tabulate

import inventario as mod_inventario
import persistencia
import validaciones

formato_cop = mod_inventario.formato_cop


def calcular_descuento(subtotal):
    """Devuelve el porcentaje de descuento (como decimal) según el subtotal."""
    if subtotal >= 100000:
        return 0.10
    if subtotal >= 50000:
        return 0.05
    return 0.0


def agregar_al_carrito(inventario, carrito, codigo, cantidad):
    """Agrega un producto al carrito. Lanza ValueError si no hay stock suficiente."""
    producto = inventario[codigo]
    ya_en_carrito = carrito.get(codigo, 0)
    if ya_en_carrito + cantidad > producto["stock"]:
        raise ValueError(
            f"Stock insuficiente de {producto['nombre']}: "
            f"hay {producto['stock']} unidades y ya llevas {ya_en_carrito} en el carrito."
        )
    carrito[codigo] = ya_en_carrito + cantidad


def calcular_subtotal(inventario, carrito):
    subtotal = 0.0
    for codigo, cantidad in carrito.items():
        subtotal = subtotal + inventario[codigo]["precio"] * cantidad
    return subtotal


def mostrar_detalle(inventario, carrito, subtotal, descuento, total):
    filas = []
    for codigo, cantidad in carrito.items():
        precio = inventario[codigo]["precio"]
        filas.append([inventario[codigo]["nombre"], cantidad, formato_cop(precio * cantidad)])
    print(tabulate(filas, headers=["Producto", "Cantidad", "Valor"], tablefmt="grid"))
    print(f"Subtotal:  {formato_cop(subtotal)}")
    print(f"Descuento: {int(descuento * 100)}% (-{formato_cop(subtotal * descuento)})")
    print(f"TOTAL:     {formato_cop(total)}")


def validar_pago(pago, total):
    """Lanza ValueError si el pago es menor que el total."""
    if pago < total:
        raise ValueError(f"Pago insuficiente: faltan {formato_cop(total - pago)}.")


def confirmar_venta(inventario, carrito, total):
    """Registra la venta en el archivo y descuenta el stock.
    Primero revisa todo, así el inventario no cambia si algo falla."""
    for codigo, cantidad in carrito.items():
        if cantidad > inventario[codigo]["stock"]:
            raise ValueError(f"El stock de {inventario[codigo]['nombre']} cambió y ya no alcanza.")

    fecha = datetime.date.today().isoformat()
    persistencia.registrar_venta(fecha, total, carrito)

    for codigo, cantidad in carrito.items():
        inventario[codigo]["stock"] = inventario[codigo]["stock"] - cantidad


def realizar_venta(inventario):
    """Flujo completo de una venta. Devuelve True si la venta se confirmó."""
    print("\n--- NUEVA VENTA ---")
    if len(inventario) == 0:
        print("No hay productos en el inventario.")
        return False

    carrito = {}
    while True:
        codigo = validaciones.pedir_codigo("Código del producto (ENTER para terminar): ", permitir_vacio=True)
        if codigo == "":
            break
        if codigo not in inventario:
            print(f"No existe ningún producto con el código {codigo}.")
            continue

        producto = inventario[codigo]
        print(f"{producto['nombre']} - {formato_cop(producto['precio'])} - stock: {producto['stock']}")
        cantidad = validaciones.pedir_entero("Cantidad: ")
        try:
            agregar_al_carrito(inventario, carrito, codigo, cantidad)
            print("Agregado al carrito.")
        except ValueError as error:
            print(f"No se pudo agregar: {error}")

    if len(carrito) == 0:
        print("Venta cancelada: el carrito está vacío.")
        return False

    subtotal = calcular_subtotal(inventario, carrito)
    descuento = calcular_descuento(subtotal)
    total = round(subtotal - subtotal * descuento, 2)

    print("\n--- DETALLE DE LA VENTA ---")
    mostrar_detalle(inventario, carrito, subtotal, descuento, total)

    if not validaciones.pedir_si_no("¿Confirmar la venta?"):
        print("Venta cancelada. El inventario no cambió.")
        return False

    # Cobro: se repite hasta que el pago alcance
    while True:
        pago = validaciones.pedir_decimal("Pago recibido (COP): ")
        try:
            validar_pago(pago, total)
            break
        except ValueError as error:
            print(f"Error: {error} Intenta de nuevo.")

    confirmar_venta(inventario, carrito, total)
    print(f"Cambio a devolver: {formato_cop(pago - total)}")
    print("Venta registrada correctamente.")
    return True
