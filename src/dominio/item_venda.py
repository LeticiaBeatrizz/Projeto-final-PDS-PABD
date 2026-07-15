from dataclasses import dataclass
from typing import Optional


@dataclass
class ItemVenda:
    id: Optional[int]
    venda_id: int
    item_id: int