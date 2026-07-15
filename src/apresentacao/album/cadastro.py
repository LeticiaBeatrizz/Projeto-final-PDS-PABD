import tkinter as tk
from tkinter import messagebox

from negocio.atividades import registrar_atividade


class CadastroMixin:
    """Modal de cadastro de um novo álbum.

    Depende de ModaisBaseMixin (self.criar_modal_rolavel), DesenhoMixin
    (self.desenhar_fundo_arredondado) e ListagemMixin (self.atualizar_listagem / self.obter_albuns).
    """

    def abrir_modal_cadastro(self):
        modal, frame_modal, botoes_frame = self.criar_modal_rolavel("Cadastrar novo álbum", largura=460, altura_desejada=600)

        titulo = tk.Label(frame_modal, text="Cadastrar novo álbum", font=("poppins", 16, "bold"), fg="#5f1c16", bg="#ffffff")
        titulo.pack(anchor="nw", pady=(22, 15), padx=20)

        def criar_campo(label_text):
            container = tk.Frame(frame_modal, bg="#ffffff")
            container.pack(fill="x", padx=20, pady=(0, 12))
            tk.Label(container, text=label_text, font=("poppins", 10, "bold"), fg="#5f1c16", bg="#ffffff").pack(anchor="w")
            entry = tk.Entry(container, font=("poppins", 10), bd=0, bg="#faf5f4", fg="#4a0e06", insertbackground="#4a0e06")
            entry.pack(fill="x", pady=(8, 0), ipady=8)
            entry.configure(highlightthickness=1, highlightbackground="#f0d7d3", highlightcolor="#f0d7d3")
            return entry

        self.entry_nome = criar_campo("Nome*")
        self.entry_artista = criar_campo("Artista(s) associado(s)*")
        self.entry_genero = criar_campo("Gênero*")
        self.entry_tamanho = criar_campo("Tamanho (faixas)*")
        self.entry_preco = criar_campo("Valor (R$)*")

        self.lbl_mensagem_modal = tk.Label(frame_modal, text="", font=("poppins", 9), fg="#c94a3f", bg="#ffffff", wraplength=380, justify="left")
        self.lbl_mensagem_modal.pack(anchor="w", padx=20, pady=(0, 12))

        canvas_btn_cancelar = self.desenhar_fundo_arredondado(botoes_frame, largura=170, altura=42, raio=18, cor_fundo="#ffffff", cor_forma="#f0d7d3")
        canvas_btn_cancelar.pack(side="left", padx=(0, 8))
        btn_cancelar = tk.Button(canvas_btn_cancelar, text="Cancelar", font=("poppins", 10, "bold"), fg="#5f1c16", bg="#f0d7d3", bd=0, activebackground="#e4d1cd", cursor="hand2", command=modal.destroy)
        canvas_btn_cancelar.create_window(85, 21, window=btn_cancelar, width=150, height=38)

        canvas_btn_cadastrar = self.desenhar_fundo_arredondado(botoes_frame, largura=170, altura=42, raio=18, cor_fundo="#ffffff", cor_forma="#d14d3a")
        canvas_btn_cadastrar.pack(side="left", padx=(8, 0))
        btn_cadastrar_modal = tk.Button(canvas_btn_cadastrar, text="Cadastrar", font=("poppins", 10, "bold"), fg="#ffffff", bg="#d14d3a", bd=0, activebackground="#b63e2a", cursor="hand2", command=lambda: self.confirmar_cadastro(modal))
        canvas_btn_cadastrar.create_window(85, 21, window=btn_cadastrar_modal, width=150, height=38)

    def confirmar_cadastro(self, modal):
        nome = self.entry_nome.get().strip()
        artista_texto = self.entry_artista.get().strip()
        genero_texto = self.entry_genero.get().strip()
        tamanho_texto = self.entry_tamanho.get().strip()
        preco_texto = self.entry_preco.get().strip()

        if not nome:
            self.lbl_mensagem_modal.config(text="Informe o nome do álbum.")
            return
        if not artista_texto:
            self.lbl_mensagem_modal.config(text="Informe o(s) artista(s) associado(s).")
            return
        if not genero_texto:
            self.lbl_mensagem_modal.config(text="Informe o gênero do álbum.")
            return
        if not tamanho_texto:
            self.lbl_mensagem_modal.config(text="Informe o tamanho do álbum.")
            return
        if not preco_texto:
            self.lbl_mensagem_modal.config(text="Informe o valor do álbum.")
            return

        try:
            tamanho = int(tamanho_texto)
            if tamanho <= 0:
                raise ValueError
        except ValueError:
            self.lbl_mensagem_modal.config(text="Informe um tamanho válido (numero inteiro maior que zero).")
            return

        try:
            preco = float(preco_texto.replace(',', '.'))
            if preco < 0:
                raise ValueError
        except ValueError:
            self.lbl_mensagem_modal.config(text="Informe um valor numérico válido.")
            return

        if self.servico_album is not None:
            try:
                self.servico_album.cadastrar_album(nome, genero_texto, artista_texto, tamanho, preco)
            except ValueError as erro:
                self.lbl_mensagem_modal.config(text=str(erro))
                return
            except Exception:
                self.lbl_mensagem_modal.config(text="Falha ao salvar o álbum no banco de dados.")
                return

            registrar_atividade(f"Álbum '{nome}' cadastrado com sucesso!")
            messagebox.showinfo("Sucesso", "Álbum cadastrado com sucesso!")

        modal.destroy()
        self.atualizar_listagem(self.obter_albuns())
