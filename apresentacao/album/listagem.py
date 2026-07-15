import tkinter as tk
import tkinter.font as tkfont


class ListagemMixin:
    """Busca, filtros e renderização da listagem de álbuns.

    Depende de ModaisBaseMixin (self.criar_lista_rolavel).
    """

    def obter_albuns(self):
        if self.servico_album is None:
            return []

        try:
            return self.servico_album.buscar_catalogo("")
        except Exception:
            return []

    def _parse_int_campo(self, entry, nome_campo):
        texto = entry.get().strip()
        if not texto:
            return None
        try:
            return int(texto)
        except ValueError:
            raise ValueError(f"Informe um número inteiro válido para {nome_campo}.")

    def _parse_float_campo(self, entry, nome_campo):
        texto = entry.get().strip()
        if not texto:
            return None
        try:
            return float(texto.replace(",", "."))
        except ValueError:
            raise ValueError(f"Informe um número válido para {nome_campo}.")

    def limpar_filtros(self):
        self.entry_busca.delete(0, tk.END)
        self.entry_tamanho_min.delete(0, tk.END)
        self.entry_tamanho_max.delete(0, tk.END)
        self.entry_preco_min.delete(0, tk.END)
        self.entry_preco_max.delete(0, tk.END)
        self.entry_estoque_min.delete(0, tk.END)
        self.entry_estoque_max.delete(0, tk.END)
        self.buscar_albuns()

    def buscar_albuns(self):
        termo = self.entry_busca.get().strip()
        self.lbl_status_busca.config(text="")

        if self.servico_album is None:
            self.lbl_status_busca.config(text="Banco de dados não conectado.")
            self.atualizar_listagem([])
            return

        try:
            tamanho_min = self._parse_int_campo(self.entry_tamanho_min, "o tamanho mínimo")
            tamanho_max = self._parse_int_campo(self.entry_tamanho_max, "o tamanho máximo")
            preco_min = self._parse_float_campo(self.entry_preco_min, "o preço mínimo")
            preco_max = self._parse_float_campo(self.entry_preco_max, "o preço máximo")
            estoque_min = self._parse_int_campo(self.entry_estoque_min, "o estoque mínimo")
            estoque_max = self._parse_int_campo(self.entry_estoque_max, "o estoque máximo")
        except ValueError as erro:
            self.lbl_status_busca.config(text=str(erro))
            return

        try:
            albuns = self.servico_album.buscar_catalogo_avancado(
                termo,
                tamanho_min=tamanho_min,
                tamanho_max=tamanho_max,
                preco_min=preco_min,
                preco_max=preco_max,
                estoque_min=estoque_min,
                estoque_max=estoque_max,
            )
        except ValueError as erro:
            self.lbl_status_busca.config(text=str(erro))
            albuns = []
        except Exception as erro:
            self.lbl_status_busca.config(text=f"Erro ao buscar álbuns: {erro}")
            albuns = []

        self.atualizar_listagem(albuns)

    def atualizar_listagem(self, albuns):
        if getattr(self, "frame_tabela", None) is not None:
            self.frame_tabela.destroy()

        self.frame_tabela, frame_lista = self.criar_lista_rolavel("Catálogo de Álbuns", altura=320)

        if not albuns:
            lbl_placeholder = tk.Label(frame_lista, text="Nenhum álbum encontrado.", font=("poppins", 12), fg="#7a7a7a", bg="#ffffff")
            lbl_placeholder.pack(anchor="w")
            return

        fonte_linha = tkfont.Font(family="poppins", size=12)

        for album in albuns:
            texto_album = (
                f"Nome: {album.get('nome', 'N/A')}  |  "
                f"Artista: {album.get('artista', 'N/A')}  |  "
                f"Preço: R$ {album.get('preco', 0):.2f}  |  "
                f"Gênero: {album.get('genero', 'N/A')}  |  "
                f"Tamanho: {album.get('tamanho', 'N/A')}  |  "
                f"Estoque: {album.get('quantidade_estoque', 0)}"
            )

            # A linha precisa saber sua largura real (texto + botões + folga) ANTES
            # de ser travada com pack_propagate(False); senao a area rolavel nunca
            # fica sabendo que o conteudo ultrapassa a largura visivel, e a barra
            # de rolagem horizontal fica sem efeito nas linhas mais compridas.
            largura_linha = fonte_linha.measure(texto_album) + 90

            linha = tk.Frame(frame_lista, bg="#ffffff", height=48, width=largura_linha)
            linha.pack(fill="x", pady=5)
            linha.pack_propagate(False)

            lbl_texto = tk.Label(linha, text=texto_album, font=("poppins", 12), fg=self.COR_TEXTO_ESCURO, bg="#ffffff", anchor="w")
            lbl_texto.pack(side="left", fill="x", expand=True)

            btn_excluir = tk.Button(
                linha,
                text="🗑",
                font=("poppins", 14),
                fg=self.COR_TEXTO_ESCURO,
                bg="#ffffff",
                bd=0,
                activebackground="#ffffff",
                cursor="hand2",
                command=lambda album_id=album.get('id'), album_nome=album.get('nome'): self.abrir_modal_confirmacao_exclusao(album_id, album_nome),
            )
            btn_excluir.pack(side="right", padx=(5, 10))

            btn_atualizar = tk.Button(
                linha,
                text="📝",
                font=("poppins", 12),
                fg=self.COR_TEXTO_ESCURO,
                bg="#ffffff",
                bd=0,
                activebackground="#ffffff",
                cursor="hand2",
                command=lambda album_atual=album: self.abrir_modal_atualizacao(album_atual),
            )
            btn_atualizar.pack(side="right", padx=(5, 0))
