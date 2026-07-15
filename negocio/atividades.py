"""Registro simples de atividades recentes do sistema, em memoria.

O banco de dados nao guarda uma coluna de "ultima atualizacao" para as
tabelas do sistema, entao listar "os ultimos registros" a partir do banco
(por ID ou por ordem alfabetica) nao reflete de verdade "o que aconteceu
por ultimo" -- por exemplo, editar um album antigo nao mudaria sua posicao
numa lista ordenada por ID.

Este modulo resolve isso mantendo, em memoria, uma pilha das ultimas acoes
realizadas na aplicacao (cadastros, atualizacoes, vendas, etc.), sempre com
a mais recente aparecendo primeiro -- independente de ID ou ordem alfabetica.
"""

from collections import deque
from datetime import datetime

_MAXIMO_ATIVIDADES = 30
_atividades = deque(maxlen=_MAXIMO_ATIVIDADES)


def registrar_atividade(mensagem: str) -> None:
    """Adiciona uma nova atividade no topo do historico."""
    momento = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    _atividades.appendleft(f"[{momento}] {mensagem}")


def obter_atividades(quantidade: int = 5) -> list[str]:
    """Retorna as atividades mais recentes primeiro, no maximo 'quantidade'."""
    return list(_atividades)[:quantidade]
