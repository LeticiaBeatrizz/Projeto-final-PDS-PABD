from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from dados.modelos import EstoqueModel
from dominio.estoque import Estoque


class EstoqueRepository:
    """Camada data: faz o acesso ao banco usando SQLAlchemy ORM."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def adicionar(self, estoque: Estoque) -> int:
        estoque_model = EstoqueModel(album_id=estoque.album_id, vendido=estoque.vendido)
        try:
            self.session.add(estoque_model)
            self.session.commit()
            self.session.refresh(estoque_model)
            return estoque_model.id
        except Exception:
            self.session.rollback()
            raise

    def listar_todos(self) -> list[Estoque]:
        resultado = self.session.execute(select(EstoqueModel).order_by(EstoqueModel.id))
        estoques_model = resultado.scalars().all()
        return [self._converter_para_entidade(estoque_model) for estoque_model in estoques_model]

    def buscar_por_id(self, id_estoque: int) -> Optional[Estoque]:
        estoque_model = self.session.get(EstoqueModel, id_estoque)
        if estoque_model is None:
            return None
        return self._converter_para_entidade(estoque_model)

    def atualizar(self, estoque: Estoque) -> bool:
        estoque_model = self.session.get(EstoqueModel, estoque.id)
        if estoque_model is None:
            return False

        estoque_model.album_id = estoque.album_id
        estoque_model.vendido = estoque.vendido
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return True

    def remover(self, id_estoque: int) -> bool:
        estoque_model = self.session.get(EstoqueModel, id_estoque)
        if estoque_model is None:
            return False

        try:
            self.session.delete(estoque_model)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return True

    def marcar_vendido_sem_commit(self, id_estoque: int) -> None:
        """Marca a unidade de estoque como vendida usando flush em vez de
        commit (ver VendaRepository.adicionar_sem_commit)."""
        estoque_model = self.session.get(EstoqueModel, id_estoque)
        if estoque_model is None:
            raise ValueError("Item de estoque nao encontrado para o ID informado.")
        estoque_model.vendido = True
        self.session.flush()

    def contar_disponivel_por_album(self, album_id: int) -> int:
        """Quantidade de unidades ainda nao vendidas de um album."""
        total = self.session.execute(
            select(func.count(EstoqueModel.id)).where(
                EstoqueModel.album_id == album_id,
                EstoqueModel.vendido.is_(False),
            )
        ).scalar_one()
        return int(total)

    def listar_disponiveis_por_album(self, album_id: int, limite: int) -> list[int]:
        """Retorna ate 'limite' IDs de unidades em estoque ainda nao vendidas do album."""
        resultado = self.session.execute(
            select(EstoqueModel.id)
            .where(EstoqueModel.album_id == album_id, EstoqueModel.vendido.is_(False))
            .limit(limite)
        )
        return [int(id_estoque) for id_estoque in resultado.scalars().all()]

    def buscar_disponivel_por_album(self, album_id: int) -> Optional[int]:
        """Retorna o ID de uma unidade em estoque ainda nao vendida do album, se houver."""
        id_estoque = self.session.execute(
            select(EstoqueModel.id)
            .where(EstoqueModel.album_id == album_id, EstoqueModel.vendido.is_(False))
            .limit(1)
        ).scalar_one_or_none()
        return int(id_estoque) if id_estoque is not None else None

    @staticmethod
    def _converter_para_entidade(estoque_model: EstoqueModel) -> Estoque:
        return Estoque(
            id=estoque_model.id,
            album_id=estoque_model.album_id,
            vendido=bool(estoque_model.vendido),
        )
