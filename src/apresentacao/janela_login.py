import tkinter as tk
from .login import Login

class TelaLogin:
    def __init__(self, janela):
        # 1. Configurações da janela principal
        self.janela = janela
        self.janela.title("Login do administrador")
        self.login_service = Login()
        self.janela.configure(bg="#941b0c")
        
        self.janela.state('zoomed') 
        
        self.janela.grid_columnconfigure(0, weight=1)
        self.janela.grid_rowconfigure(0, weight=1)
        
        self.criar_widgets()

    
    def on_enter(self, event=None):
        self.verificar_login()

    def verificar_login(self):
        # Protecao extra: se por algum motivo este metodo for chamado de novo
        # apos a tela de login ja ter sido destruida (ex: evento duplicado),
        # simplesmente ignora em vez de estourar erro.
        if not self.entrada_usuario.winfo_exists():
            return

        usuario = self.entrada_usuario.get().strip()
        senha = self.entrada_senha.get().strip()
        
        # 4. Autenticação do usuário usando a classe Login
        usuario_logado = self.login_service.autenticar(usuario, senha)
        
        if usuario_logado:
            # Remove o atalho de tecla ligado a janela antes de destruir os widgets
            # da tela de login, para evitar callbacks em widgets ja destruidos.
            self.janela.unbind("<Return>")

            for widget in self.janela.winfo_children():
                widget.destroy()
    
            from .telainicial.janela_inicial import TelaInicial
            TelaInicial(self.janela, usuario_logado)
        else:
            self.lbl_erro.config(text="Usuário ou senha incorretos.")

    def desenhar_retangulo_arredondado(self, canvas, x1, y1, x2, y2, raio, **kwargs):
        
        # 2. Desenhando um retângulo arredondado no canvas
        pontos = [x1 + raio, y1, x1 + raio, y1, x2 - raio, y1, x2 - raio, y1, x2, y1, x2, y1 + raio, x2, y1 + raio, x2, y2 - raio, x2, y2 - raio, x2, y2, x2 - raio, y2, x2 - raio, y2, x1 + raio, y2, x1 + raio, y2, x1, y2, x1, y2 - raio, x1, y2 - raio, x1, y1 + raio, x1, y1 + raio, x1, y1]
        return canvas.create_polygon(pontos, **kwargs, smooth=True)

    def criar_widgets(self):
        
        # 3. Criando o layout da tela de login
        self.canvas = tk.Canvas(self.janela, width=450, height=520, bg="#941b0c", highlightthickness=0)
        self.canvas.grid(row=0, column=0)

        self.canvas.create_text(225, 30, text="Titan", font=("poppins", 32, "bold"), fill="#ffffff")
        
        self.canvas.create_text(225, 75, text="Loja de mídia física para música", font=("poppins", 12), fill="#ffffff")

        self.desenhar_retangulo_arredondado(self.canvas, 10, 110, 440, 510, raio=40, fill="#fff5f5")

        self.canvas.create_text(50, 155, text="Login", font=("poppins", 14, "bold"), fill="#4a0e06", anchor="w")
        
        self.desenhar_retangulo_arredondado(self.canvas, 50, 180, 400, 225, raio=20, fill="#ffffff", outline="#efe0e0")
        
        self.entrada_usuario = tk.Entry(self.janela, font=("poppins", 12), bg="#ffffff", bd=0, highlightthickness=0)
        self.canvas.create_window(225, 203, window=self.entrada_usuario, width=330, height=30)

        self.canvas.create_text(50, 265, text="Senha", font=("poppins", 14, "bold"), fill="#4a0e06", anchor="w")
        
        self.desenhar_retangulo_arredondado(self.canvas, 50, 290, 400, 335, raio=20, fill="#ffffff", outline="#efe0e0")
        
        self.entrada_senha = tk.Entry(self.janela, show="*", font=("poppins", 12), bg="#ffffff", bd=0, highlightthickness=0)
        self.canvas.create_window(225, 313, window=self.entrada_senha, width=330, height=30)
            
            # 3.1. Botão de login
        self.desenhar_retangulo_arredondado(self.canvas, 150, 410, 300, 455, raio=20, fill="#ffffff", outline="#fff5f5")
        
        self.botao_login = tk.Button(self.janela, text="Entrar", font=("poppins", 11, "bold"), fg="#4a0e06", bg="#ffffff", bd=0, activebackground="#f5e6e6", activeforeground="#4a0e06",cursor="hand2",command=self.verificar_login)
        self.canvas.create_window(225, 433, window=self.botao_login, width=146, height=42)

        # Opcao de sair (encerrar) exigida pelos criterios de aceitacao da US01,
        # disponivel diretamente na tela de login (nao so depois de autenticar).
        self.botao_sair = tk.Button(self.janela, text="Sair", font=("poppins", 10, "underline"), fg="#ffffff", bg="#941b0c", bd=0, activebackground="#941b0c", activeforeground="#f39274", cursor="hand2", command=self.janela.destroy)
        self.canvas.create_window(225, 480, window=self.botao_sair, width=100, height=24)

        self.lbl_erro = tk.Label(self.janela, text="", font=("poppins", 10), fg="#ff3333", bg="#fff5f5")
        self.canvas.create_window(225, 375, window=self.lbl_erro, width=350)

        self.janela.bind("<Return>", self.on_enter)
