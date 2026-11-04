"""Utilidades de presentación para la consola (ANSI, sin dependencias)."""

import os
import sys

# Habilita colores ANSI en Windows 10+
if os.name == "nt":
    os.system("")  # activa el procesamiento de secuencias ANSI en cmd/PowerShell

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"
GRAY = "\033[90m"


def habilitar_ansi() -> None:
    """Fuerza UTF-8 en stdout (evita problemas con ✔ ✖ en Windows)."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:  # pylint: disable=broad-exception-caught
        pass


def titulo(texto: str) -> str:
    """Devuelve un título enmarcado con color."""
    linea = "═" * (len(texto) + 4)
    return f"{CYAN}{BOLD}╔{linea}╗\n║  {texto}  ║\n╚{linea}╝{RESET}"


def opcion(num: str, texto: str) -> str:
    """Formatea una opción del menú."""
    return f"  {YELLOW}{BOLD}[{num}]{RESET} {texto}"


def ok(texto: str) -> str:
    """Mensaje de éxito."""
    return f"{GREEN}✔ {texto}{RESET}"


def error(texto: str) -> str:
    """Mensaje de error."""
    return f"{RED}✖ {texto}{RESET}"


def info(texto: str) -> str:
    """Mensaje informativo."""
    return f"{BLUE}ℹ {texto}{RESET}"


def etiqueta(texto: str) -> str:
    """Etiqueta de campo para input()."""
    return f"{MAGENTA}{BOLD}{texto}{RESET}"


def separador() -> str:
    """Línea separadora."""
    return f"{GRAY}{'─' * 50}{RESET}"
