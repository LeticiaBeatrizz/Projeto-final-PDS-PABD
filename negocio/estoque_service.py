from typing import Optional

from dados.estoque_repository import EstoqueRepository
from dominio.estoque import Estoque


class EstoqueService:
    """Camada de negócio: aplica validações e regras simples."""

    def __init__(self, repositorio: EstoqueRepository) -> None:
        self.repositorio = repositorio

    def adicionar_estoque(self, album_id: int, vendido: bool = False) -> Estoque:
        if album_id <= 0:
            raise ValueError("O ID do album deve ser um numero inteiro positivo.")

        estoque = Estoque(id=None, album_id=album_id, vendido=vendido)
        novo_id = self.repositorio.adicionar(estoque)
        estoque.id = novo_id
        return estoque

    def listar_estoque(self) -> list[Estoque]:
        return self.repositorio.listar_todos()

    def buscar_estoque_por_id(self, id_estoque: int) -> Optional[Estoque]:
        if id_estoque <= 0:
            raise ValueError("O ID deve ser um numero inteiro positivo.")
        return self.repositorio.buscar_por_id(id_estoque)

    def atualizar_estoque(self, id_estoque: int, album_id: int, vendido: bool) -> bool:
        if id_estoque <= 0:
            raise ValueError("O ID deve ser um numero inteiro positivo.")

        if album_id <= 0:
            raise ValueError("O ID do album deve ser um numero inteiro positivo.")

        estoque = Estoque(id=id_estoque, album_id=album_id, vendido=vendido)
        return self.repositorio.atualizar(estoque)

    def adicionar_multiplos(self, album_id: int, quantidade: int) -> int:
        """Cadastra 'quantidade' unidades novas em estoque para o mesmo album."""
        if album_id <= 0:
            raise ValueError("O ID do album deve ser um numero inteiro positivo.")
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")

        for _ in range(quantidade):
            self.adicionar_estoque(album_id)
        return quantidade

    def remover_multiplos(self, album_id: int, quantidade: int) -> int:
        """Remove 'quantidade' unidades ainda disponiveis (nao vendidas) do estoque do album."""
        if album_id <= 0:
            raise ValueError("O ID do album deve ser um numero inteiro positivo.")
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")

        ids_disponiveis = self.repositorio.listar_disponiveis_por_album(album_id, quantidade)
        if len(ids_disponiveis) < quantidade:
            raise ValueError(
                f"Estoque insuficiente: ha apenas {len(ids_disponiveis)} unidade(s) disponivel(is) para remover."
            )

        for id_estoque in ids_disponiveis:
            self.repositorio.remover(id_estoque)
        return quantidade

    def contar_disponivel(self, album_id: int) -> int:
        if album_id <= 0:
            raise ValueError("O ID do album deve ser um numero inteiro positivo.")
        return self.repositorio.contar_disponivel_por_album(album_id)

    def buscar_disponivel_para_venda(self, album_id: int) -> Optional[int]:
        if album_id <= 0:
            raise ValueError("O ID do album deve ser um numero inteiro positivo.")
        return self.repositorio.buscar_disponivel_por_album(album_id)

    def marcar_como_vendido(self, id_estoque: int) -> bool:
        estoque = self.buscar_estoque_por_id(id_estoque)
        if estoque is None:
            raise ValueError("Estoque nao encontrado para o ID informado.")

        estoque.vendido = True
        return self.repositorio.atualizar(estoque)

    def remover_estoque(self, id_estoque: int) -> bool:
        if id_estoque <= 0:
            raise ValueError("O ID deve ser um numero inteiro positivo.")

        estoque = self.repositorio.buscar_por_id(id_estoque)
        if estoque is None:
            raise ValueError("Item de estoque nao encontrado para o ID informado.")

        if estoque.vendido:
            raise ValueError("Não é possível remover um item de estoque que já foi vendido.")

        return self.repositorio.remover(id_estoque)
