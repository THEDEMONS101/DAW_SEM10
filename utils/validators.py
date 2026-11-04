"""Funciones de validación y sanitización de entrada."""

from .exceptions import ValidationError


def validar_numero(
    valor: str,
    tipo: type = float,
    min_val: float = 0,
    max_val: float | None = None,
) -> float:
    """Convierte y valida un número dentro de un rango."""
    try:
        num = tipo(valor)
    except (ValueError, TypeError) as exc:
        raise ValidationError(f"Formato numérico inválido: {valor!r}") from exc

    if num < min_val or (max_val is not None and num > max_val):
        rango = f"{min_val}-{max_val}" if max_val is not None else f">= {min_val}"
        raise ValidationError(f"Valor fuera de rango ({rango}): {num}")
    return num


def validar_texto(valor: str, campo: str = "texto", min_len: int = 1) -> str:
    """Sanitiza un texto: strip y valida longitud mínima."""
    limpio = (valor or "").strip()
    if len(limpio) < min_len:
        raise ValidationError(f"El campo '{campo}' no puede estar vacío")
    return limpio


def validar_categoria(categoria: str) -> str:
    """Valida y normaliza la categoría del producto."""
    validas = {"electronico", "libro"}
    normalizada = (categoria or "").strip().lower()
    if normalizada not in validas:
        raise ValidationError(
            f"Categoría inválida: {categoria!r}. Válidas: {sorted(validas)}"
        )
    return normalizada


def formatear_precio(valor: float) -> str:
    """Formatea un precio con símbolo de moneda."""
    return f"S/ {valor:,.2f}"