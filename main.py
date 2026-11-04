#!/usr/bin/env python3
"""Orquestador CLI - Sistema de Gestión de Productos (IS093A Semana 10)."""

from models import Electronico, Libro, Producto
from utils import (
    NotFoundError,
    ValidationError,
    formatear_precio,
    validar_categoria,
    validar_numero,
    validar_texto,
)
from utils.ui import (
    error,
    etiqueta,
    habilitar_ansi,
    info,
    ok,
    opcion,
    separador,
    titulo,
)


def menu() -> str:
    """Muestra el menú principal y devuelve la opción elegida."""
    print()
    print(titulo("GESTIÓN DE PRODUCTOS (CLI)"))
    print(opcion("1", "Agregar producto"))
    print(opcion("2", "Listar productos"))
    print(opcion("3", "Calcular precio final"))
    print(opcion("4", "Salir"))
    return input(etiqueta("Opción > ")).strip()


def pedir_datos_producto() -> Producto:
    """Pide datos por consola y construye el producto correspondiente."""
    categoria = validar_categoria(input(etiqueta("Categoría (electronico/libro) > ")))
    nombre = validar_texto(input(etiqueta("Nombre > ")), campo="nombre")
    precio = validar_numero(input(etiqueta("Precio base > ")), float, min_val=0.01)
    stock = validar_numero(input(etiqueta("Stock > ")), int, min_val=0, max_val=10000)

    if categoria == "electronico":
        garantia = validar_numero(
            input(etiqueta("Garantía (meses) > ")),
            int,
            min_val=0,
            max_val=60,
        )
        return Electronico(nombre, precio, stock, garantia)

    autor = validar_texto(input(etiqueta("Autor > ")), campo="autor")
    es_texto = input(etiqueta("¿Es libro de texto? (s/n) > ")).strip().lower() == "s"
    return Libro(nombre, precio, stock, autor, es_texto)


def agregar_producto(inventario: dict[int, Producto], contador_id: int) -> int:
    """Agrega un producto al inventario y devuelve el siguiente ID libre."""
    producto = pedir_datos_producto()
    inventario[contador_id] = producto
    print(ok(f"Producto agregado con ID {contador_id}."))
    return contador_id + 1


def listar_productos(inventario: dict[int, Producto]) -> None:
    """Lista todos los productos del inventario."""
    print()
    print(titulo("INVENTARIO"))
    if not inventario:
        print(info("No hay productos registrados."))
        return
    for pid, prod in inventario.items():
        print(separador())
        print(f"  {etiqueta(f'ID {pid}:')} {prod}")
        print(
            f"       {info('Precio final')}: "
            f"{formatear_precio(prod.calcular_precio_final())}"
        )
    print(separador())


def calcular_precio(inventario: dict[int, Producto]) -> None:
    """Calcula y muestra el precio final de un producto por ID."""
    if not inventario:
        raise NotFoundError("El inventario está vacío")
    pid = validar_numero(input(etiqueta("ID del producto > ")), int, min_val=1)
    if pid not in inventario:
        raise NotFoundError(f"No existe producto con ID {pid}")
    prod = inventario[pid]
    print(
        f"{ok(prod.nombre)} → precio final: "
        f"{formatear_precio(prod.calcular_precio_final())}"
    )


def main() -> None:
    """Punto de entrada del CLI."""
    habilitar_ansi()
    inventario: dict[int, Producto] = {}
    contador_id = 1

    while True:
        try:
            opcion_elegida = menu()
            if opcion_elegida == "1":
                contador_id = agregar_producto(inventario, contador_id)
            elif opcion_elegida == "2":
                listar_productos(inventario)
            elif opcion_elegida == "3":
                calcular_precio(inventario)
            elif opcion_elegida == "4":
                print(ok("Cerrando sistema..."))
                break
            else:
                raise ValidationError(f"Opción inválida: {opcion_elegida!r}")
        except ValidationError as exc:
            print(error(f"Error de validación: {exc}"))
        except NotFoundError as exc:
            print(error(f"No encontrado: {exc}"))
        except KeyboardInterrupt:
            print(info("Interrumpido por el usuario. Saliendo..."))
            break
        except Exception as exc:  # pylint: disable=broad-exception-caught
            print(error(f"Error inesperado: {exc}"))
        else:
            # Se ejecuta solo si no hubo excepción (ruta feliz)
            pass
        finally:
            # Limpieza / log: aquí podrías vaciar buffers o cerrar recursos
            pass


if __name__ == "__main__":
    main()
