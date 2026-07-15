from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

@dataclass
class Album:
    id: Optional[int]
    nome: str
    genero: str
    artista: str
    tamanho: int = 1
    preco: Decimal = Decimal('0.00')