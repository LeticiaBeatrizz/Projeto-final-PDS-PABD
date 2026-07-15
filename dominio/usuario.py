from dataclasses import dataclass
from typing import Optional, Literal

@dataclass
class Usuario:
    id: Optional[int]
    login: str
    senha: str
    nome_completo: str