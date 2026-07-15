import tkinter as tk

from apresentacao.janela_login import TelaLogin


def principal() -> None:
    janela = tk.Tk()
    TelaLogin(janela)
    janela.mainloop()


if __name__ == "__main__":
    principal()
