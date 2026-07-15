import tkinter as tk


class ModaisBaseMixin:
    """Componentes reutilizáveis: container de listagem, corpo rolável e modal rolável.

    Depende de DesenhoMixin (usa self.desenhar_fundo_arredondado).
    """

    def criar_container_lista(self, altura=320):
        """Cria o container fixo da listagem, ocupando toda a largura disponivel."""
        frame_tabela = tk.Frame(self.conteudo, bg="#ffffff", bd=0, height=altura)
        frame_tabela.pack_propagate(False)
        frame_tabela.pack(fill="x", expand=False, pady=10)
        return frame_tabela

    def criar_corpo_rolavel(self, frame_pai):
        """Cria a area rolavel dentro de frame_pai (abaixo de qualquer cabecalho
        ja empacotado nele) e retorna o frame onde as linhas devem ser inseridas.
        """
        corpo = tk.Frame(frame_pai, bg="#ffffff")
        corpo.pack(fill="both", expand=True)

        canvas_lista = tk.Canvas(corpo, bg="#ffffff", highlightthickness=0)
        scrollbar_lista = tk.Scrollbar(corpo, orient="vertical", command=canvas_lista.yview)
        canvas_lista.configure(yscrollcommand=scrollbar_lista.set)
        canvas_lista.pack(side="left", fill="both", expand=True)
        scrollbar_lista.pack(side="right", fill="y")

        frame_lista = tk.Frame(canvas_lista, bg="#ffffff", padx=15, pady=15)
        janela_lista = canvas_lista.create_window((0, 0), window=frame_lista, anchor="nw")

        def _atualizar_scrollregion(event=None):
            canvas_lista.configure(scrollregion=canvas_lista.bbox("all"))

        def _ajustar_largura(event):
            canvas_lista.itemconfig(janela_lista, width=event.width)

        frame_lista.bind("<Configure>", _atualizar_scrollregion)
        canvas_lista.bind("<Configure>", _ajustar_largura)

        def _on_mousewheel(event):
            canvas_lista.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas_lista.bind("<Enter>", lambda e: canvas_lista.bind_all("<MouseWheel>", _on_mousewheel))
        canvas_lista.bind("<Leave>", lambda e: canvas_lista.unbind_all("<MouseWheel>"))

        return frame_lista

    def criar_modal_rolavel(self, titulo_janela, largura=500, altura_desejada=480, cor_fundo_modal="#ffe8e4"):
        """Cria um Toplevel com fundo arredondado, area de conteudo rolavel (para os
        campos do formulario) e uma barra de botoes fixa na parte de baixo, que fica
        sempre visivel mesmo em telas menores ou com muitos campos.

        Retorna (modal, area_conteudo, area_botoes).
        """
        modal = tk.Toplevel(self.parent)
        modal.title(titulo_janela)
        modal.configure(bg=cor_fundo_modal)
        modal.transient(self.parent)
        modal.grab_set()

        screen_width = modal.winfo_screenwidth()
        screen_height = modal.winfo_screenheight()
        altura = min(altura_desejada, screen_height - 80)
        x = (screen_width - largura) // 2
        y = max(10, (screen_height - altura) // 2)
        modal.geometry(f"{largura}x{altura}+{x}+{y}")
        modal.minsize(largura, 320)

        canvas_modal = self.desenhar_fundo_arredondado(modal, largura=largura - 20, altura=altura - 20, raio=24, cor_fundo=cor_fundo_modal, cor_forma="#ffffff")
        canvas_modal.place(relx=0.5, rely=0.5, anchor="center")

        frame_modal_raiz = tk.Frame(modal, bg="#ffffff", bd=0, relief="flat")
        canvas_modal.create_window((largura - 20) / 2, (altura - 20) / 2, window=frame_modal_raiz, width=largura - 40, height=altura - 40)

        frame_modal_raiz.grid_rowconfigure(0, weight=1)
        frame_modal_raiz.grid_rowconfigure(1, weight=0)
        frame_modal_raiz.grid_columnconfigure(0, weight=1)

        area_rolavel = tk.Canvas(frame_modal_raiz, bg="#ffffff", highlightthickness=0)
        area_rolavel.grid(row=0, column=0, sticky="nsew")

        scrollbar_area = tk.Scrollbar(frame_modal_raiz, orient="vertical", command=area_rolavel.yview)
        scrollbar_area.grid(row=0, column=1, sticky="ns")
        area_rolavel.configure(yscrollcommand=scrollbar_area.set)

        conteudo_scroll = tk.Frame(area_rolavel, bg="#ffffff")
        janela_scroll = area_rolavel.create_window((0, 0), window=conteudo_scroll, anchor="nw")

        def _atualizar_scrollregion(event=None):
            area_rolavel.configure(scrollregion=area_rolavel.bbox("all"))

        def _ajustar_largura_scroll(event):
            area_rolavel.itemconfig(janela_scroll, width=event.width)

        conteudo_scroll.bind("<Configure>", _atualizar_scrollregion)
        area_rolavel.bind("<Configure>", _ajustar_largura_scroll)

        def _on_mousewheel(event):
            area_rolavel.yview_scroll(int(-1 * (event.delta / 120)), "units")

        area_rolavel.bind("<Enter>", lambda e: area_rolavel.bind_all("<MouseWheel>", _on_mousewheel))
        area_rolavel.bind("<Leave>", lambda e: area_rolavel.unbind_all("<MouseWheel>"))

        botoes_frame = tk.Frame(frame_modal_raiz, bg="#ffffff")
        botoes_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=(10, 16))

        return modal, conteudo_scroll, botoes_frame
