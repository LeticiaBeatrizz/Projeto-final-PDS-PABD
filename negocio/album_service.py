from typing import Optional
from decimal import Decimal

from dados.album_repository import AlbumRepository
from dominio.album import Album


class AlbumService:
    """Camada de negócio: aplica validações e regras simples."""

    def __init__(self, repositorio: AlbumRepository) -> None:
        self.repositorio = repositorio

    def cadastrar_album(self, nome: str, genero: str, artista: str, tamanho: int, preco: Decimal) -> Album:
        nome_limpo = nome.strip()
        if not nome_limpo:
            raise ValueError("O nome do album nao pode ficar vazio.")

        genero_limpo = genero.strip()
        if not genero_limpo:
            raise ValueError("O genero do album nao pode ficar vazio.")

        artista_limpo = artista.strip()
        if not artista_limpo:
            raise ValueError("O artista do album nao pode ficar vazio.")

        if tamanho <= 0:
            raise ValueError("O tamanho do album deve ser maior que zero.")

        if preco < 0:
            raise ValueError("O preco do album nao pode ser negativo.")

        album = Album(id=None, nome=nome_limpo, genero=genero_limpo, artista=artista_limpo, tamanho=tamanho, preco=preco)
        novo_id = self.repositorio.adicionar(album)
        album.id = novo_id
        return album

    def listar_albums(self) -> list[Album]:
        return self.repositorio.listar_todos()

    def buscar_catalogo(self, texto: str = "") -> list[dict]:
        """Busca albuns por nome/genero incluindo a quantidade disponivel em estoque."""
        return self.repositorio.buscar_por_texto(texto)

    def buscar_catalogo_avancado(
        self,
        texto: str = "",
        tamanho_min: Optional[int] = None,
        tamanho_max: Optional[int] = None,
        preco_min: Optional[float] = None,
        preco_max: Optional[float] = None,
        estoque_min: Optional[int] = None,
        estoque_max: Optional[int] = None,
    ) -> list[dict]:
        """Busca albuns permitindo filtrar por faixas de tamanho, preco e estoque."""
        if tamanho_min is not None and tamanho_max is not None and tamanho_min > tamanho_max:
            raise ValueError("O tamanho mínimo não pode ser maior que o máximo.")
        if preco_min is not None and preco_max is not None and preco_min > preco_max:
            raise ValueError("O valor mínimo não pode ser maior que o máximo.")
        if estoque_min is not None and estoque_max is not None and estoque_min > estoque_max:
            raise ValueError("O estoque mínimo não pode ser maior que o máximo.")

        return self.repositorio.buscar_avancado(
            texto,
            tamanho_min=tamanho_min,
            tamanho_max=tamanho_max,
            preco_min=preco_min,
            preco_max=preco_max,
            estoque_min=estoque_min,
            estoque_max=estoque_max,
        )

    def buscar_album_por_id(self, id_album: int) -> Optional[Album]:
        if id_album <= 0:
            raise ValueError("O ID deve ser um numero inteiro positivo.")
        return self.repositorio.buscar_por_id(id_album)

    def atualizar_album(self, id_album: int, nome: str, genero: str, artista: str, tamanho: int, preco: Decimal) -> bool:
        if id_album <= 0:
            raise ValueError("O ID deve ser um numero inteiro positivo.")

        nome_limpo = nome.strip()
        if not nome_limpo:
            raise ValueError("O nome do album nao pode ficar vazio.")

        genero_limpo = genero.strip()
        if not genero_limpo:
            raise ValueError("O genero do album nao pode ficar vazio.")

        artista_limpo = artista.strip()
        if not artista_limpo:
            raise ValueError("O artista do album nao pode ficar vazio.")

        if tamanho <= 0:
            raise ValueError("O tamanho do album deve ser maior que zero.")

        if preco < 0:
            raise ValueError("O preco do album nao pode ser negativo.")

        album = Album(id=id_album, nome=nome_limpo, genero=genero_limpo, artista=artista_limpo, tamanho=tamanho, preco=preco)
        return self.repositorio.atualizar(album)

    def remover_album(self, id_album: int) -> bool:
        if id_album <= 0:
            raise ValueError("O ID deve ser um numero inteiro positivo.")

        if self.repositorio.possui_estoque(id_album):
            raise ValueError(
                "Não é possível remover um álbum que possui itens no estoque "
                "ou associados a alguma compra."
            )

        return self.repositorio.remover(id_album)
