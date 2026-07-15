import tkinter as tk

from negocio.atividades import obter_atividades


class AtualizacoesMixin:
    """Card de "Últimas atualizações do sistema", exibido na tela Início."""

    def alternar_ordem_atualizacoes(self):
        """Inverte a ordem de exibicao das atualizacoes (mais antiga <-> mais nova)."""
        self.ordem_atualizacoes_recente_primeiro = not self.ordem_atualizacoes_recente_primeiro
        self.criar_card_atualizacoes()

    def criar_card_atualizacoes(self):
        # Se o card ja existir (ex: ao trocar a ordem), remove antes de recriar
        if getattr(self, "frame_card", None) is not None:
            self.frame_card.destroy()

        # Card container branco limpo, ocupando toda a largura disponivel
        frame_card = tk.Frame(self.conteudo, bg="#ffffff", bd=0, height=280)
        frame_card.pack_propagate(False)
        frame_card.pack(fill="x", expand=False, pady=25)
        self.frame_card = frame_card

        # Cabeçalho do Card
        topo_card = tk.Frame(frame_card, bg="#e87c74")
        topo_card.pack(fill="x")

        lbl_topo = tk.Label(topo_card, text="Últimas atualizações do sistema", font=("poppins", 16, "bold"), fg="#ffffff", bg="#e87c74", anchor="w", padx=15, pady=10)
        lbl_topo.pack(side="left")

        texto_botao_ordem = "↑ Mais antigas primeiro" if self.ordem_atualizacoes_recente_primeiro else "↓ Mais recentes primeiro"
        btn_ordem = tk.Button(
            topo_card,
            text=texto_botao_ordem,
            font=("poppins", 10, "bold"),
            fg="#e87c74",
            bg="#ffffff",
            bd=0,
            activebackground="#ffe8e4",
            activeforeground="#e87c74",
            cursor="hand2",
            command=self.alternar_ordem_atualizacoes,
        )
        btn_ordem.pack(side="right", padx=15, pady=10)

        # Corpo rolavel (para quando houver muitas atualizações)
        corpo_card = tk.Frame(frame_card, bg="#ffffff")
        corpo_card.pack(fill="both", expand=True)
        corpo_card.grid_rowconfigure(0, weight=1)
        corpo_card.grid_columnconfigure(0, weight=1)

        canvas_card = tk.Canvas(corpo_card, bg="#ffffff", highlightthickness=0)
        canvas_card.grid(row=0, column=0, sticky="nsew")

        scrollbar_card = tk.Scrollbar(corpo_card, orient="vertical", command=canvas_card.yview)
        scrollbar_card.grid(row=0, column=1, sticky="ns")

        scrollbar_card_x = tk.Scrollbar(corpo_card, orient="horizontal", command=canvas_card.xview)
        scrollbar_card_x.grid(row=1, column=0, sticky="ew")

        canvas_card.configure(yscrollcommand=scrollbar_card.set, xscrollcommand=scrollbar_card_x.set)

        frame_logs = tk.Frame(canvas_card, bg="#ffffff")
        janela_logs = canvas_card.create_window((0, 0), window=frame_logs, anchor="nw")

        def _ajustar_largura_conteudo(event=None):
            largura_canvas = canvas_card.winfo_width()
            largura_conteudo = frame_logs.winfo_reqwidth()
            nova_largura = max(largura_canvas, largura_conteudo)
            canvas_card.itemconfig(janela_logs, width=nova_largura)
            canvas_card.configure(scrollregion=canvas_card.bbox("all"))

        frame_logs.bind("<Configure>", _ajustar_largura_conteudo)
        canvas_card.bind("<Configure>", _ajustar_largura_conteudo)

        def _on_mousewheel(event):
            canvas_card.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas_card.bind("<Enter>", lambda e: canvas_card.bind_all("<MouseWheel>", _on_mousewheel))
        canvas_card.bind("<Leave>", lambda e: canvas_card.unbind_all("<MouseWheel>"))

        # Mostra as ultimas acoes realizadas na aplicacao (cadastros, atualizacoes,
        # vendas, exclusoes), sempre com a mais recente aparecendo primeiro por
        # padrao -- nunca em ordem alfabetica. O botao acima permite inverter
        # para ver as mais antigas primeiro, se preferir.
        lista_logs = obter_atividades(15)

        if not lista_logs:
            lista_logs = [
                "Sistema iniciado com sucesso.",
                "Aguardando novas inserções ou atualizações no Banco de Dados MySQL.",
            ]
        elif not self.ordem_atualizacoes_recente_primeiro:
            lista_logs = list(reversed(lista_logs))

        for log in lista_logs:
            lbl_log = tk.Label(frame_logs, text=f"• {log}", font=("poppins", 11), fg="#4a0e06", bg="#ffffff", anchor="w", padx=20, pady=8)
            lbl_log.pack(fill="x")
