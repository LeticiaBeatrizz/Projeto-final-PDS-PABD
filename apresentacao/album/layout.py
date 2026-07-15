import tkinter as tk


class LayoutMixin:
    """Monta o layout principal da tela de álbuns: título, controles de
    busca/filtro e a listagem inicial.

    Depende de DesenhoMixin e de ListagemMixin (self.atualizar_listagem / self.obter_albuns).
    """

    def criar_layout(self):
        self.conteudo = tk.Frame(self.frame, bg=self.COR_BG, padx=40, pady=40)
        self.conteudo.pack(fill="both", expand=True)

        # Título da seção
        lbl_welcome = tk.Label(self.conteudo, text="Álbuns", font=("poppins", 24, "bold"), fg=self.COR_TEXTO_ESCURO, bg=self.COR_BG)
        lbl_welcome.pack(anchor="w", pady=(0, 20))

        # Container para os controles (Botão Cadastrar e Campo de Busca)
        frame_controles = tk.Frame(self.conteudo, bg=self.COR_BG)
        frame_controles.pack(anchor="w", fill="x", pady=(0, 20))

        # --- BOTÃO CADASTRAR COM CANVAS APENAS NO FUNDO ---
        canvas_btn = self.desenhar_fundo_arredondado(frame_controles, largura=130, altura=35, raio=12, cor_fundo=self.COR_BG, cor_forma=self.COR_VERMELHO_BOTAO)
        canvas_btn.pack(side="left", padx=(0, 15))

        btn_cadastrar = tk.Button(canvas_btn, text="+ Cadastrar", font=("poppins", 11, "bold"), fg="#ffffff", bg=self.COR_VERMELHO_BOTAO, bd=0, activebackground=self.COR_VERMELHO_BOTAO, activeforeground="#ffffff", cursor="hand2", command=self.abrir_modal_cadastro)
        canvas_btn.create_window(65, 17, window=btn_cadastrar, width=120, height=30)

        canvas_busca = self.desenhar_fundo_arredondado(frame_controles, largura=220, altura=35, raio=12, cor_fundo=self.COR_BG, cor_forma="#ffffff")
        canvas_busca.pack(side="left")

        self.entry_busca = tk.Entry(canvas_busca, font=("poppins", 11), fg=self.COR_TEXTO_ESCURO, bg="#ffffff", bd=0, highlightthickness=0)
        self.entry_busca.insert(0, "")
        self.entry_busca.bind("<Return>", lambda event: self.buscar_albuns())
        canvas_busca.create_window(15, 17, window=self.entry_busca, width=160, anchor="w")

        canvas_busca.create_oval(185, 10, 195, 20, outline=self.COR_TEXTO_ESCURO, width=2)
        canvas_busca.create_line(193, 18, 199, 24, fill=self.COR_TEXTO_ESCURO, width=2)

        canvas_btn_buscar = self.desenhar_fundo_arredondado(frame_controles, largura=100, altura=35, raio=12, cor_fundo=self.COR_BG, cor_forma=self.COR_VERMELHO_BOTAO)
        canvas_btn_buscar.pack(side="left", padx=(10, 0), pady=1)
        btn_buscar = tk.Button(canvas_btn_buscar, text="Buscar", font=("poppins", 11, "bold"), fg="#ffffff", bg=self.COR_VERMELHO_BOTAO, bd=0, activebackground=self.COR_VERMELHO_BOTAO, activeforeground="#ffffff", cursor="hand2", command=self.buscar_albuns)
        canvas_btn_buscar.create_window(50, 17, window=btn_buscar, width=90, height=30)

        txt_orientacao = tk.Label(self.conteudo, text="Busque por nome, gênero ou artista, e refine por tamanho, preço e estoque.", font=("poppins", 10), fg="#7a7a7a", bg=self.COR_BG)
        txt_orientacao.pack(anchor="w", pady=(0, 10))

        # --- LINHA DE FILTROS AVANÇADOS (TAMANHO, PREÇO E ESTOQUE) ---
        frame_filtros = tk.Frame(self.conteudo, bg=self.COR_BG)
        frame_filtros.pack(anchor="w", fill="x", pady=(0, 15))

        def criar_par_filtro(label_text):
            container = tk.Frame(frame_filtros, bg=self.COR_BG)
            container.pack(side="left", padx=(0, 18))
            tk.Label(container, text=label_text, font=("poppins", 9, "bold"), fg=self.COR_TEXTO_ESCURO, bg=self.COR_BG).pack(anchor="w")
            linha = tk.Frame(container, bg=self.COR_BG)
            linha.pack(anchor="w", pady=(3, 0))
            entry_min = tk.Entry(linha, font=("poppins", 10), width=6, bd=1, relief="solid", fg=self.COR_TEXTO_ESCURO)
            entry_min.pack(side="left")
            tk.Label(linha, text=" a ", font=("poppins", 9), bg=self.COR_BG, fg=self.COR_TEXTO_ESCURO).pack(side="left")
            entry_max = tk.Entry(linha, font=("poppins", 10), width=6, bd=1, relief="solid", fg=self.COR_TEXTO_ESCURO)
            entry_max.pack(side="left")
            entry_min.bind("<Return>", lambda event: self.buscar_albuns())
            entry_max.bind("<Return>", lambda event: self.buscar_albuns())
            return entry_min, entry_max

        self.entry_tamanho_min, self.entry_tamanho_max = criar_par_filtro("Tamanho (faixas)")
        self.entry_preco_min, self.entry_preco_max = criar_par_filtro("Preço (R$)")
        self.entry_estoque_min, self.entry_estoque_max = criar_par_filtro("Estoque")

        canvas_btn_limpar = self.desenhar_fundo_arredondado(frame_filtros, largura=110, altura=32, raio=10, cor_fundo=self.COR_BG, cor_forma="#f0d7d3")
        canvas_btn_limpar.pack(side="left", padx=(0, 0), pady=(15, 0))
        btn_limpar = tk.Button(canvas_btn_limpar, text="Limpar filtros", font=("poppins", 9, "bold"), fg="#5f1c16", bg="#f0d7d3", bd=0, activebackground="#e4d1cd", cursor="hand2", command=self.limpar_filtros)
        canvas_btn_limpar.create_window(55, 16, window=btn_limpar, width=100, height=28)

        self.lbl_status_busca = tk.Label(self.conteudo, text="", font=("poppins", 10), fg="#c94a3f", bg=self.COR_BG)
        self.lbl_status_busca.pack(anchor="w", pady=(0, 8))

        self.atualizar_listagem(self.obter_albuns())
