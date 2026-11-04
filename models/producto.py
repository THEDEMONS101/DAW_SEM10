"""Jerarquía de clases Producto, Electronico y Libro."""

from __future__ import annotations

from abc import ABC, abstractmethod

from utils.exceptions import ValidationError


class DescuentoMixin:  # pylint: disable=too-few-public-methods
    """Mixin opcional: aplica descuentos por porcentaje sobre un monto."""

    def aplicar_descuento(self, monto: float, porcentaje: float) -> float:
        """Devuelve el monto con el porcentaje de descuento aplicado."""
        if not 0 <= porcentaje <= 100:
            raise ValidationError(f"Porcentaje de descuento inválido: {porcentaje}")
        return monto * (1 - porcentaje / 100)


class Producto(ABC):
    """Clase base abstracta de productos."""

    IGV = 0.18  # constante de clase

    def __init__(self, nombre: str, precio_base: float, stock: int):
        # Usamos setters con @property => encapsulamiento + validación
        self.nombre = nombre
        self.precio_base = precio_base
        self.stock = stock

    # ---------- nombre ----------
    @property
    def nombre(self) -> str:
        """Nombre del producto."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        limpio = (valor or "").strip()
        if not limpio:
            raise ValidationError("El nombre no puede estar vacío")
        self._nombre = limpio

    # ---------- precio_base ----------
    @property
    def precio_base(self) -> float:
        """Precio base sin impuestos ni descuentos."""
        return self._precio_base

    @precio_base.setter
    def precio_base(self, valor: float) -> None:
        try:
            num = float(valor)
        except (TypeError, ValueError) as exc:
            raise ValidationError(f"Precio inválido: {valor!r}") from exc
        if num <= 0:
            raise ValidationError(f"El precio debe ser > 0: {num}")
        self._precio_base = num

    # ---------- stock ----------
    @property
    def stock(self) -> int:
        """Unidades disponibles en inventario."""
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        try:
            num = int(valor)
        except (TypeError, ValueError) as exc:
            raise ValidationError(f"Stock inválido: {valor!r}") from exc
        if num < 0:
            raise ValidationError(f"El stock no puede ser negativo: {num}")
        self._stock = num

    # ---------- contrato polimórfico ----------
    @abstractmethod
    def calcular_precio_final(self) -> float:
        """Cada subclase define su cálculo de precio final."""
        raise NotImplementedError

    def __str__(self) -> str:
        return (
            f"[{self.__class__.__name__}] {self.nombre} | "
            f"Base: S/ {self.precio_base:.2f} | Stock: {self.stock}"
        )

    def __del__(self):
        print(f"  [__del__] Destruyendo instancia: {self.nombre}")


class Electronico(Producto, DescuentoMixin):
    """Producto electrónico: aplica IGV + descuento si stock > 50."""

    def __init__(
        self,
        nombre: str,
        precio_base: float,
        stock: int,
        garantia_meses: int,
    ):
        super().__init__(nombre, precio_base, stock)
        self._garantia_meses = 0
        self.garantia_meses = garantia_meses  # pasa por el setter

    @property
    def garantia_meses(self) -> int:
        """Meses de garantía del producto."""
        return self._garantia_meses

    @garantia_meses.setter
    def garantia_meses(self, valor: int) -> None:
        try:
            num = int(valor)
        except (TypeError, ValueError) as exc:
            raise ValidationError(f"Garantía inválida: {valor!r}") from exc
        if not 0 <= num <= 60:
            raise ValidationError(f"Garantía fuera de rango 0-60 meses: {num}")
        self._garantia_meses = num

    def calcular_precio_final(self) -> float:
        precio = self.precio_base * (1 + self.IGV)
        if self.stock > 50:
            precio = self.aplicar_descuento(precio, 10)  # 10 % por stock alto
        return round(precio, 2)

    def __str__(self) -> str:
        return f"{super().__str__()} | Garantía: {self.garantia_meses} meses"


class Libro(Producto, DescuentoMixin):
    """Libro: 10 % de descuento si es libro de texto."""

    def __init__(
        self,
        nombre: str,
        precio_base: float,
        stock: int,
        autor: str,
        es_texto: bool = False,
    ):
        super().__init__(nombre, precio_base, stock)
        self._autor = ""
        self.autor = autor
        self._es_texto = bool(es_texto)

    @property
    def autor(self) -> str:
        """Autor del libro."""
        return self._autor

    @autor.setter
    def autor(self, valor: str) -> None:
        limpio = (valor or "").strip()
        if not limpio:
            raise ValidationError("El autor no puede estar vacío")
        self._autor = limpio

    @property
    def es_texto(self) -> bool:
        """Indica si es un libro de texto (aplica descuento)."""
        return self._es_texto

    def calcular_precio_final(self) -> float:
        precio = self.precio_base
        if self.es_texto:
            precio = self.aplicar_descuento(precio, 10)
        return round(precio, 2)

    def __str__(self) -> str:
        tipo = "Texto" if self.es_texto else "General"
        return f"{super().__str__()} | Autor: {self.autor} | Tipo: {tipo}"
