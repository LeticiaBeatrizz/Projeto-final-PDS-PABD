import tkinter as tk
from tkinter import messagebox, ttk

from negocio.atividades import registrar_atividade


class RemoverEstoqueMixin:
    """Modal de remoção de unidades do estoque de um álbum.

    Depende de ModaisBaseMixin (self.criar_modal_rolavel), DesenhoMixin
    (self.desenhar_fundo_arredondado) e ListagemMixin (self.obter_albuns / self.atualizar_listagem).
    """

    def abrir_modal_remover_estoque(self):
        albuns = self.obter_albuns()
        if not albuns:
            messagebox.showwarning("Aviso", "Cadastre um álbum antes de remover estoque.")
            return

        modal, frame_modal, botoes_frame = self.criar_modal_rolavel("Remover do estoque", largura=500, altura_desejada=500)

        titulo = tk.Label(frame_modal, text="Remover do estoque", font=("poppins", 16, "bold"), fg="#5f1c16", bg="#ffffff")
        titulo.pack(anchor="nw", pady=(22, 15), padx=20)

        mapa_albuns = {f"{album['nome']} — {album['artista']} ({album['genero']})": album for album in albuns}
        opcoes = list(mapa_albuns.keys())

        container_album = tk.Frame(frame_modal, bg="#ffffff")
        container_album.pack(fill="x", padx=20, pady=(0, 12))
        tk.Label(container_album, text="Álbum*", font=("poppins", 10, "bold"), fg="#5f1c16", bg="#ffffff").pack(anchor="w")

        combo_album = ttk.Combobox(container_album, values=opcoes, state="readonly", font=("poppins", 10))
        combo_album.pack(fill="x", pady=(8, 0), ipady=4)

        container_qtd = tk.Frame(frame_modal, bg="#ffffff")
        container_qtd.pack(fill="x", padx=20, pady=(0, 12))
        tk.Label(container_qtd, text="Quantidade*", font=("poppins", 10, "bold"), fg="#5f1c16", bg="#ffffff").pack(anchor="w")
        entry_quantidade = tk.Entry(container_qtd, font=("poppins", 10), bd=0, bg="#faf5f4", fg="#4a0e06", insertbackground="#4a0e06")
        entry_quantidade.pack(fill="x", pady=(8, 0), ipady=8)
        entry_quantidade.configure(highlightthickness=1, highlightbackground="#f0d7d3", highlightcolor="#f0d7d3")

        lbl_estoque_atual = tk.Label(frame_modal, text="Estoque atual: '--'", font=("poppins", 11, "bold"), fg=self.COR_TEXTO_ESCURO, bg="#ffffff")
        lbl_estoque_atual.pack(anchor="w", padx=20, pady=(6, 0))

        lbl_apos_operacao = tk.Label(frame_modal, text="Após a operação: '--'", font=("poppins", 11, "bold"), fg=self.COR_TEXTO_ESCURO, bg="#ffffff")
        lbl_apos_operacao.pack(anchor="w", padx=20, pady=(4, 0))

        lbl_mensagem_modal = tk.Label(frame_modal, text="", font=("poppins", 9), fg="#c94a3f", bg="#ffffff", wraplength=380, justify="left")
        lbl_mensagem_modal.pack(anchor="w", padx=20, pady=(8, 12))

        def obter_estoque_atual(album_id: int) -> int:
            if self.servico_estoque is None:
                return 0
            try:
                return self.servico_estoque.contar_disponivel(album_id)
            except Exception:
                return 0

        def atualizar_previa(*_args):
            album_selecionado = mapa_albuns.get(combo_album.get())
            if album_selecionado is None:
                lbl_estoque_atual.config(text="Estoque atual: '--'")
                lbl_apos_operacao.config(text="Após a operação: '--'")
                return

            atual = obter_estoque_atual(album_selecionado["id"])
            lbl_estoque_atual.config(text=f"Estoque atual: '{atual}'")

            texto_quantidade = entry_quantidade.get().strip()
            try:
                quantidade = int(texto_quantidade)
                if quantidade < 0:
                    raise ValueError
            except ValueError:
                lbl_apos_operacao.config(text=f"Após a operação: '{atual}'")
                return

            lbl_apos_operacao.config(text=f"Após a operação: '{max(atual - quantidade, 0)}'")

        combo_album.bind("<<ComboboxSelected>>", atualizar_previa)
        entry_quantidade.bind("<KeyRelease>", atualizar_previa)

        canvas_btn_cancelar = self.desenhar_fundo_arredondado(botoes_frame, largura=190, altura=42, raio=18, cor_fundo="#ffffff", cor_forma="#f0d7d3")
        canvas_btn_cancelar.pack(side="left", padx=(0, 8))
        btn_cancelar = tk.Button(canvas_btn_cancelar, text="Cancelar", font=("poppins", 10, "bold"), fg="#5f1c16", bg="#f0d7d3", bd=0, activebackground="#e4d1cd", cursor="hand2", command=modal.destroy)
        canvas_btn_cancelar.create_window(95, 21, window=btn_cancelar, width=170, height=38)

        def confirmar_remocao():
            album_selecionado = mapa_albuns.get(combo_album.get())
            if album_selecionado is None:
                lbl_mensagem_modal.config(text="Selecione um álbum.")
                return

            texto_quantidade = entry_quantidade.get().strip()
            try:
                quantidade = int(texto_quantidade)
                if quantidade <= 0:
                    raise ValueError
            except ValueError:
                lbl_mensagem_modal.config(text="Informe uma quantidade válida (numero inteiro maior que zero).")
                return

            if self.servico_estoque is None:
                modal.destroy()
                return

            try:
                self.servico_estoque.remover_multiplos(album_selecionado["id"], quantidade)
            except ValueError as erro:
                lbl_mensagem_modal.config(text=str(erro))
                return
            except Exception:
                lbl_mensagem_modal.config(text="Falha ao remover do estoque no banco de dados.")
                return

            registrar_atividade(f"Estoque do álbum '{album_selecionado['nome']}' reduzido em {quantidade} unidade(s).")
            messagebox.showinfo("Sucesso", "Estoque atualizado com sucesso!")
            modal.destroy()
            self.atualizar_listagem(self.obter_albuns())

        canvas_btn_remover_confirmar = self.desenhar_fundo_arredondado(botoes_frame, largura=190, altura=42, raio=18, cor_fundo="#ffffff", cor_forma="#d14d3a")
        canvas_btn_remover_confirmar.pack(side="left", padx=(8, 0))
        btn_remover_confirmar = tk.Button(canvas_btn_remover_confirmar, text="Remover", font=("poppins", 10, "bold"), fg="#ffffff", bg="#d14d3a", bd=0, activebackground="#b63e2a", cursor="hand2", command=confirmar_remocao)
        canvas_btn_remover_confirmar.create_window(95, 21, window=btn_remover_confirmar, width=170, height=38)
