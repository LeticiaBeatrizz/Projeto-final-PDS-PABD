from typing import Optional
from datetime import datetime

from dados.venda_repository import VendaRepository
from dados.estoque_repository import EstoqueRepository
from dados.item_venda_repository import ItemVendaRepository
from dominio.venda import Venda
from dominio.item_venda import ItemVenda


class VendaService:
    """Camada de negócio: aplica validações e regras simples."""

    def __init__(
        self,
        repositorio: VendaRepository,
        repo_estoque: Optional[EstoqueRepository] = None,
        repo_item_venda: Optional[ItemVendaRepository] = None,
    ) -> None:
        self.repositorio = repositorio
        self.repo_estoque = repo_estoque
        self.repo_item_venda = repo_item_venda

    def registrar_venda(self, vendedor_id: int, cpf_cliente: Optional[str] = None) -> Venda:
        if vendedor_id <= 0:
            raise ValueError("O ID do vendedor deve ser um numero inteiro positivo.")

        if cpf_cliente is not None:
            cpf_limpo = cpf_cliente.strip()
            if cpf_limpo and len(cpf_limpo) != 11:
                raise ValueError("O CPF do cliente deve ter 11 digitos.")
            cpf_cliente = cpf_limpo or None

        venda = Venda(id=None, vendedor_id=vendedor_id, data=datetime.now(), cpf_cliente=cpf_cliente)
        novo_id = self.repositorio.adicionar(venda)
        venda.id = novo_id
        return venda

    def listar_vendas(self) -> list[Venda]:
        return self.repositorio.listar_todos()

    def buscar_vendas_por_texto(self, texto: str) -> list[Venda]:
        return self.repositorio.buscar_por_texto(texto)

    def buscar_venda_por_id(self, id_venda: int) -> Optional[Venda]:
        if id_venda <= 0:
            raise ValueError("O ID deve ser um numero inteiro positivo.")
        return self.repositorio.buscar_por_id(id_venda)

    def atualizar_venda(self, id_venda: int, vendedor_id: int, cpf_cliente: Optional[str] = None) -> bool:
        if id_venda <= 0:
            raise ValueError("O ID deve ser um numero inteiro positivo.")

        if vendedor_id <= 0:
            raise ValueError("O ID do vendedor deve ser um numero inteiro positivo.")

        if cpf_cliente is not None:
            cpf_limpo = cpf_cliente.strip()
            if cpf_limpo and len(cpf_limpo) != 11:
                raise ValueError("O CPF do cliente deve ter 11 digitos.")
            cpf_cliente = cpf_limpo or None

        venda_existente = self.buscar_venda_por_id(id_venda)
        if venda_existente is None:
            raise ValueError("Venda nao encontrada para o ID informado.")

        venda = Venda(id=id_venda, vendedor_id=vendedor_id, data=venda_existente.data, cpf_cliente=cpf_cliente)
        return self.repositorio.atualizar(venda)

    def remover_venda(self, id_venda: int) -> bool:
        if id_venda <= 0:
            raise ValueError("O ID deve ser um numero inteiro positivo.")
        return self.repositorio.remover(id_venda)

    def buscar_nomes_albuns_da_venda(self, venda_id: int) -> list[str]:
        """Retorna os nomes dos albuns vendidos numa venda, para exibicao."""
        if self.repo_item_venda is None:
            return []
        if venda_id <= 0:
            raise ValueError("O ID da venda deve ser um numero inteiro positivo.")
        return self.repo_item_venda.buscar_nomes_albuns_por_venda(venda_id)

    def registrar_venda_completa(
        self,
        vendedor_id: int,
        cpf_cliente: Optional[str],
        album_ids: list[int],
    ) -> Venda:
        """Registra uma venda completa: cria a venda, baixa uma unidade de estoque
        para cada album informado (repeticoes contam como quantidade) e cria os
        respectivos registros de item_venda.

        Precisa ter sido construido com repo_estoque e repo_item_venda.
        """
        if self.repo_estoque is None or self.repo_item_venda is None:
            raise ValueError("VendaService nao foi configurado com estoque/item_venda.")

        if vendedor_id <= 0:
            raise ValueError("O ID do vendedor deve ser um numero inteiro positivo.")

        if not album_ids:
            raise ValueError("Adicione pelo menos um album a venda.")

        # Garante que ha estoque disponivel em quantidade suficiente para cada
        # album, considerando repeticoes (ex: 2x o mesmo album no carrinho).
        # Isso e verificado ANTES de criar a venda, para nao gerar uma venda
        # "pela metade" quando o estoque nao for suficiente.
        quantidade_necessaria: dict[int, int] = {}
        for album_id in album_ids:
            quantidade_necessaria[album_id] = quantidade_necessaria.get(album_id, 0) + 1

        for album_id, quantidade in quantidade_necessaria.items():
            disponivel = self.repo_estoque.contar_disponivel_por_album(album_id)
            if disponivel < quantidade:
                raise ValueError(
                    f"Estoque insuficiente para o album de ID {album_id}: "
                    f"solicitado {quantidade}, disponível {disponivel}."
                )

        if cpf_cliente is not None:
            cpf_limpo = cpf_cliente.strip()
            if cpf_limpo and len(cpf_limpo) != 11:
                raise ValueError("O CPF do cliente deve ter 11 digitos.")
            cpf_cliente = cpf_limpo or None

        # Tudo abaixo roda em UMA UNICA transacao: cada insercao/atualizacao usa
        # flush (nao commit), e so ha um commit no final. Se qualquer passo
        # falhar (ex: condicao de corrida deixando o estoque insuficiente),
        # a sessao inteira e revertida com rollback, entao nunca fica uma
        # venda "pela metade" salva no banco.
        session = self.repositorio.session
        try:
            venda_id = self.repositorio.adicionar_sem_commit(
                Venda(id=None, vendedor_id=vendedor_id, data=datetime.now(), cpf_cliente=cpf_cliente)
            )

            # Reserva (marca como vendido) e cria o item_venda uma unidade por vez,
            # dentro do MESMO laco -- assim, se o carrinho tiver o mesmo album duas
            # vezes, cada repeticao pega uma unidade de estoque DIFERENTE, em vez de
            # marcar a mesma unidade como vendida duas vezes.
            for album_id in album_ids:
                id_estoque = self.repo_estoque.buscar_disponivel_por_album(album_id)
                if id_estoque is None:
                    raise ValueError(
                        f"Nao ha estoque disponivel para o album de ID {album_id}."
                    )

                self.repo_item_venda.adicionar_sem_commit(
                    ItemVenda(id=None, venda_id=venda_id, item_id=id_estoque)
                )
                self.repo_estoque.marcar_vendido_sem_commit(id_estoque)

            session.commit()
        except Exception:
            session.rollback()
            raise

        return self.repositorio.buscar_por_id(venda_id)
