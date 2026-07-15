from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from dados.modelos import UsuarioModel
from dominio.usuario import Usuario


class UsuarioRepository:
    """Camada data: faz o acesso ao banco usando SQLAlchemy ORM."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def adicionar(self, usuario: Usuario) -> int:
        usuario_model = UsuarioModel(
            nome_completo=usuario.nome_completo,
            login=usuario.login,
            senha=usuario.senha,
        )
        try:
            self.session.add(usuario_model)
            self.session.commit()
            self.session.refresh(usuario_model)
            return usuario_model.id
        except Exception:
            self.session.rollback()
            raise

    def listar_todos(self) -> list[Usuario]:
        resultado = self.session.execute(select(UsuarioModel).order_by(UsuarioModel.id))
        usuarios_model = resultado.scalars().all()
        return [self._converter_para_entidade(usuario_model) for usuario_model in usuarios_model]

    def buscar_por_id(self, id_usuario: int) -> Optional[Usuario]:
        usuario_model = self.session.get(UsuarioModel, id_usuario)
        if usuario_model is None:
            return None
        return self._converter_para_entidade(usuario_model)

    def buscar_por_login(self, login: str) -> Optional[Usuario]:
        usuario_model = self.session.execute(
            select(UsuarioModel).where(UsuarioModel.login == login)
        ).scalar_one_or_none()
        if usuario_model is None:
            return None
        return self._converter_para_entidade(usuario_model)

    def buscar_por_texto(self, texto: str) -> list[Usuario]:
        termo = f"%{texto}%" if texto else "%"
        resultado = self.session.execute(
            select(UsuarioModel)
            .where(
                UsuarioModel.nome_completo.like(termo) | UsuarioModel.login.like(termo)
            )
            .order_by(UsuarioModel.nome_completo)
        )
        usuarios_model = resultado.scalars().all()
        return [self._converter_para_entidade(usuario_model) for usuario_model in usuarios_model]

    def atualizar(self, usuario: Usuario) -> bool:
        usuario_model = self.session.get(UsuarioModel, usuario.id)
        if usuario_model is None:
            return False

        usuario_model.nome_completo = usuario.nome_completo
        usuario_model.login = usuario.login
        usuario_model.senha = usuario.senha
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return True

    def remover(self, id_usuario: int) -> bool:
        usuario_model = self.session.get(UsuarioModel, id_usuario)
        if usuario_model is None:
            return False

        try:
            self.session.delete(usuario_model)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return True

    @staticmethod
    def _converter_para_entidade(usuario_model: UsuarioModel) -> Usuario:
        return Usuario(
            id=usuario_model.id,
            login=usuario_model.login,
            senha=usuario_model.senha,
            nome_completo=usuario_model.nome_completo,
        )
