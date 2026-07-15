import tkinter as tk
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dados.banco import SessionLocal
from dados.album_repository import AlbumRepository
from dados.venda_repository import VendaRepository
from dados.estoque_repository import EstoqueRepository
from dados.usuario_repository import UsuarioRepository
from dados.item_venda_repository import ItemVendaRepository

from negocio.album_service import AlbumService
from negocio.estoque_service import EstoqueService
from negocio.usuario_service import UsuarioService
from negocio.venda_service import VendaService

from .imagens import ImagensMixin
from .layout import LayoutMixin
from .navegacao import NavegacaoMixin
from .atualizacoes import AtualizacoesMixin


class TelaInicial(
    ImagensMixin,
    LayoutMixin,
    NavegacaoMixin,
    AtualizacoesMixin,
):
    """Camada apresentacao: painel do administrador (tela inicial).

    Monta a barra superior, o menu lateral e a área de conteúdo, e
    orquestra a troca entre as demais telas (álbuns, estoque, usuários,
    vendas) conforme o item selecionado no menu.

    Esta classe apenas monta as funcionalidades, que estao divididas em
    arquivos menores (mixins) dentro deste mesmo pacote:
      - imagens.py          -> carregar_imagem
      - layout.py            -> criar_layout, criar_menu, limpar_conteudo
      - navegacao.py         -> on_menu_click, mostrar_inicio, mostrar_placeholder
      - atualizacoes.py      -> alternar_ordem_atualizacoes, criar_card_atualizacoes
    """

    def __init__(self, janela, usuario_logado):
        #configurações da janela principal
        self.janela = janela
        self.usuario_logado = usuario_logado
        self.janela.title("Titan - Painel do Administrador")
        self.janela.configure(bg="#fff5f5")

        #p/abrir maximizada
        self.janela.state('zoomed')

        self.janela.grid_rowconfigure(0, weight=0)
        self.janela.grid_rowconfigure(1, weight=1)

        self.janela.grid_columnconfigure(0, weight=0)
        self.janela.grid_columnconfigure(1, weight=1)

        self.repo_album = None
        self.repo_venda = None
        self.repo_estoque = None
        self.repo_usuario = None
        self.repo_item_venda = None

        self.servico_album = None
        self.servico_estoque = None
        self.servico_usuario = None
        self.servico_venda = None
        self.ordem_atualizacoes_recente_primeiro = True
        try:
            self.conexao = SessionLocal()

            self.repo_album = AlbumRepository(self.conexao)
            self.repo_venda = VendaRepository(self.conexao)
            self.repo_estoque = EstoqueRepository(self.conexao)
            self.repo_usuario = UsuarioRepository(self.conexao)
            self.repo_item_venda = ItemVendaRepository(self.conexao)

            self.servico_album = AlbumService(self.repo_album)
            self.servico_estoque = EstoqueService(self.repo_estoque)
            self.servico_usuario = UsuarioService(self.repo_usuario, self.repo_venda)
            self.servico_venda = VendaService(
                self.repo_venda, self.repo_estoque, self.repo_item_venda
            )

        except Exception as e:
            print(f"Aviso: Rodando painel offline. Erro: {e}")
            self.conexao = None

        # Garante que a sessao SQLAlchemy seja fechada quando a janela for encerrada.
        self.janela.protocol("WM_DELETE_WINDOW", self._encerrar)

        self.carregar_imagem()
        self.criar_layout()

    def _encerrar(self) -> None:
        if self.conexao is not None:
            self.conexao.close()
        self.janela.destroy()
