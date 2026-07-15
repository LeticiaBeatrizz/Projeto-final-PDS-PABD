from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from dados.modelos import ItemVendaModel, EstoqueModel, AlbumModel
from dominio.item_venda import ItemVenda


class ItemVendaRepository:
    """Camada data: faz o acesso ao banco usando SQLAlchemy ORM."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def adicionar(self, item_venda: ItemVenda) -> int:
        item_venda_model = ItemVendaModel(
            venda_id=item_venda.venda_id,
            item_id=item_venda.item_id,
        )
        try:
            self.session.add(item_venda_model)
            self.session.commit()
            self.session.refresh(item_venda_model)
            return item_venda_model.id
        except Exception:
            self.session.rollback()
            raise

    def adicionar_sem_commit(self, item_venda: ItemVenda) -> int:
        """Igual a adicionar, mas usa flush em vez de commit (ver
        VendaRepository.adicionar_sem_commit)."""
        item_venda_model = ItemVendaModel(
            venda_id=item_venda.venda_id,
            item_id=item_venda.item_id,
        )
        self.session.add(item_venda_model)
        self.session.flush()
        return item_venda_model.id

    def listar_todos(self) -> list[ItemVenda]:
        resultado = self.session.execute(
            select(ItemVendaModel).order_by(ItemVendaModel.id)
        )
        itens_model = resultado.scalars().all()
        return [self._converter_para_entidade(item_model) for item_model in itens_model]

    def buscar_por_id(self, id_item_venda: int) -> Optional[ItemVenda]:
        item_venda_model = self.session.get(ItemVendaModel, id_item_venda)
        if item_venda_model is None:
            return None
        return self._converter_para_entidade(item_venda_model)

    def atualizar(self, item_venda: ItemVenda) -> bool:
        item_venda_model = self.session.get(ItemVendaModel, item_venda.id)
        if item_venda_model is None:
            return False

        item_venda_model.venda_id = item_venda.venda_id
        item_venda_model.item_id = item_venda.item_id
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return True

    def remover(self, id_item_venda: int) -> bool:
        item_venda_model = self.session.get(ItemVendaModel, id_item_venda)
        if item_venda_model is None:
            return False

        try:
            self.session.delete(item_venda_model)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return True

    def buscar_nomes_albuns_por_venda(self, venda_id: int) -> list[str]:
        """Retorna o nome de cada album vendido numa venda (na ordem em que
        foram adicionados), para exibicao na listagem de vendas."""
        resultado = self.session.execute(
            select(AlbumModel.nome)
            .select_from(ItemVendaModel)
            .join(EstoqueModel, EstoqueModel.id == ItemVendaModel.item_id)
            .join(AlbumModel, AlbumModel.id == EstoqueModel.album_id)
            .where(ItemVendaModel.venda_id == venda_id)
            .order_by(ItemVendaModel.id)
        )
        return [nome for (nome,) in resultado]

    @staticmethod
    def _converter_para_entidade(item_venda_model: ItemVendaModel) -> ItemVenda:
        return ItemVenda(
            id=item_venda_model.id,
            venda_id=item_venda_model.venda_id,
            item_id=item_venda_model.item_id,
        )
