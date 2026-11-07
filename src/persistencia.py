"""Lectura y escritura de archivos de texto plano.

Inventario:  data/inventario.txt  ->  codigo|nombre|categoria|precio|stock|stock_minimo|proveedor
Ventas:      data/ventas.txt      ->  fecha|total|codigo:cantidad;codigo:cantidad
"""

import os

# La carpeta data/ queda junto a la carpeta src/, sin importar desde dónde se ejecute
RUTA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_INVENTARIO = os.path.join(RUTA_BASE, "data", "inventario.txt")
RUTA_VENTAS = os.path.join(RUTA_BASE, "data", "ventas.txt")


def crear_carpeta_data():
    os.makedirs(os.path.join(RUTA_BASE, "data"), exist_ok=True)


# ---------------------------------------------------------------- inventario
def linea_a_producto(linea):
    """Convierte una línea del archivo en un diccionario.
    Si la línea está mal escrita, lanza ValueError."""
    partes = linea.split("|")
    if len(partes) != 7:
        raise ValueError("se esperaban 7 campos separados por '|'")

    codigo = partes[0].strip().upper()
    nombre = partes[1].strip()
    categoria = partes[2].strip()
    proveedor = partes[6].strip()
    precio = float(partes[3])
    stock = int(partes[4])
    stock_minimo = int(partes[5])

    if codigo == "" or nombre == "" or categoria == "" or proveedor == "":
        raise ValueError("hay campos de texto vacíos")
    if not precio > 0:
        raise ValueError("el precio debe ser mayor que cero")
    if stock < 0 or stock_minimo < 0:
        raise ValueError("el stock no puede ser negativo")

    return {
        "codigo": codigo,
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "stock": stock,
        "stock_minimo": stock_minimo,
        "proveedor": proveedor,
    }


def cargar_inventario():
    """Lee el inventario. Devuelve un diccionario {codigo: producto}."""
    inventario = {}
    try:
        with open(RUTA_INVENTARIO, "r", encoding="utf-8") as archivo:
            numero_linea = 0
            for linea in archivo:
                numero_linea += 1
                linea = linea.strip()
                if linea == "":
                    continue
                try:
                    producto = linea_a_producto(linea)
                except ValueError as error:
                    print(f"Advertencia: línea {numero_linea} omitida ({error}).")
                    continue
                if producto["codigo"] in inventario:
                    print(f"Advertencia: línea {numero_linea} omitida (código repetido).")
                    continue
                inventario[producto["codigo"]] = producto
    except FileNotFoundError:
        print("Aviso: no existe data/inventario.txt. Se inicia con un inventario vacío.")
    return inventario


def guardar_inventario(inventario):
    """Guarda todos los productos, uno por línea."""
    crear_carpeta_data()
    with open(RUTA_INVENTARIO, "w", encoding="utf-8") as archivo:
        for p in inventario.values():
            linea = "|".join([
                p["codigo"],
                p["nombre"],
                p["categoria"],
                str(p["precio"]),
                str(p["stock"]),
                str(p["stock_minimo"]),
                p["proveedor"],
            ])
            archivo.write(linea + "\n")


# -------------------------------------------------------------------- ventas
def linea_a_venta(linea):
    """Convierte 'fecha|total|COD:cant;COD:cant' en un diccionario.
    Si la línea está mal escrita, lanza ValueError."""
    partes = linea.split("|")
    if len(partes) != 3:
        raise ValueError("se esperaban 3 campos separados por '|'")

    fecha = partes[0].strip()
    total = float(partes[1])
    if fecha == "" or total < 0:
        raise ValueError("fecha vacía o total negativo")

    items = {}
    for texto in partes[2].split(";"):
        pareja = texto.split(":")
        if len(pareja) != 2:
            raise ValueError("producto mal escrito, se esperaba codigo:cantidad")
        codigo = pareja[0].strip().upper()
        cantidad = int(pareja[1])
        if codigo == "" or cantidad <= 0:
            raise ValueError("código vacío o cantidad no válida")
        items[codigo] = items.get(codigo, 0) + cantidad

    return {"fecha": fecha, "total": total, "items": items}


def cargar_ventas():
    """Lee el historial de ventas. Devuelve una lista de diccionarios."""
    ventas = []
    try:
        with open(RUTA_VENTAS, "r", encoding="utf-8") as archivo:
            numero_linea = 0
            for linea in archivo:
                numero_linea += 1
                linea = linea.strip()
                if linea == "":
                    continue
                try:
                    ventas.append(linea_a_venta(linea))
                except ValueError as error:
                    print(f"Advertencia: venta de la línea {numero_linea} omitida ({error}).")
    except FileNotFoundError:
        pass  # todavía no hay ventas, es normal
    return ventas


def registrar_venta(fecha, total, carrito):
    """Agrega una venta al final de data/ventas.txt."""
    crear_carpeta_data()
    productos = []
    for codigo, cantidad in carrito.items():
        productos.append(f"{codigo}:{cantidad}")
    linea = f"{fecha}|{total}|" + ";".join(productos)
    with open(RUTA_VENTAS, "a", encoding="utf-8") as archivo:
        archivo.write(linea + "\n")
