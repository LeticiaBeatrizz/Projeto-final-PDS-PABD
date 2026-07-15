from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from dados.modelos import VendaModel, UsuarioModel
from dominio.venda import Venda


class VendaRepository:
    """Camada data: faz o acesso ao banco usando SQLAlchemy ORM."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def adicionar(self, venda: Venda) -> int:
        venda_model = VendaModel(
            vendedor_id=venda.vendedor_id,
            data=venda.data,
            cpf_cliente=venda.cpf_cliente,
        )
        try:
            self.session.add(venda_model)
            self.session.commit()
            self.session.refresh(venda_model)
            return venda_model.id
        except Exception:
            self.session.rollback()
            raise

    def adicionar_sem_commit(self, venda: Venda) -> int:
        """Igual a adicionar, mas usa flush em vez de commit: o registro fica
        visivel dentro da mesma transacao (com ID gerado), sem persistir no
        banco ainda. Usado por VendaService.registrar_venda_completa para
        inserir venda + itens em uma unica transacao atomica."""
        venda_model = VendaModel(
            vendedor_id=venda.vendedor_id,
            data=venda.data,
            cpf_cliente=venda.cpf_cliente,
        )
        self.session.add(venda_model)
        self.session.flush()
        return venda_model.id

    def listar_todos(self) -> list[Venda]:
        resultado = self.session.execute(
            select(VendaModel, UsuarioModel.nome_completo)
            .outerjoin(UsuarioModel, UsuarioModel.id == VendaModel.vendedor_id)
            .order_by(VendaModel.id)
        )
        return [
            self._converter_para_entidade(venda_model, vendedor_nome)
            for venda_model, vendedor_nome in resultado
        ]

    def buscar_por_texto(self, texto: str) -> list[Venda]:
        """Busca vendas pelo CPF do cliente ou pelo nome/login do vendedor."""
        termo = f"%{texto}%" if texto else "%"
        resultado = self.session.execute(
            select(VendaModel, UsuarioModel.nome_completo)
            .outerjoin(UsuarioModel, UsuarioModel.id == VendaModel.vendedor_id)
            .where(
                VendaModel.cpf_cliente.like(termo)
                | UsuarioModel.nome_completo.like(termo)
                | UsuarioModel.login.like(termo)
            )
            .order_by(VendaModel.id)
        )
        return [
            self._converter_para_entidade(venda_model, vendedor_nome)
            for venda_model, vendedor_nome in resultado
        ]

    def buscar_por_id(self, id_venda: int) -> Optional[Venda]:
        resultado = self.session.execute(
            select(VendaModel, UsuarioModel.nome_completo)
            .outerjoin(UsuarioModel, UsuarioModel.id == VendaModel.vendedor_id)
            .where(VendaModel.id == id_venda)
        ).first()
        if resultado is None:
            return None
        venda_model, vendedor_nome = resultado
        return self._converter_para_entidade(venda_model, vendedor_nome)

    def atualizar(self, venda: Venda) -> bool:
        venda_model = self.session.get(VendaModel, venda.id)
        if venda_model is None:
            return False

        venda_model.vendedor_id = venda.vendedor_id
        venda_model.data = venda.data
        venda_model.cpf_cliente = venda.cpf_cliente
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return True

    def existe_venda_para_vendedor(self, vendedor_id: int) -> bool:
        """Verifica se o vendedor (usuario) possui alguma venda registrada.
        Usado para bloquear a remocao de usuarios com vendas no historico."""
        resultado = self.session.execute(
            select(VendaModel.id).where(VendaModel.vendedor_id == vendedor_id).limit(1)
        ).first()
        return resultado is not None

    def remover(self, id_venda: int) -> bool:
        venda_model = self.session.get(VendaModel, id_venda)
        if venda_model is None:
            return False

        try:
            self.session.delete(venda_model)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return True

    @staticmethod
    def _converter_para_entidade(venda_model: VendaModel, vendedor_nome: Optional[str]) -> Venda:
        return Venda(
            id=venda_model.id,
            vendedor_id=venda_model.vendedor_id,
            data=venda_model.data,
            cpf_cliente=venda_model.cpf_cliente,
            vendedor_nome=vendedor_nome,
        )
