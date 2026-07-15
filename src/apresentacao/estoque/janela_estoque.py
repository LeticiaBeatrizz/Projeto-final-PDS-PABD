import tkinter as tk

from .desenho import DesenhoMixin
from .modais_base import ModaisBaseMixin
from .layout import LayoutMixin
from .listagem import ListagemMixin
from .adicionar_estoque import AdicionarEstoqueMixin
from .remover_estoque import RemoverEstoqueMixin


class TelaEstoque(
    DesenhoMixin,
    ModaisBaseMixin,
    LayoutMixin,
    ListagemMixin,
    AdicionarEstoqueMixin,
    RemoverEstoqueMixin,
):
    """Camada apresentacao: tela de estoque e catalogo.

    Mostra, para cada album do catalogo, quantas unidades ainda estao
    disponiveis para venda, e permite dar entrada de novas unidades.
    Toda a logica passa pela camada de negocio (EstoqueService/AlbumService).

    Esta classe apenas monta as funcionalidades, que estao divididas em
    arquivos menores (mixins) dentro deste mesmo pacote:
      - desenho.py           -> desenhar_fundo_arredondado
      - modais_base.py        -> criar_container_lista, criar_corpo_rolavel, criar_modal_rolavel
      - layout.py              -> criar_layout
      - listagem.py            -> obter_albuns, buscar_estoque, atualizar_listagem
      - adicionar_estoque.py   -> abrir_modal_adicionar_estoque
      - remover_estoque.py     -> abrir_modal_remover_estoque
    """

    def __init__(self, parent, servico_estoque=None, servico_album=None):
        self.parent = parent
        self.parent.configure(bg="#fff5f5")
        self.servico_estoque = servico_estoque
        self.servico_album = servico_album

        self.COR_BG = "#fff5f5"
        self.COR_TEXTO_ESCURO = "#4a0e06"
        self.COR_VERMELHO_BOTAO = "#e87c74"

        self.frame = tk.Frame(self.parent, bg=self.COR_BG)
        self.frame.pack(fill="both", expand=True)

        self.criar_layout()
