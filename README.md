# TiendaPy

Aplicación de consola en Python para controlar el inventario y las ventas de una tienda de barrio
(caso de estudio: Tienda "Don Aurelio"). Proyecto final del curso **Python 0 a 100 – ACM**.

## ¿Qué hace?

- **M1 Inventario:** registrar, consultar (por código o categoría), modificar precio/stock y eliminar productos.
- **M2 Ventas:** carrito con varios productos, descuento automático (5 % desde $50.000 y 10 % desde $100.000), pago y cambio.
- **M3 Alertas:** productos con stock menor o igual al mínimo, agrupados por proveedor (los agotados se marcan como AGOTADO).
- **M4 Reportes:** cierre del día (total vendido, número de ventas, ticket promedio, producto más vendido, productos sin ventas y categorías con movimiento).
- **M5 Persistencia:** el inventario se guarda en `data/inventario.txt` y las ventas en `data/ventas.txt`.
- **M6 Menú principal:** se repite hasta que el usuario elige salir.

## Instalación y ejecución

```bash
# 1. Crear y activar el entorno virtual
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux / Mac

# 2. Instalar la dependencia
pip install -r requirements.txt

# 3. Ejecutar (desde la carpeta tiendapy/)
python src/main.py
```

## Estructura

```
tiendapy/
|-- README.md
|-- requirements.txt
|-- data/
|   |-- inventario.txt
|   `-- ventas.txt
`-- src/
    |-- main.py            # menú principal y flujo general
    |-- inventario.py      # CRUD de productos
    |-- ventas.py          # carrito, descuentos y cambio
    |-- reportes.py        # alertas y cierre del día
    |-- persistencia.py    # lectura y escritura de archivos
    `-- validaciones.py    # captura segura de datos
```

## Decisiones de diseño

- **Sin clases:** cada producto es un diccionario y el inventario es un diccionario `{codigo: producto}`;
  así la búsqueda por código es directa y el código es sencillo de leer.
- **Dependencia externa:** `tabulate`, para mostrar tablas ordenadas en consola.
- **Reglas de negocio con `raise`:** las violaciones (código repetido, stock insuficiente, pago insuficiente)
  lanzan `ValueError` y se capturan con `try/except`.
- **Archivos con `with`:** se cierran solos aunque ocurra un error.

## Formato de los archivos

`data/inventario.txt` (un producto por línea):

```
codigo|nombre|categoria|precio|stock|stock_minimo|proveedor
LAC001|Leche entera 1L|Lacteos|4200.0|35|10|Alqueria
```

`data/ventas.txt` (una venta por línea):

```
fecha|total|codigo:cantidad;codigo:cantidad
2026-11-04|18400.0|LAC001:2;BEB003:1
```

## Integrantes

- (escribe aquí los nombres del grupo)
