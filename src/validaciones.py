"""Captura segura de datos: si el usuario se equivoca, se vuelve a preguntar."""

LIMITE_MAXIMO = 1000000000  # evita números absurdos (por ejemplo "inf")


def pedir_texto(mensaje):
    """Pide un texto que no esté vacío y que no tenga el caracter '|'."""
    while True:
        texto = input(mensaje).strip()
        if texto == "":
            print("Error: este dato no puede estar vacío.")
        elif "|" in texto:
            print("Error: no se puede usar el caracter '|'.")
        else:
            return texto


def pedir_codigo(mensaje, permitir_vacio=False):
    """Pide un código de producto (se guarda en mayúsculas)."""
    while True:
        codigo = input(mensaje).strip().upper()
        if codigo == "" and permitir_vacio:
            return ""
        if codigo == "":
            print("Error: el código no puede estar vacío.")
        elif "|" in codigo or ":" in codigo or ";" in codigo:
            print("Error: el código no puede tener los caracteres | : ;")
        else:
            return codigo


def pedir_entero(mensaje):
    """Pide un número entero mayor que cero."""
    while True:
        try:
            numero = int(input(mensaje))
        except ValueError:
            print("Error: escribe un número entero (sin letras ni decimales).")
            continue
        if numero <= 0:
            print("Error: el valor debe ser mayor que cero.")
        elif numero > LIMITE_MAXIMO:
            print("Error: el número es demasiado grande.")
        else:
            return numero


def pedir_decimal(mensaje):
    """Pide un número (puede tener decimales) mayor que cero."""
    while True:
        try:
            numero = float(input(mensaje))
        except ValueError:
            print("Error: escribe un número (por ejemplo 4500 o 4500.5).")
            continue
        if not numero > 0:
            print("Error: el valor debe ser mayor que cero.")
        elif numero > LIMITE_MAXIMO:
            print("Error: el número es demasiado grande.")
        else:
            return numero


def pedir_opcion(mensaje, minimo, maximo):
    """Pide un número entero entre minimo y maximo (ambos incluidos)."""
    while True:
        try:
            numero = int(input(mensaje))
        except ValueError:
            print("Error: escribe solo el número de la opción.")
            continue
        if numero < minimo or numero > maximo:
            print(f"Error: elige un número entre {minimo} y {maximo}.")
        else:
            return numero


def pedir_si_no(mensaje):
    """Pide s o n. Devuelve True si responde que sí."""
    while True:
        respuesta = input(mensaje + " (s/n): ").strip().lower()
        if respuesta in ("s", "si", "sí"):
            return True
        if respuesta in ("n", "no"):
            return False
        print("Error: responde con 's' o 'n'.")
