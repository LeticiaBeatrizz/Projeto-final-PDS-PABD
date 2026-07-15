import tkinter as tk


class ListagemMixin:
    """Busca e renderização da listagem de álbuns com sua quantidade em estoque.

    Depende de ModaisBaseMixin (self.criar_container_lista / self.criar_corpo_rolavel).
    """

    def obter_albuns(self, texto: str = ""):
        if self.servico_album is None:
            return []
        try:
            return self.servico_album.buscar_catalogo(texto)
        except Exception:
            return []

    def buscar_estoque(self):
        termo = self.entry_busca.get().strip()
        self.lbl_status.config(text="")

        if self.servico_album is None:
            self.lbl_status.config(text="Banco de dados não conectado.")
            albuns = []
        else:
            try:
                albuns = self.servico_album.buscar_catalogo(termo)
            except Exception as erro:
                self.lbl_status.config(text=f"Erro ao buscar álbuns: {erro}")
                albuns = []

        self.atualizar_listagem(albuns)

    def atualizar_listagem(self, albuns):
        if getattr(self, "frame_tabela", None) is not None:
            self.frame_tabela.destroy()

        self.frame_tabela = self.criar_container_lista(altura=360)

        frame_cabecalho = tk.Frame(self.frame_tabela, bg=self.COR_VERMELHO_BOTAO)
        frame_cabecalho.pack(fill="x")

        lbl_col_album = tk.Label(frame_cabecalho, text="Álbum", font=("poppins", 14, "bold"), fg="#ffffff", bg=self.COR_VERMELHO_BOTAO, anchor="w", padx=15, pady=10)
        lbl_col_album.pack(side="left", fill="x", expand=True)

        lbl_col_disp = tk.Label(frame_cabecalho, text="Disponível", font=("poppins", 14, "bold"), fg="#ffffff", bg=self.COR_VERMELHO_BOTAO, anchor="w", padx=15, pady=10)
        lbl_col_disp.pack(side="right")

        frame_lista = self.criar_corpo_rolavel(self.frame_tabela)

        if not albuns:
            lbl_placeholder = tk.Label(frame_lista, text="Nenhum álbum encontrado.", font=("poppins", 12), fg="#7a7a7a", bg="#ffffff")
            lbl_placeholder.pack(anchor="w")
            return

        for indice, album in enumerate(albuns, start=1):
            linha = tk.Frame(frame_lista, bg="#ffffff", height=36)
            linha.pack(fill="x", pady=4)
            linha.pack_propagate(False)

            texto_album = f"{indice:02d} - '{album.get('nome', 'N/A')}'"
            lbl_texto = tk.Label(linha, text=texto_album, font=("poppins", 12), fg=self.COR_TEXTO_ESCURO, bg="#ffffff", anchor="w")
            lbl_texto.pack(side="left", fill="x", expand=True)

            quantidade = album.get("quantidade_estoque", 0)
            lbl_disponivel = tk.Label(linha, text=f"'{quantidade}' unidades.", font=("poppins", 12), fg=self.COR_TEXTO_ESCURO, bg="#ffffff", anchor="e")
            lbl_disponivel.pack(side="right", padx=(0, 10))
