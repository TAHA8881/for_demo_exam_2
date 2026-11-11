from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Product:
    product_id: int
    name: str
    category: str
    manufacturer: str
    content: str
    image: str | None
    price: Decimal
    quantity: int