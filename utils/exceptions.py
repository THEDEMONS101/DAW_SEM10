"""Excepciones de dominio para el Sistema de Gestión de Productos."""


class ValidationError(Exception):
    """Error de validación de datos de entrada."""


class NotFoundError(Exception):
    """Error cuando un recurso no existe en el inventario."""