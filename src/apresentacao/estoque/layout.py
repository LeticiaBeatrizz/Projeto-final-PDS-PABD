import tkinter as tk


class LayoutMixin:
    """Monta o layout principal da tela de estoque: título, busca e botões
    de adicionar/remover.

    Depende de DesenhoMixin e de ListagemMixin (self.atualizar_listagem / self.obter_albuns).
    """

    def criar_layout(self):
        self.conteudo = tk.Frame(self.frame, bg=self.COR_BG, padx=40, pady=40)
        self.conteudo.pack(fill="both", expand=True)

        lbl_titulo = tk.Label(self.conteudo, text="Selecionar álbum", font=("poppins", 24, "bold"), fg=self.COR_TEXTO_ESCURO, bg=self.COR_BG)
        lbl_titulo.pack(anchor="w", pady=(0, 20))

        frame_controles = tk.Frame(self.conteudo, bg=self.COR_BG)
        frame_controles.pack(anchor="w", fill="x", pady=(0, 20))

        canvas_busca = self.desenhar_fundo_arredondado(frame_controles, largura=220, altura=35, raio=12, cor_fundo=self.COR_BG, cor_forma="#ffffff")
        canvas_busca.pack(side="left")

        self.entry_busca = tk.Entry(canvas_busca, font=("poppins", 11), fg=self.COR_TEXTO_ESCURO, bg="#ffffff", bd=0, highlightthickness=0)
        self.entry_busca.bind("<Return>", lambda event: self.buscar_estoque())
        canvas_busca.create_window(15, 17, window=self.entry_busca, width=160, anchor="w")

        canvas_busca.create_oval(185, 10, 195, 20, outline=self.COR_TEXTO_ESCURO, width=2)
        canvas_busca.create_line(193, 18, 199, 24, fill=self.COR_TEXTO_ESCURO, width=2)

        canvas_btn_cadastrar = self.desenhar_fundo_arredondado(frame_controles, largura=130, altura=35, raio=12, cor_fundo=self.COR_BG, cor_forma=self.COR_VERMELHO_BOTAO)
        canvas_btn_cadastrar.pack(side="left", padx=(10, 0))
        btn_cadastrar = tk.Button(canvas_btn_cadastrar, text="+ Cadastrar", font=("poppins", 11, "bold"), fg="#ffffff", bg=self.COR_VERMELHO_BOTAO, bd=0, activebackground=self.COR_VERMELHO_BOTAO, activeforeground="#ffffff", cursor="hand2", command=self.abrir_modal_adicionar_estoque)
        canvas_btn_cadastrar.create_window(65, 17, window=btn_cadastrar, width=120, height=30)

        canvas_btn_remover = self.desenhar_fundo_arredondado(frame_controles, largura=130, altura=35, raio=12, cor_fundo=self.COR_BG, cor_forma="#f0d7d3")
        canvas_btn_remover.pack(side="left", padx=(10, 0))
        btn_remover = tk.Button(canvas_btn_remover, text="- Remover", font=("poppins", 11, "bold"), fg="#5f1c16", bg="#f0d7d3", bd=0, activebackground="#e4d1cd", activeforeground="#5f1c16", cursor="hand2", command=self.abrir_modal_remover_estoque)
        canvas_btn_remover.create_window(65, 17, window=btn_remover, width=120, height=30)

        self.lbl_status = tk.Label(self.conteudo, text="", font=("poppins", 10), fg="#c94a3f", bg=self.COR_BG)
        self.lbl_status.pack(anchor="w", pady=(0, 8))

        self.atualizar_listagem(self.obter_albuns())
