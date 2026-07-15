import tkinter as tk

from .imagens import ImagensMixin
from .desenho import DesenhoMixin
from .modais_base import ModaisBaseMixin
from .layout import LayoutMixin
from .cadastro import CadastroMixin
from .atualizacao import AtualizacaoMixin
from .exclusao import ExclusaoMixin
from .listagem import ListagemMixin


class TelaAlbum(
    ImagensMixin,
    DesenhoMixin,
    ModaisBaseMixin,
    LayoutMixin,
    CadastroMixin,
    AtualizacaoMixin,
    ExclusaoMixin,
    ListagemMixin,
):
    """Camada apresentacao: tela de cadastro/consulta de albuns.

    Toda a validacao e persistencia passa pela camada de negocio
    (AlbumService), que por sua vez conversa com o AlbumRepository.

    Esta classe apenas monta as funcionalidades, que estao divididas em
    arquivos menores (mixins) dentro deste mesmo pacote:
      - imagens.py       -> carregar_imagem
      - desenho.py        -> desenhar_fundo_arredondado
      - modais_base.py     -> criar_modal_rolavel, criar_lista_rolavel
      - layout.py           -> criar_layout
      - cadastro.py         -> abrir_modal_cadastro, confirmar_cadastro
      - atualizacao.py      -> abrir_modal_atualizacao
      - exclusao.py         -> abrir_modal_confirmacao_exclusao, excluir_album
      - listagem.py         -> obter_albuns, buscar_albuns, limpar_filtros, atualizar_listagem
    """

    def __init__(self, parent, servico_album=None):
        self.parent = parent
        self.parent.configure(bg="#fff5f5")
        self.servico_album = servico_album

        self.COR_BG = "#fff5f5"
        self.COR_TEXTO_ESCURO = "#4a0e06"
        self.COR_LARANJA_MENU = "#f39274"
        self.COR_VERMELHO_BOTAO = "#e87c74"
        self.COR_MODAL_BG = "#fffaf9"

        self.frame = tk.Frame(self.parent, bg=self.COR_BG)
        self.frame.pack(fill="both", expand=True)

        self.carregar_imagem()
        self.criar_layout()
