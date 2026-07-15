from typing import Optional

from dados.item_venda_repository import ItemVendaRepository
from dominio.item_venda import ItemVenda


class ItemVendaService:
    """Camada de negócio: aplica validações e regras simples."""

    def __init__(self, repositorio: ItemVendaRepository) -> None:
        self.repositorio = repositorio

    def adicionar_item_venda(self, venda_id: int, item_id: int) -> ItemVenda:
        if venda_id <= 0:
            raise ValueError("O ID da venda deve ser um numero inteiro positivo.")

        if item_id <= 0:
            raise ValueError("O ID do item deve ser um numero inteiro positivo.")

        item_venda = ItemVenda(id=None, venda_id=venda_id, item_id=item_id)
        novo_id = self.repositorio.adicionar(item_venda)
        item_venda.id = novo_id
        return item_venda

    def listar_itens_venda(self) -> list[ItemVenda]:
        return self.repositorio.listar_todos()

    def buscar_item_venda_por_id(self, id_item_venda: int) -> Optional[ItemVenda]:
        if id_item_venda <= 0:
            raise ValueError("O ID deve ser um numero inteiro positivo.")
        return self.repositorio.buscar_por_id(id_item_venda)

    def atualizar_item_venda(self, id_item_venda: int, venda_id: int, item_id: int) -> bool:
        if id_item_venda <= 0:
            raise ValueError("O ID deve ser um numero inteiro positivo.")

        if venda_id <= 0:
            raise ValueError("O ID da venda deve ser um numero inteiro positivo.")

        if item_id <= 0:
            raise ValueError("O ID do item deve ser um numero inteiro positivo.")

        item_venda = ItemVenda(id=id_item_venda, venda_id=venda_id, item_id=item_id)
        return self.repositorio.atualizar(item_venda)

    def remover_item_venda(self, id_item_venda: int) -> bool:
        if id_item_venda <= 0:
            raise ValueError("O ID deve ser um numero inteiro positivo.")
        return self.repositorio.remover(id_item_venda)
