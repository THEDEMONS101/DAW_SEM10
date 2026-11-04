# Sistema de Gestión de Productos (CLI)

Práctica Grupal Semana 10 — IS093A (UNCP). Autor: <CAMARGO ALVARADO EDILSON ROBERTO>.

## Diagrama de clases

```mermaid
classDiagram
    class Producto {
        <<abstract>>
        +str nombre
        +float precio_base
        +int stock
        +IGV = 0.18
        +calcular_precio_final()* float
        +__str__() str
    }
    class DescuentoMixin {
        +aplicar_descuento(monto, pct) float
    }
    class Electronico {
        -int _garantia_meses
        +calcular_precio_final() float
    }
    class Libro {
        -str _autor
        -bool _es_texto
        +calcular_precio_final() float
    }
    Producto <|-- Electronico
    Producto <|-- Libro
    DescuentoMixin <|-- Electronico
    DescuentoMixin <|-- Libro