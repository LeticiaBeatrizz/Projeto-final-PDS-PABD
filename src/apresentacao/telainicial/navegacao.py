import tkinter as tk


class NavegacaoMixin:
    """Troca de tela ao clicar em uma opção do menu lateral, e a tela
    "Início" com o resumo de totais.

    Depende de LayoutMixin (self.limpar_conteudo) e de AtualizacoesMixin
    (self.criar_card_atualizacoes).
    """

    def on_menu_click(self, opcao):
        self.limpar_conteudo()

        if opcao == "Início":
            self.mostrar_inicio()
        elif opcao == "Álbuns":
            from ..album.janela_album import TelaAlbum
            TelaAlbum(self.conteudo, self.servico_album)
        elif opcao == "Estoque e catálogo":
            from ..estoque.janela_estoque import TelaEstoque
            TelaEstoque(self.conteudo, self.servico_estoque, self.servico_album)
        elif opcao == "Usuários":
            from ..usuarios.janela_usuarios import TelaUsuarios
            TelaUsuarios(self.conteudo, self.servico_usuario, self.usuario_logado)
        elif opcao == "Vendas":
            from ..vendas.janela_vendas import TelaVendas
            TelaVendas(self.conteudo, self.servico_venda, self.servico_album, self.servico_usuario, self.usuario_logado)
        else:
            self.mostrar_placeholder(opcao)

    def mostrar_inicio(self):
        lbl_welcome = tk.Label(self.conteudo, text=f"Bem vindo, {self.usuario_logado['nome_completo']}!", font=("poppins", 24, "bold"), fg="#4a0e06", bg="#fff5f5")
        lbl_welcome.pack(anchor="w", pady=(0, 20))

        total_albuns = len(self.servico_album.listar_albums()) if self.conexao else 0
        total_vendas = len(self.servico_venda.listar_vendas()) if self.conexao else 0

        lbl_tot_albuns = tk.Label(self.conteudo, text=f"Total de álbuns ----------------------------------- {total_albuns}", font=("poppins", 12, "bold"), fg="#4a0e06", bg="#fff5f5")
        lbl_tot_albuns.pack(anchor="w", pady=5)

        lbl_vendas = tk.Label(self.conteudo, text=f"Total de vendas -------------------------------------- {total_vendas}", font=("poppins", 12, "bold"), fg="#4a0e06", bg="#fff5f5")
        lbl_vendas.pack(anchor="w", pady=5)

        self.criar_card_atualizacoes()

    def mostrar_placeholder(self, opcao):
        lbl = tk.Label(self.conteudo, text=f"Tela '{opcao}' em desenvolvimento.", font=("poppins", 18, "bold"), fg="#4a0e06", bg="#fff5f5")
        lbl.pack(anchor="w", pady=(20, 10))
