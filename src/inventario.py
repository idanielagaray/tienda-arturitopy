"""CRUD de productos (M1): registrar, consultar, modificar y eliminar."""

from tabulate import tabulate

import validaciones

CATEGORIAS = ["Lacteos", "Bebidas", "Aseo", "Abarrotes", "Snacks"]


def formato_cop(valor):
    """4200.0 -> $4.200"""
    return "$" + f"{valor:,.0f}".replace(",", ".")


def elegir_categoria():
    """Muestra las categorías numeradas y devuelve la elegida."""
    for numero, nombre in enumerate(CATEGORIAS, 1):
        print(f"  {numero}. {nombre}")
    opcion = validaciones.pedir_opcion("Elige la categoría: ", 1, len(CATEGORIAS))
    return CATEGORIAS[opcion - 1]


def mostrar_productos(lista_productos):
    """Imprime una tabla con los productos de la lista."""
    filas = []
    for p in lista_productos:
        filas.append([
            p["codigo"], p["nombre"], p["categoria"], formato_cop(p["precio"]),
            p["stock"], p["stock_minimo"], p["proveedor"],
        ])
    encabezados = ["Código", "Nombre", "Categoría", "Precio", "Stock", "Stock mín.", "Proveedor"]
    print(tabulate(filas, headers=encabezados, tablefmt="grid"))


def registrar_producto(inventario):
    """Registra un producto nuevo. Si el código ya existe, lanza ValueError."""
    print("\n--- REGISTRAR PRODUCTO ---")
    codigo = validaciones.pedir_codigo("Código (ej. LAC001): ")
    if codigo in inventario:
        raise ValueError(f"El código {codigo} ya existe. No se puede repetir.")

    nombre = validaciones.pedir_texto("Nombre: ")
    categoria = elegir_categoria()
    precio = validaciones.pedir_decimal("Precio de venta (COP): ")
    stock = validaciones.pedir_entero("Stock (unidades disponibles): ")
    stock_minimo = validaciones.pedir_entero("Stock mínimo para alerta: ")
    proveedor = validaciones.pedir_texto("Proveedor: ")

    inventario[codigo] = {
        "codigo": codigo,
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "stock": stock,
        "stock_minimo": stock_minimo,
        "proveedor": proveedor,
    }
    print(f"Producto {codigo} registrado correctamente.")


def consultar_por_codigo(inventario):
    print("\n--- CONSULTAR POR CÓDIGO ---")
    codigo = validaciones.pedir_codigo("Código del producto: ")
    if codigo in inventario:
        mostrar_productos([inventario[codigo]])
    else:
        print(f"No existe ningún producto con el código {codigo}.")


def consultar_por_categoria(inventario):
    print("\n--- CONSULTAR POR CATEGORÍA ---")
    categoria = elegir_categoria()
    encontrados = []
    for p in inventario.values():
        if p["categoria"].lower() == categoria.lower():
            encontrados.append(p)
    if len(encontrados) == 0:
        print(f"No hay productos en la categoría {categoria}.")
    else:
        mostrar_productos(encontrados)


def ver_inventario(inventario):
    print("\n--- INVENTARIO COMPLETO ---")
    if len(inventario) == 0:
        print("El inventario está vacío.")
    else:
        mostrar_productos(inventario.values())


def modificar_producto(inventario):
    """Cambia el precio o el stock de un producto que ya existe."""
    print("\n--- MODIFICAR PRODUCTO ---")
    codigo = validaciones.pedir_codigo("Código del producto: ")
    if codigo not in inventario:
        print(f"No existe ningún producto con el código {codigo}.")
        return

    producto = inventario[codigo]
    mostrar_productos([producto])
    print("1. Cambiar precio")
    print("2. Cambiar stock")
    opcion = validaciones.pedir_opcion("Elige qué modificar: ", 1, 2)
    if opcion == 1:
        producto["precio"] = validaciones.pedir_decimal("Nuevo precio (COP): ")
        print("Precio actualizado.")
    else:
        producto["stock"] = validaciones.pedir_entero("Nuevo stock (total de unidades): ")
        print("Stock actualizado.")


def eliminar_producto(inventario):
    print("\n--- ELIMINAR PRODUCTO ---")
    codigo = validaciones.pedir_codigo("Código del producto: ")
    if codigo not in inventario:
        print(f"No existe ningún producto con el código {codigo}.")
        return

    mostrar_productos([inventario[codigo]])
    if validaciones.pedir_si_no("¿Seguro que quieres eliminarlo?"):
        del inventario[codigo]
        print("Producto eliminado.")
    else:
        print("No se eliminó nada.")
