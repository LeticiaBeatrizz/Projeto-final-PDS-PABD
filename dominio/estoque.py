from dataclasses import dataclass
from typing import Optional


@dataclass
class Estoque:
    id: Optional[int]
    album_id: int
    vendido: bool = False