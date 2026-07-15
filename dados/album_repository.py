from typing import Optional

from sqlalchemy import and_, case, func, select
from sqlalchemy.orm import Session

from dados.modelos import AlbumModel, EstoqueModel
from dominio.album import Album


class AlbumRepository:
    """Camada data: faz o acesso ao banco usando SQLAlchemy ORM."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def adicionar(self, album: Album) -> int:
        album_model = AlbumModel(
            nome=album.nome,
            tamanho=album.tamanho,
            genero=album.genero,
            artista=album.artista,
            preco=album.preco,
        )
        try:
            self.session.add(album_model)
            self.session.commit()
            self.session.refresh(album_model)
            return album_model.id
        except Exception:
            self.session.rollback()
            raise

    def listar_todos(self) -> list[Album]:
        resultado = self.session.execute(select(AlbumModel).order_by(AlbumModel.id))
        albuns_model = resultado.scalars().all()
        return [self._converter_para_entidade(album_model) for album_model in albuns_model]

    def buscar_por_id(self, id_album: int) -> Optional[Album]:
        album_model = self.session.get(AlbumModel, id_album)
        if album_model is None:
            return None
        return self._converter_para_entidade(album_model)

    def buscar_por_nome(self, nome: str) -> list[Album]:
        termo = f"%{nome}%"
        resultado = self.session.execute(
            select(AlbumModel)
            .where(AlbumModel.nome.like(termo))
            .order_by(AlbumModel.id)
        )
        albuns_model = resultado.scalars().all()
        return [self._converter_para_entidade(album_model) for album_model in albuns_model]

    def buscar_por_texto(self, texto: str) -> list[dict]:
        """Busca albuns por nome ou genero, trazendo tambem a quantidade disponivel em estoque.

        Usado pela camada de apresentacao (tela de albuns e tela de vendas) para
        listar/buscar produtos. Retorna dicionarios (e nao objetos Album) porque a
        tela combina o dado do album com uma informacao calculada (estoque).
        """
        termo = f"%{texto}%" if texto else "%"
        quantidade_estoque = func.count(
            case((EstoqueModel.vendido.is_(False), 1))
        ).label("quantidade_estoque")

        resultado = self.session.execute(
            select(
                AlbumModel.id,
                AlbumModel.nome,
                AlbumModel.genero,
                AlbumModel.artista,
                AlbumModel.tamanho,
                AlbumModel.preco,
                quantidade_estoque,
            )
            .outerjoin(EstoqueModel, EstoqueModel.album_id == AlbumModel.id)
            .where(
                AlbumModel.nome.like(termo)
                | AlbumModel.genero.like(termo)
                | AlbumModel.artista.like(termo)
            )
            .group_by(
                AlbumModel.id,
                AlbumModel.nome,
                AlbumModel.genero,
                AlbumModel.artista,
                AlbumModel.tamanho,
                AlbumModel.preco,
            )
            .order_by(AlbumModel.nome)
        )
        return [self._converter_linha_para_dict(linha) for linha in resultado]

    def buscar_avancado(
        self,
        texto: str = "",
        tamanho_min: Optional[int] = None,
        tamanho_max: Optional[int] = None,
        preco_min: Optional[float] = None,
        preco_max: Optional[float] = None,
        estoque_min: Optional[int] = None,
        estoque_max: Optional[int] = None,
    ) -> list[dict]:
        """Igual a buscar_por_texto, mas permite filtrar por faixas de tamanho,
        preco e quantidade em estoque. Qualquer filtro nao informado (None) e
        ignorado.
        """
        termo = f"%{texto}%" if texto else "%"
        quantidade_estoque = func.count(
            case((EstoqueModel.vendido.is_(False), 1))
        ).label("quantidade_estoque")

        condicoes = [
            AlbumModel.nome.like(termo)
            | AlbumModel.genero.like(termo)
            | AlbumModel.artista.like(termo)
        ]
        if tamanho_min is not None:
            condicoes.append(AlbumModel.tamanho >= tamanho_min)
        if tamanho_max is not None:
            condicoes.append(AlbumModel.tamanho <= tamanho_max)
        if preco_min is not None:
            condicoes.append(AlbumModel.preco >= preco_min)
        if preco_max is not None:
            condicoes.append(AlbumModel.preco <= preco_max)

        consulta = (
            select(
                AlbumModel.id,
                AlbumModel.nome,
                AlbumModel.genero,
                AlbumModel.artista,
                AlbumModel.tamanho,
                AlbumModel.preco,
                quantidade_estoque,
            )
            .outerjoin(EstoqueModel, EstoqueModel.album_id == AlbumModel.id)
            .where(and_(*condicoes))
            .group_by(
                AlbumModel.id,
                AlbumModel.nome,
                AlbumModel.genero,
                AlbumModel.artista,
                AlbumModel.tamanho,
                AlbumModel.preco,
            )
        )

        if estoque_min is not None:
            consulta = consulta.having(quantidade_estoque >= estoque_min)
        if estoque_max is not None:
            consulta = consulta.having(quantidade_estoque <= estoque_max)

        consulta = consulta.order_by(AlbumModel.nome)

        resultado = self.session.execute(consulta)
        return [self._converter_linha_para_dict(linha) for linha in resultado]

    def atualizar(self, album: Album) -> bool:
        album_model = self.session.get(AlbumModel, album.id)
        if album_model is None:
            return False

        album_model.nome = album.nome
        album_model.tamanho = album.tamanho
        album_model.genero = album.genero
        album_model.artista = album.artista
        album_model.preco = album.preco
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return True

    def possui_estoque(self, album_id: int) -> bool:
        """Verifica se o album tem algum registro na tabela estoque (unidade
        disponivel ou ja vendida/associada a uma compra). Usado para bloquear
        a remocao do album enquanto isso for verdade."""
        resultado = self.session.execute(
            select(EstoqueModel.id).where(EstoqueModel.album_id == album_id).limit(1)
        ).first()
        return resultado is not None

    def remover(self, id_album: int) -> bool:
        album_model = self.session.get(AlbumModel, id_album)
        if album_model is None:
            return False

        try:
            self.session.delete(album_model)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return True

    @staticmethod
    def _converter_para_entidade(album_model: AlbumModel) -> Album:
        return Album(
            id=album_model.id,
            nome=album_model.nome,
            genero=album_model.genero,
            artista=album_model.artista,
            tamanho=album_model.tamanho,
            preco=album_model.preco,
        )

    @staticmethod
    def _converter_linha_para_dict(linha) -> dict:
        return {
            "id": linha.id,
            "nome": linha.nome,
            "genero": linha.genero,
            "artista": linha.artista,
            "tamanho": linha.tamanho,
            "preco": linha.preco,
            "quantidade_estoque": int(linha.quantidade_estoque or 0),
        }
