from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Venda:
    id: Optional[int]
    vendedor_id: int
    data: Optional[datetime] = None
    cpf_cliente: Optional[str] = None
    vendedor_nome: Optional[str] = None