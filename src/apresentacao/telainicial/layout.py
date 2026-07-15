import tkinter as tk


class LayoutMixin:
    """Monta o layout principal da janela: barra superior, sidebar com o
    menu de navegação e a área de conteúdo.

    Depende de ImagensMixin (self.img_logo / self.img_usuario) e de
    NavegacaoMixin (self.on_menu_click / self.mostrar_inicio).
    """

    def criar_layout(self):
        # 1. Barra superior
        self.top_bar = tk.Frame(self.janela, bg="#941b0c", height=80)
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.top_bar.grid_propagate(False)

            # 1.1 Container para o logo e textos da loja
        frame_logo_titulo = tk.Frame(self.top_bar, bg="#941b0c")
        frame_logo_titulo.pack(side="left", padx=20, pady=15)

        if self.img_logo:
            lbl_img_logo = tk.Label(frame_logo_titulo, image=self.img_logo, bg="#941b0c")
            lbl_img_logo.image = self.img_logo
            lbl_img_logo.pack(side="left", padx=(0, 10))

                # 1.1.2 Container interno para os textos da marca
        frame_textos_logo = tk.Frame(frame_logo_titulo, bg="#941b0c")
        frame_textos_logo.pack(side="left")

                    # 1.1.2.1 Título
        lbl_titulo_principal = tk.Label(frame_textos_logo, text="Titan", font=("poppins", 15, "bold"), fg="#ffffff", bg="#941b0c")
        lbl_titulo_principal.grid(row=0, column=0, sticky="w", pady=(0, 0))

                    # 1.1.2.2 Subtítulo
        lbl_subtitulo = tk.Label(frame_textos_logo, text="Loja de mídia física\npara música", justify="left", font=("poppins", 10), fg="#ffffff", bg="#941b0c")
        lbl_subtitulo.grid(row=1, column=0, sticky="w", pady=(0, 0))

                # 1.1.3 Divisor
        lbl_divisor = tk.Label(frame_logo_titulo, text="   | Painel do administrador", font=("poppins", 12), fg="#ffffff", bg="#941b0c")
        lbl_divisor.pack(side="left")

            # 1.2 Container para o usuário e botão de sair
        self.frame_user = tk.Frame(self.top_bar, bg="#941b0c")
        self.frame_user.pack(side="right", padx=20, pady=15)

                # 1.2.1 Imagem do usuário
        if self.img_usuario:
            lbl_img_user = tk.Label(self.frame_user, image=self.img_usuario, bg="#941b0c")
            lbl_img_user.image = self.img_usuario
            lbl_img_user.pack(side="left", padx=(0, 10))

                # 1.2.2 Container para os textos do usuário
        frame_textos_user = tk.Frame(self.frame_user, bg="#941b0c")
        frame_textos_user.pack(side="left")

        tk.Label(self.top_bar, text=f"Usuário: {self.usuario_logado['nome_completo']}", font=("poppins", 11), fg="white", bg="#941b0c").pack(side="right", padx=20)

        btn_sair = tk.Button(frame_textos_user, text="Sair", font=("poppins", 10, "underline"), fg="#ffffff", bg="#941b0c", bd=0, activebackground="#941b0c", activeforeground="#f39274", cursor="hand2", command=self.janela.quit)
        btn_sair.pack(anchor="w")

        # 2. Corpo principal (sidebar + conteúdo)
        self.body_frame = tk.Frame(self.janela, bg="#fff5f5")
        self.body_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.body_frame.grid_rowconfigure(0, weight=1)
        self.body_frame.grid_columnconfigure(0, weight=0)
        self.body_frame.grid_columnconfigure(1, weight=1)

        self.sidebar = tk.Frame(self.body_frame, bg="#f39274", width=200)
        self.sidebar.grid(row=0, column=0, sticky="nsew", pady=(2, 0))
        self.sidebar.grid_propagate(False)

        self.conteudo = tk.Frame(self.body_frame, bg="#fff5f5", padx=40, pady=40)
        self.conteudo.grid(row=0, column=1, sticky="nsew")

        self.criar_menu()
        self.mostrar_inicio()

    def criar_menu(self):
        opcoes_menu = ["Início", "Álbuns", "Estoque e catálogo", "Usuários", "Vendas"]
        for i, opcao in enumerate(opcoes_menu):
            btn = tk.Button(
                self.sidebar,
                text=opcao,
                font=("poppins", 12, "bold"),
                fg="#ffffff",
                bg="#f39274",
                bd=0,
                activebackground="#e28163",
                activeforeground="#ffffff",
                anchor="w",
                padx=20,
                cursor="hand2",
                command=lambda o=opcao: self.on_menu_click(o)
            )

            if i == 0:
                btn.pack(fill="x", pady=(30, 5))
            else:
                btn.pack(fill="x", pady=5)

    def limpar_conteudo(self):
        for widget in self.conteudo.winfo_children():
            widget.destroy()
