import tkinter as tk

from negocio.atividades import registrar_atividade


class ExclusaoMixin:
    """Modal de confirmação e execução da exclusão de um álbum.

    Depende de DesenhoMixin (self.desenhar_fundo_arredondado) e de
    ListagemMixin (self.atualizar_listagem / self.obter_albuns).
    """

    def abrir_modal_confirmacao_exclusao(self, album_id: int, album_nome: str):
        modal = tk.Toplevel(self.parent)
        modal.title("Confirmar exclusão")
        modal.geometry("420x220")
        modal.resizable(False, False)
        modal.configure(bg="#ffe8e4")
        modal.transient(self.parent)
        modal.grab_set()

        screen_width = modal.winfo_screenwidth()
        screen_height = modal.winfo_screenheight()
        x = (screen_width - 420) // 2
        y = (screen_height - 220) // 2
        modal.geometry(f"420x220+{x}+{y}")

        canvas_modal = self.desenhar_fundo_arredondado(modal, largura=400, altura=200, raio=24, cor_fundo="#ffe8e4", cor_forma="#ffffff")
        canvas_modal.place(relx=0.5, rely=0.5, anchor="center")

        frame_modal = tk.Frame(modal, bg="#ffffff", bd=0, relief="flat")
        canvas_modal.create_window(200, 100, window=frame_modal, width=380, height=180)

        titulo = tk.Label(frame_modal, text="Tem certeza de que deseja excluir este álbum?", font=("poppins", 14, "bold"), fg="#5f1c16", bg="#ffffff", wraplength=340, justify="center")
        titulo.pack(anchor="center", pady=(25, 20), padx=10)

        botoes_frame = tk.Frame(frame_modal, bg="#ffffff")
        botoes_frame.pack(fill="x", padx=20, pady=(0, 10))

        canvas_btn_sim = self.desenhar_fundo_arredondado(botoes_frame, largura=140, altura=40, raio=18, cor_fundo="#ffffff", cor_forma=self.COR_VERMELHO_BOTAO)
        canvas_btn_sim.pack(side="left", expand=True, padx=(0, 8))
        btn_sim = tk.Button(canvas_btn_sim, text="Sim", font=("poppins", 11, "bold"), fg="#ffffff", bg=self.COR_VERMELHO_BOTAO, bd=0, activebackground="#d14d3a", cursor="hand2", command=lambda: self.excluir_album(album_id, album_nome, modal))
        canvas_btn_sim.create_window(70, 20, window=btn_sim, width=120, height=34)

        canvas_btn_nao = self.desenhar_fundo_arredondado(botoes_frame, largura=140, altura=40, raio=18, cor_fundo="#ffffff", cor_forma="#f0d7d3")
        canvas_btn_nao.pack(side="right", expand=True, padx=(8, 0))
        btn_nao = tk.Button(canvas_btn_nao, text="Não", font=("poppins", 11, "bold"), fg="#5f1c16", bg="#f0d7d3", bd=0, activebackground="#e4d1cd", cursor="hand2", command=modal.destroy)
        canvas_btn_nao.create_window(70, 20, window=btn_nao, width=120, height=34)

    def excluir_album(self, album_id: int, album_nome: str, modal):
        if self.servico_album is None:
            modal.destroy()
            return

        try:
            self.servico_album.remover_album(album_id)
        except ValueError as erro:
            self.lbl_status_busca.config(text=str(erro))
        except Exception:
            self.lbl_status_busca.config(text="Você não pode excluir um álbum associado a uma venda.")
        else:
            registrar_atividade(f"Álbum '{album_nome}' removido do catálogo.")
            self.atualizar_listagem(self.obter_albuns())
        finally:
            modal.destroy()
