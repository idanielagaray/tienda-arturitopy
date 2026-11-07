"""TiendaPy - menú principal y flujo general.

Cómo ejecutarlo (desde la carpeta tiendapy/):
    python src/main.py
"""

import inventario as mod_inventario
import persistencia
import reportes
import validaciones
import ventas


def mostrar_menu():
    print("\n==============================")
    print("   TIENDAPY - Don Aurelio")
    print("==============================")
    print(" 1. Registrar producto")
    print(" 2. Consultar producto por código")
    print(" 3. Consultar productos por categoría")
    print(" 4. Ver inventario completo")
    print(" 5. Modificar precio o stock")
    print(" 6. Eliminar producto")
    print(" 7. Nueva venta")
    print(" 8. Alertas de stock")
    print(" 9. Cierre del día")
    print("10. Guardar inventario")
    print(" 0. Salir")


def main():
    inventario = persistencia.cargar_inventario()
    print(f"Inventario cargado: {len(inventario)} productos.")

    try:
        while True:
            mostrar_menu()
            opcion = validaciones.pedir_opcion("Elige una opción: ", 0, 10)

            # Cualquier violación de reglas de negocio (ValueError) se captura aquí
            try:
                if opcion == 1:
                    mod_inventario.registrar_producto(inventario)
                elif opcion == 2:
                    mod_inventario.consultar_por_codigo(inventario)
                elif opcion == 3:
                    mod_inventario.consultar_por_categoria(inventario)
                elif opcion == 4:
                    mod_inventario.ver_inventario(inventario)
                elif opcion == 5:
                    mod_inventario.modificar_producto(inventario)
                elif opcion == 6:
                    mod_inventario.eliminar_producto(inventario)
                elif opcion == 7:
                    if ventas.realizar_venta(inventario):
                        persistencia.guardar_inventario(inventario)  # guarda el nuevo stock
                elif opcion == 8:
                    reportes.alertas_stock(inventario)
                elif opcion == 9:
                    reportes.cierre_del_dia(inventario, persistencia.cargar_ventas())
                elif opcion == 10:
                    persistencia.guardar_inventario(inventario)
                    print("Inventario guardado.")
                elif opcion == 0:
                    break
            except ValueError as error:
                print(f"Error: {error}")
            except OSError as error:
                print(f"Error con los archivos: {error}")
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma interrumpido.")

    persistencia.guardar_inventario(inventario)
    print("Inventario guardado. ¡Hasta luego!")


if __name__ == "__main__":
    main()
