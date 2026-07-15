import tkinter as tk
from tkinter import messagebox

from negocio.atividades import registrar_atividade


class AtualizacaoMixin:
    """Modal de atualização de um álbum existente.

    Depende de ModaisBaseMixin (self.criar_modal_rolavel), DesenhoMixin
    (self.desenhar_fundo_arredondado) e ListagemMixin (self.atualizar_listagem / self.obter_albuns).
    """

    def abrir_modal_atualizacao(self, album: dict):
        modal, frame_modal, botoes_frame = self.criar_modal_rolavel("Atualizar álbum", largura=460, altura_desejada=600)

        titulo = tk.Label(frame_modal, text="Atualizar álbum", font=("poppins", 16, "bold"), fg="#5f1c16", bg="#ffffff")
        titulo.pack(anchor="nw", pady=(22, 15), padx=20)

        def criar_campo(label_text, valor_inicial=""):
            container = tk.Frame(frame_modal, bg="#ffffff")
            container.pack(fill="x", padx=20, pady=(0, 12))
            tk.Label(container, text=label_text, font=("poppins", 10, "bold"), fg="#5f1c16", bg="#ffffff").pack(anchor="w")
            entry = tk.Entry(container, font=("poppins", 10), bd=0, bg="#faf5f4", fg="#4a0e06", insertbackground="#4a0e06")
            entry.insert(0, str(valor_inicial))
            entry.pack(fill="x", pady=(8, 0), ipady=8)
            entry.configure(highlightthickness=1, highlightbackground="#f0d7d3", highlightcolor="#f0d7d3")
            return entry

        entry_nome = criar_campo("Nome*", album.get("nome", ""))
        entry_artista = criar_campo("Artista(s) associado(s)*", album.get("artista", ""))
        entry_genero = criar_campo("Gênero*", album.get("genero", ""))
        entry_tamanho = criar_campo("Tamanho (faixas)*", album.get("tamanho", ""))
        entry_preco = criar_campo("Valor (R$)*", album.get("preco", ""))

        lbl_mensagem = tk.Label(frame_modal, text="", font=("poppins", 9), fg="#c94a3f", bg="#ffffff", wraplength=380, justify="left")
        lbl_mensagem.pack(anchor="w", padx=20, pady=(0, 12))

        canvas_btn_cancelar = self.desenhar_fundo_arredondado(botoes_frame, largura=170, altura=42, raio=18, cor_fundo="#ffffff", cor_forma="#f0d7d3")
        canvas_btn_cancelar.pack(side="left", padx=(0, 8))
        btn_cancelar = tk.Button(canvas_btn_cancelar, text="Cancelar", font=("poppins", 10, "bold"), fg="#5f1c16", bg="#f0d7d3", bd=0, activebackground="#e4d1cd", cursor="hand2", command=modal.destroy)
        canvas_btn_cancelar.create_window(85, 21, window=btn_cancelar, width=150, height=38)

        def confirmar_atualizacao():
            nome = entry_nome.get().strip()
            artista_texto = entry_artista.get().strip()
            genero_texto = entry_genero.get().strip()
            tamanho_texto = entry_tamanho.get().strip()
            preco_texto = entry_preco.get().strip()

            if not artista_texto:
                lbl_mensagem.config(text="Informe o(s) artista(s) associado(s).")
                return

            try:
                tamanho = int(tamanho_texto)
            except ValueError:
                lbl_mensagem.config(text="Informe um tamanho válido (numero inteiro maior que zero).")
                return

            try:
                preco = float(str(preco_texto).replace(',', '.'))
            except ValueError:
                lbl_mensagem.config(text="Informe um valor numérico válido.")
                return

            if self.servico_album is None:
                modal.destroy()
                return

            try:
                self.servico_album.atualizar_album(album.get("id"), nome, genero_texto, artista_texto, tamanho, preco)
            except ValueError as erro:
                lbl_mensagem.config(text=str(erro))
                return
            except Exception:
                lbl_mensagem.config(text="Falha ao atualizar o álbum no banco de dados.")
                return

            registrar_atividade(f"Álbum '{nome}' atualizado com sucesso!")
            messagebox.showinfo("Sucesso", "Álbum atualizado com sucesso!")
            modal.destroy()
            self.atualizar_listagem(self.obter_albuns())

        canvas_btn_atualizar = self.desenhar_fundo_arredondado(botoes_frame, largura=170, altura=42, raio=18, cor_fundo="#ffffff", cor_forma="#d14d3a")
        canvas_btn_atualizar.pack(side="left", padx=(8, 0))
        btn_atualizar_modal = tk.Button(canvas_btn_atualizar, text="Atualizar", font=("poppins", 10, "bold"), fg="#ffffff", bg="#d14d3a", bd=0, activebackground="#b63e2a", cursor="hand2", command=confirmar_atualizacao)
        canvas_btn_atualizar.create_window(85, 21, window=btn_atualizar_modal, width=150, height=38)
